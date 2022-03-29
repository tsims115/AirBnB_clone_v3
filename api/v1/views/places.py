#!/usr/bin/python3
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def places(city_id=None):
    """returns all places objs"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        allPlace = storage.all(Place)
        places = []
        for place in allPlace.values():
            place = place.to_dict()
            if place['city_id'] == city_id:
                places.append(place)
        return jsonify(places)
        """placeList = []
        for place in city.places:
            place = place.to_dict()
            placeList.append(place)
        return jsonify(placeList)"""


@app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['GET'])
def singlePlace(place_id=None):
    """ returns specified place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def deletePlace(place_id=None):
    """deletes specified place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def postPlace(city_id=None):
    """creates new place objs"""
    newData = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if newData is None:
        abort(400, "Not a JSON")
    if 'user_id' not in newData.keys():
        abort(400, "Missing user_id")
    else:
        user = storage.get(User, newData['user_id'])
        if user is None:
            abort(404)
    if 'name' not in newData.keys():
        abort(400, "Missing name")
    newPlace = Place(**newData)
    newPlace.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putPlace(place_id=None):
    """updates existing specified place obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        ignoreList = ['id', 'user_id', 'city_id' 'created_at', 'updated_at']
        for attr, value in newData.items():
            if attr not in ignoreList:
                setattr(place, attr, value)
                place.save()
        return jsonify(place.to_dict()), 200
