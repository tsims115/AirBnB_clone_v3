#!/usr/bin/python3
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def cities_by_state(state_id=None):
    """returns all city objs based on state obj"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        cityList = []
        for city in state.cities:
            cityList.append(city.to_dict())
        return jsonify(cityList)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def singleCity(city_id=None):
    """returns all city obj with given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteCity(city_id=None):
    """deletes specified city obj"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def postCity(state_id=None):
    """creates new city obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    if 'name' in newData.keys():
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        newCity = City(**newData)
        newCity.state_id = state_id
        newCity.save()
        return jsonify(newCity.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putCity(city_id=None):
    """updates existing specified city obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    attrList = ['id', 'state_id', 'created_at', 'updated_at']
    for attr, value in newData.items():
        if attr not in attrList:
            setattr(city, attr, value)
            city.save()
    return jsonify(city.to_dict()), 200
