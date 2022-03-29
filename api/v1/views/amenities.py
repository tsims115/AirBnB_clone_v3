#!/usr/bin/python3
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    """returns all amenities objs"""
    amenityList = list(storage.all(Amenity).values())
    newList = []
    for amenity in amenityList:
        amenity = amenity.to_dict()
        newList.append(amenity)
    return jsonify(newList)


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def singleAmenity(amenity_id=None):
    """ returns specified amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteAmenity(amenity_id=None):
    """deletes specified amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def postAmenity():
    """creates new amenity objs"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    if 'name' in newData.keys():
        newAmenity = Amenity(**newData)
        newAmenity.save()
        return jsonify(newAmenity.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putAmenity(amenity_id=None):
    """updates existing specified amenity obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        for attr, value in newData.items():
            if attr != 'id' and attr != 'created_at' and attr != 'updated_at':
                setattr(amenity, attr, value)
                amenity.save()
        return jsonify(amenity.to_dict()), 200
