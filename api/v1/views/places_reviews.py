#!/usr/bin/python3
"""
Handles RESTful API actions for Review objects related to Place.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on Review objects related to Place through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.

    Args:
        place_id (str): The ID of the Place for which to retrieve reviews.

    Returns:
        JSON response containing a list of dictionaries, each representing a Review object
        related to the specified Place. If the Place with the given ID does not exist,
        returns HTTP status code 404.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    
    
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific Review object.
    
    Args:
        review_id (str): The ID of the Review to retrieve.

    Returns:
        JSON response containing the dictionary representation of the Review object.
        If the Review with the given ID does not exist, returns HTTP status code 404.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        return jsonify(review.to_dict())
    
    
@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object related to a Place.
    
    Args:
        place_id (str): The ID of the Place for which to create the Review.

    Returns:
        JSON response containing the dictionary representation of the newly created Review object.
        If the Place with the given ID does not exist, or the request does not contain valid JSON data,
        or the required 'user_id' or 'text' field is missing, or the specified user does not exist,
        returns HTTP status code 404 or 400 respectively.
    """
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
                        data['place_id'] = place_id
                        new_review = Review(**data)
                        new_review.save()
                        return jsonify(new_review.to_dict()), 201
                
                    
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an existing Review object.

    Args:
        review_id (str): The ID of the Review to update.

    Returns:
        JSON response containing the dictionary representation of the updated Review object.
        If the Review with the given ID does not exist, or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
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
    """
    Deletes an existing Review object.

    Args:
        review_id (str): The ID of the Review to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the Review with the given ID does not exist, returns HTTP status code 404.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        review.delete()
        storage.save()
        return jsonify({}), 200
