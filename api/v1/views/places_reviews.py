#!/usr/bin/python3
""" Reviews RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    list = []
    for review in reviews:
        list.append(review.to_dict())
    return jsonify(list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    user_id = data.get("user_id")
    text = data.get("text")
    if user_id is None:
        abort(400, "Missing user_id")
    if text is None:
        abort(400, "Missing text")
    if storage.get("Place", place_id) is None:
        abort(404)
    if storage.get("User", user_id) is None:
        abort(404)

    new_review = Review()
    new_review.place_id = place_id
    new_review.user_id = user_id
    new_review.text = text
    new_review.save()
    return (jsonify(new_review.to_dict())), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return (jsonify(review.to_dict()))
