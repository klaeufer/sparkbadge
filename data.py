#!/usr/bin/env python3

import requests
import random
import json

def sample():
    return random.sample(range(10, 30), 10)

travis_base = "https://api.travis-ci.org/repos/"
travis_status_map = {None: -1, 0: 0}

def travis(user, repo):
    url = travis_base + user + "/" + repo + "/builds"
    res = requests.get(url)
    data = json.loads(res.text)
    return [travis_status_map[s['result']] for s in data]
