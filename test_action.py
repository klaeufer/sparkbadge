#!/usr/bin/env python

# The following script is meant to test gh actions.
# Creates a randomly-colored badge, which is added to .sparkbadge/

import os
import random
from os.path import join, dirname
from pybadges import badge

colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown']

color = random.choice(colors)

test_badge = badge(left_text='coverage', right_text='23%', right_color=color)

spark_dir = join(dirname(__file__), '.sparkbadge')
file_name = join(dirname(__file__), '.sparkbadge/test_badge.svg')

if not os.path.exists(spark_dir):
    os.makedirs(spark_dir)

with open(file_name, 'w') as f:
    f.write(test_badge)
