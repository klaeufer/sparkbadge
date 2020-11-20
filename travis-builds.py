#!/usr/bin/env python3

# Travis API doc
# https://docs.travis-ci.com/api/?http#builds

import sys
import data

user = sys.argv[1]
repo = sys.argv[2]

print(data.travis(user, repo))
