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

    # generate image for badge
    qc = QuickChart()
    qc.width = 75
    qc.height = 25
    #qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "sparkline",
        "data": {
            "datasets": [{
                "data": random.sample(range(10, 30), 10)
            }]
        }
    }
    badge = requests.get(qc.get_short_url()).content

    # serve image with suitable cache control headers
    res = make_response(badge)
    res.headers.set('Content-Type', 'image/png')
    res.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    res.headers.set('Pragma', 'no-cache')
    res.headers.set('Expires', '0')
    return res
