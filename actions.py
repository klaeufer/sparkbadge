#!/usr/bin/env python3

from flask import make_response
from quickchart import QuickChart
import requests
import random

def sparkline(data):
    # generate image for badge
    qc = QuickChart()
    qc.width = 75
    qc.height = 25
    #qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "sparkline",
        "data": {
            "datasets": [{
                "data": data
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

def sparkline_random():
    return sparkline(random.sample(range(10, 30), 10))
