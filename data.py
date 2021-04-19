#!/usr/bin/env python3
from functions import is_int
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
    until_date = until_date.split('T')[0].split('-')
    time = "T00:00:00Z"
    shas = []
    dates = []
    try:
        result = requests.get(url)
        data = json.loads(result.text)
        for i in data:
            date = i['commit']['author']['date']
            end = '-'.join(until_date) + time
            if date >= end:
                sha = i['sha']
                shas.append(sha)
                dates.append(date)
    except Exception as e:
        print(str(e))
    return [shas, dates]


def get_commits_sizes(user: str, repo: str, shas: list) -> list:
    commits_sizes = []
    for sha in shas:
        url = '/'.join([git_api_base, user, repo, "git/trees", str(sha)])
        try:
            result = requests.get(url)
            data = json.loads(result.text)
            tree = str(data).split("'tree':")[1]
            sizes_in_tree = tree.split("'size':")
            tree_sizes = []
            for size in sizes_in_tree:
                value = size.split(',')[0]
                if is_int(value):
                    tree_sizes.append(int(value))
            commits_sizes.append(sum(tree_sizes))
        except Exception as e:
            print(str(e))
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
        if i - 1 >= 0:
            data_points[i] += data_points[i - 1]
    return data_points


def repo_size(user: str, repo: str) -> list:
    results = get_commit_sha(user=user, repo=repo, until_date="2020-11-18")
    data_points = []
    if len(results[0]):
        commits_sizes = get_commits_sizes(user=user, repo=repo, shas=results[0])
        if len(results[1]):
            data_points = get_data_points(shas=results[0], dates=results[1], commits_sizes=commits_sizes)
            if len(data_points) > 1:
                plot(data_points=data_points)
    return data_points


repo_size(user="Landaluce", repo="sparkbadge")
