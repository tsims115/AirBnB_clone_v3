#!/usr/bin/python3
"""sets up our api for state objs"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def reviews(place_id=None):
    """returns all review objs"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        reviewList = []
        for review in place.reviews:
            review = review.to_dict()
            reviewList.append(review)
        return jsonify(reviewList)


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def singleReview(review_id=None):
    """ returns specified review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteReview(review_id=None):
    """deletes specified review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def postReview(place_id=None):
    """creates new review objs"""
    newData = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if newData is None:
        abort(400, "Not a JSON")
    if 'user_id' not in newData.keys():
        abort(400, "Missing user_id")
    else:
        user = storage.get(User, newData['user_id'])
        if user is None:
            abort(404)
    if 'text' not in newData.keys():
        abort(400, "Missing text")
    newReview = Review(**newData)
    newReview.place_id = place_id
    newReview.save()
    return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'PUT'])
def putReview(review_id=None):
    """updates existing specified review obj"""
    newData = request.get_json(silent=True)
    if newData is None:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        ignoreList = ['id', 'user_id', 'place_id' 'created_at', 'updated_at']
        for attr, value in newData.items():
            if attr not in ignoreList:
                setattr(review, attr, value)
                review.save()
        return jsonify(review.to_dict()), 200
