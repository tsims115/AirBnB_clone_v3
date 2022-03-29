#!/usr/bin/python3
""" setting up the first endpoint to return status of API """
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """404 not found default error"""
    return jsonify({'error': 'Not found'}), 404


"""@app.errorhandler(400)
def invalid_route(e):
    if type(e.description) is dict:
        return jsonify(e.description), 400
    else:
        return jsonify({'error': 'Not a JSON'}), 400
"""

if __name__ == '__main__':
    host = "0.0.0.0"
    port = '5000'
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
