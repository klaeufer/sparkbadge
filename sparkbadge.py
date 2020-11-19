#!/usr/bin/env python3

from flask import Flask, make_response
from actions import sparkline_random

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello and welcome to SparkBadge! <a href="/random">Try this.</a>'

@app.route('/random')
def random():
    return sparkline_random()
