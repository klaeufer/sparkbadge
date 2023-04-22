from typing import Dict 
import api

def github_stars(owner: str, repo: str) -> Dict:
    """List repository stars.
    Note: we need to use https://www.gharchive.org/ to do this

    Args:
        owner: Repository owner.
        repo: The repository to scan.

    Returns:
    """

def github_issues(owner: str, repo: str) -> Dict:
    """List issues.
    See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues
    
    Args:
        owner: Repository owner.
        repo: The repository to scan.

    Returns:
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/issues' 
    params = {
        "per_page" : 10,
        "since": "2018-01-01T00:00:00Z",
        "direction": "asc",
    }
    payload = api.connect_to_endpoint(url, params)
    issue_data = lambda issues: {
        str(issue["id"]) : {
            "created_at": issue["created_at"],
            "closed_at": issue["closed_at"],
            "state" : issue["state"],
        } 
        for issue in issues 
    }
    return issue_data(payload)


def github_commits(owner: str, repo: str) -> Dict:
    """List commits.
    
    Args:
        owner: Repository owner.
        repo: The repository to scan.

    Returns:
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/commits' 
    params = {
        "per_page" : 10,
        "until": "2021-01-01",
        # "since": "2021-01-01",
    }
    payload = api.connect_to_endpoint(url, params)
    commit_data = lambda commits: {
        str(commit["sha"]) : {
            "authored_at": commit["commit"]["author"]["date"], 
            "applied_at": commit["commit"]["committer"]["date"],
            "verified" : commit["commit"]["verification"]["verified"]
        } 
        for commit in commits 
    }
    return commit_data(payload)


def github_runs(owner: str, repo: str) -> Dict:
    """List action runs in a github repository.

    curl -H "Accept: application/vnd.github.v3+json"
    https://api.github.com/rate_limit
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs' 
    params = {
        "status": "completed",
        "per_page" : 10,
        "created": "<2022-01-01"
    }
    payload = api.connect_to_endpoint(url, params)["workflow_runs"]
    run_data = lambda runs: {
        str(run["id"]) : {
            "created_at": run["created_at"], 
            "conclusion": run["conclusion"] 
        } 
        for run in runs
    }
    return run_data(payload)


# github_runs("facebook", "react")
# github_commits("facebook", "react")
github_issues("facebook", "react")
