#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

from flask import redirect
from quickchart import QuickChart

@app.route('/')
def hello():
    return "Hello and welcome to SparkBadge!"

@app.route('/<int:z>/<int:x>/<int:y>')
def quickchart_proxy(x, y, z):
    qc = QuickChart()
    qc.width = 100
    qc.height = 50
    #qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "sparkline",
        "data": {
            "datasets": [{
                "label": "Foo",
                "data": [x, y, z]
            }]
        }
    }
    return redirect(qc.get_url())
