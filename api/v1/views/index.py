#!/usr/bin/python3
"""is the index for app api"""
from api_v1.views import app_views

@app_views.route('/status', strict_slashes=False, defaults={'status': "OK"} )
