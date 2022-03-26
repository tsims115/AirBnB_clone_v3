#!/usr/bin/python3
"""is the index for app api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ returns dictionary containing status """
    return jsonify({'status': "OK"})
