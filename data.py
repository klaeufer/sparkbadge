#!/usr/bin/env python3
import os

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


def get_commit_sha(user: str, repo: str, until_time: str) -> str:
    url = '/'.join([git_api_base, user, repo, "commits"])
    result = requests.get(url)
    data = json.loads(result.text)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    sha = ""
    i = 0
    found = False
    while i < len(data) and not found:
        i_date = data[i]['commit']['author']['date']
        i_sha = data[i]['sha']
        if i_date < until_time:
            sha = i_sha
            found = True
        i += 1
    print(sha)
    return sha


def get_size(user: str, repo: str, sha: str):
    url = '/'.join([git_api_base, user, repo, "git/trees", sha])
    result = requests.get(url)
    print(type(result.text))
    if result.text.startswith("{\"message\":\"Not Found\""):
        with open('data.json', 'r') as file:
            lines = file.readlines()
            data = json.loads(lines)
    else:
        data = json.loads(result.text)
    total_size = 0
    for i in data['tree']:
        total_size += i['size']
    return total_size


def repo_size():
    data_points = []
    for day in range(20, 31):
        time = "2020-11-" + str(day) + "T00:00:00Z"
        commit_sha = get_commit_sha(user="Landaluce", repo="sparkbadge", until_time=time)
        data_points.append(get_size(user="Landaluce", repo="sparkbadge", sha=commit_sha))
    print(data_points)
    if len(data_points):
        plot(data_points=data_points, output_file="images/repo_size")
    return data_points


repo_size()
