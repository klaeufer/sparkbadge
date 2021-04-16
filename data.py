#!/usr/bin/env python3
from plot import plot
import requests
import random
import json


def sample():
    return random.sample(range(20, 30), 10)


# Travis API doc
# https://docs.travis-ci.com/api/?http#builds


travis_base = "https://api.travis-ci.org/repos/"
travis_status_map = {None: -1, 0: 0}
git_api_base = "https://api.github.com/repos"


def travis(user, repo):
    url = travis_base + user + "/" + repo + "/builds"
    res = requests.get(url)
    data = json.loads(res.text)
    return [travis_status_map[s['result']] for s in data]


def get_commit_sha(user: str, repo: str, until_date: str) -> list:
    url = '/'.join([git_api_base, user, repo, "commits"])
    result = requests.get(url)
    data = json.loads(result.text)
    shas = []
    dates = []
    time = "T00:00:00Z"
    if "API rate limit exceeded" not in str(data) and "{\"message\":\"Not Found\"" not in str(data):
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
    else:
        with open('data.json', 'r') as file:
            lines = file.readlines()
        data = json.loads(lines[0])
    until_date = until_date.split('T')[0].split('-')
    for i in data:
        date = i['commit']['author']['date']
        end = '-'.join(until_date) + time
        if date >= end:
            sha = i['sha']
            shas.append(sha)
            dates.append(date)
    return [shas, dates]


def get_commits_sizes(user: str, repo: str, shas: list) -> list:
    commits_sizes = []
    size = 0
    for sha in shas:
        url = '/'.join([git_api_base, user, repo, "git/trees", str(sha)])
        data = None
        try:
            result = requests.get(url)
            data = json.loads(result.text)
        except:
            pass
        if "API rate limit exceeded" not in str(data) and "{\"message\":\"Not Found\"" not in str(data):
            with open('size.json', 'w') as json_file:
                json.dump(data, json_file)
        else:
            with open('size.json', 'r') as file:
                lines = file.readlines()
            data = json.loads(lines[0])
        if 'tree' in data.keys():
            for i in data['tree']:
                if 'size' in i.keys():
                    size += i['size']
            commits_sizes.append(size)
    return commits_sizes


def get_data_points(shas, dates, commits_sizes) -> list:
    date_holder = dates[0]
    data_points = []
    data_point = 0
    for sha, date, size in zip(shas, dates, commits_sizes):
        if date[:10] == date_holder[:10]:
            data_point += size
        else:
            data_points.append(data_point)
            data_point = size
            date_holder = date
    for i in range(len(data_points)):
        if i-1 >= 0:
            data_points[i] += data_points[i-1]
    return data_points


def repo_size(user: str, repo: str) -> list:
    result = get_commit_sha(user=user, repo=repo,  until_date="2020-11-18")
    commits_sizes = get_commits_sizes(user=user, repo=repo, shas=result[0])
    data_points = get_data_points(shas=result[0], dates=result[1], commits_sizes=commits_sizes)
    if len(data_points) > 1:
        plot(data_points=data_points, output_file="images/repo_size")
    return data_points


repo_size(user="Landaluce", repo="sparkbadge")
