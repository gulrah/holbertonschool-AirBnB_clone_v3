#!/usr/bin/python3
"""
Handles RESTful API actions for City objects.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on City objects through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id (str): The ID of the State for which to retrieve cities.

    Returns:
        JSON response containing a list of dictionaries, each representing a City object
        belonging to the specified State. If the State with the given ID does not exist,
        returns HTTP status code 404.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    
    
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a specific City object.

    Args:
        city_id (str): The ID of the City to retrieve.

    Returns:
        JSON response containing the dictionary representation of the City object.
        If the City with the given ID does not exist, returns HTTP status code 404.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        return jsonify(city.to_dict())
    
    
@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object.

    Args:
        state_id (str): The ID of the State under which to create the City.

    Returns:
        JSON response containing the dictionary representation of the newly created City object.
        If the State with the given ID does not exist, or the request does not contain valid JSON data,
        or the required 'name' field is missing, returns HTTP status code 404 or 400 respectively.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            if 'name' not in data:
                abort(400, 'Missing name')
                data['state_id'] = state_id
                new_city = City(**data)
                new_city.save()
                return jsonify(new_city.to_dict()), 201
            
            
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates an existing City object.
    
    Args:
        city_id (str): The ID of the City to update.

    Returns:
        JSON response containing the dictionary representation of the updated City object.
        If the City with the given ID does not exist, or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(city, key, value)
                    city.save()
                    return jsonify(city.to_dict())
                
            
@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes an existing City object.
    
    Args:
        city_id (str): The ID of the City to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the City with the given ID does not exist, returns HTTP status code 404.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        city.delete()
        storage.save()
        return jsonify({}), 200
