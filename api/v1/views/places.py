#!/usr/bin/python3
"""
Handles RESTful API actions for Place objects.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on Place objects through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.

    Args:
        city_id (str): The ID of the City for which to retrieve places.

    Returns:
        JSON response containing a list of dictionaries, each representing a Place object
        belonging to the specified City. If the City with the given ID does not exist,
        returns HTTP status code 404.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    
    
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific Place object.
    
    Args:
        place_id (str): The ID of the Place to retrieve.

    Returns:
        JSON response containing the dictionary representation of the Place object.
        If the Place with the given ID does not exist, returns HTTP status code 404.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object.
    
    Args:
        city_id (str): The ID of the City under which to create the Place.

    Returns:
        JSON response containing the dictionary representation of the newly created Place object.
        If the City with the given ID does not exist, or the request does not contain valid JSON data,
        or the required 'user_id' or 'name' field is missing, or the specified user does not exist,
        returns HTTP status code 404 or 400 respectively.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            if 'user_id' not in data:
                abort(400, 'Missing user_id')
                if 'name' not in data:
                    abort(400, 'Missing name')
                    if storage.get(User, data['user_id']) is None:
                        abort(404)
                        data['city_id'] = city_id
                        new_place = Place(**data)
                        new_place.save()
                        return jsonify(new_place.to_dict()), 201
                    
                    
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates an existing Place object.

    Args:
        place_id (str): The ID of the Place to update.

    Returns:
        JSON response containing the dictionary representation of the updated Place object.
        If the Place with the given ID does not exist, or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(place, key, value)
                    place.save()
                    return jsonify(place.to_dict())
                
                
@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes an existing Place object.
    
    Args:
        place_id (str): The ID of the Place to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the Place with the given ID does not exist, returns HTTP status code 404.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        place.delete()
        storage.save()
        return jsonify({}), 200
