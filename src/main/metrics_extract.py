import datetime
import requests
import numpy as np

# Github Actions: workflow runs
def actions_runs(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs' 
    response = requests.get(url=url)
    data = response.json()
    wf_runs = data['workflow_runs']
    for wf in wf_runs:
        run_url = wf['url']
        run = requests.get(url=run_url).json()

        run_id = run['id']
        status = run['status']
        conclusion = run['conclusion']
        start = run['created_at'] 
        end = run['updated_at'] 
        duration = build_duration(end) - build_duration(start)

        print('----------------------------------------------')
        print(f'ID: {run_id}  STATUS: {status}  CONCLUSION: {conclusion}')
        print(f'START: {start}  END: {end}  DURATION: {duration} s')


# Github Actions: workflow jobs 
def actions_jobs(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs' 
    response = requests.get(url=url)
    data = response.json()
    wf_runs = data['workflow_runs']
    # Create a dict of unique jobs
    job_set = set([])
    for wf in wf_runs:
        jobs_url = wf['jobs_url']
        job = requests.get(url=jobs_url).json()
        # valid_job is {job_id : run_id}
        job_set.add(job['id']) 
        run_id = job['run_id']
        status = job['status']
        conclusion = job['conclusion']

        start = job['created_at'] 
        end = job['updated_at'] 
        duration = build_duration(end) - build_duration(start)

        print('----------------------------------------------')
        print(f'ID: {run_id}  STATUS: {status}  CONCLUSION: {conclusion}')
        print(f'START: {start}  END: {end}  DURATION: {duration} s')


def issues(owner, repo):
    """
    Longitudal status of repository issues. Returns two lists (opened and closed issues) where 
    index is equal to the month and the value is the number of issues opened/closed.
    """

    url = f'https://api.github.com/repos/{owner}/{repo}/issues?state=all' 
    response = requests.get(url=url)
    issues = response.json()
    
    opened = list(np.zeros(12, dtype=int))
    closed = list(np.zeros(12, dtype=int))

    for issue in issues:
        opened_in_month = datetime.datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ').month
        closed_in_month = None

        opened[opened_in_month-1]+=1

        if issue['closed_at']:
            closed_in_month = datetime.datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ').month
            closed[closed_in_month-1]+=1

    print('opened: ' , opened)
    print('closed: ' , closed)

    return opened, closed


def build_duration(utc):
    dt = datetime.datetime.strptime(utc, '%Y-%m-%dT%H:%M:%SZ')
    ut = dt.timestamp()
    return ut

#iss = issues('nshan651', 'excite-cli')
