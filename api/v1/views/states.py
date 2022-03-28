#!/usr/bin/python
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """returns all state objs"""
    stateList = list(storage.all(State).values())
    newList = []
    for state in stateList:
        state = state.to_dict()
        newList.append(state)
    return jsonify(newList)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def singleState(state_id=None):
    """ returns specified state obj"""
    allStates = storage.all()
    if 'State.' + state_id in allStates:
        return jsonify(allStates['State.' + state_id].to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteState(state_id=None):
    """deletes specified state obj"""
    allStates = storage.all(State)
    if 'State.' + state_id in allStates:
        storage.delete(allStates['State.' + state_id])
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def postState():
    """creates new state objs"""
    newData = request.get_json()
    if 'name' in newData.keys():
        newState = State(**newData)
        newState.save()
        return jsonify(newState.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putState(state_id=None):
    """updates existing specified state obj"""
    allStates = storage.all(State)
    newData = request.get_json()
    if 'State.' + state_id in allStates:
        workingState = allStates['State.' + state_id]
        for attr, value in newData.items():
            if attr != 'id' and attr != 'created_at' and attr != 'updated_at':
                setattr(workingState, attr, value)
                workingState.save()
        return jsonify(workingState.to_dict()), 200
    else:
        abort(404)
