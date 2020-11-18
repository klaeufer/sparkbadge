#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

from flask import redirect, make_response
from quickchart import QuickChart
import requests
import random

@app.route('/')
def hello():
    return "Hello and welcome to SparkBadge!"

@app.route('/random')
def sparkline_random():

    qc = QuickChart()
    qc.width = 50
    qc.height = 25
    #qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "sparkline",
        "data": {
            "datasets": [{
                "data": random.sample(range(10, 30), 5)
            }]
        }
    }

    req = requests.get(qc.get_short_url())
    res = make_response(req.content)
    res.headers.set('Content-Type', 'image/png')
    res.headers.set('Cache-Control', 'no-cache')

    return res
