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
    sha = ""
    if "API rate limit exceeded" not in data and "{\"message\":\"Not Found\"" not in data:
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
        i = 0
        found = False
        while i < len(data) and not found:
            i_date = data[i]['commit']['author']['date']
            i_sha = data[i]['sha']
            if i_date < until_time:
                sha = i_sha
                found = True
            i += 1
    return sha


def get_size(user: str, repo: str, sha: str):
    url = '/'.join([git_api_base, user, repo, "git/trees", sha])
    result = requests.get(url)
    data = json.loads(result.text)
    if "API rate limit exceeded" not in data and "{\"message\":\"Not Found\"" not in data:
        with open('size.json', 'w') as json_file:
            json.dump(data, json_file)
    if "API rate limit exceeded" in data or "{\"message\":\"Not Found\"" in data:
        with open('size.json', 'r') as file:
            lines = file.readlines()
            # data = json.loads(lines)
        total_size = 0
        data = json.loads(lines[0])
        print(data['tree'][0]['size'])
        print(data)
        for i in data['tree']:
            total_size += i['size']
    else:
        data = json.loads(result.text)
        total_size = 0
        for i in data['tree']:
            total_size += i['size']
    return total_size


def repo_size(user: str, repo: str):
    data_points = []
    for day in range(20, 31):
        time = "2021-04-" + str(day) + "T00:00:00Z"
        commit_sha = get_commit_sha(user=user, repo=repo, until_time=time)
        data_points.append(get_size(user=user, repo=repo, sha=commit_sha))
    if len(data_points):
        plot(data_points=data_points, output_file="images/repo_size")
    return data_points


repo_size(user="Landaluce", repo="sparkbadge")
