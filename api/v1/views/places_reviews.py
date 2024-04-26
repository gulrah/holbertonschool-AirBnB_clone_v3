#!/usr/bin/python3
"""
Handles RESTful API actions for Review objects related to Place.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    
    
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        return jsonify(review.to_dict())
    
    
@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            if 'user_id' not in data:
                abort(400, 'Missing user_id')
                if 'text' not in data:
                    abort(400, 'Missing text')
                    if storage.get(User, data['user_id']) is None:
                        abort(404)
                        new_review = Review(**data)
                        new_review.save()
                        return jsonify(new_review.to_dict()), 201
                    
                    
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(review, key, value)
                    review.save()
                    return jsonify(review.to_dict())
                
                
@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        review.delete()
        storage.save()
        return jsonify({}), 200
