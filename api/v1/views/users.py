#!/usr/bin/python3
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
    """returns all users objs"""
    userList = list(storage.all(User).values())
    newList = []
    for user in userList:
        user = user.to_dict()
        newList.append(user)
    return jsonify(newList)


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['GET'])
def singleUser(user_id=None):
    """ returns specified user obj"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteUser(user_id=None):
    """deletes specified user obj"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def postUser():
    """creates new user objs"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    if 'email' not in newData.keys():
        abort(400, "Missing email")
    if 'password' not in newData.keys():
        abort(400, "Missing password")
    newUser = User(**newData)
    newUser.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putUser(user_id=None):
    """updates existing specified user obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        ignoreList = ['id', 'email', 'created_at', 'updated_at']
        for attr, value in newData.items():
            if attr not in ignoreList:
                setattr(user, attr, value)
                user.save()
        return jsonify(user.to_dict()), 200
