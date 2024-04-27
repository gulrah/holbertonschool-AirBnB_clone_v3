#!/usr/bin/python3
"""
Handles RESTful API actions for State objects.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on State objects through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON response containing a list of dictionaries, each representing a State object.
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a specific State object.

    Args:
        state_id (str): The ID of the State to retrieve.

    Returns:
        JSON response containing the dictionary representation of the State object.
        If the State with the given ID does not exist, returns HTTP status code 404.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        return jsonify(state.to_dict())
    
    
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.

    Returns:
        JSON response containing the dictionary representation of the newly created State object.
        If the request does not contain valid JSON data or the required 'name' field is missing,
        returns HTTP status code 400.
    """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
            new_state = State(**data)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        
        
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates an existing State object.
    
    Args:
        state_id (str): The ID of the State to update.

    Returns:
        JSON response containing the dictionary representation of the updated State object.
        If the State with the given ID does not exist or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(state, key, value)
                    state.save()
                    return jsonify(state.to_dict())
                
                
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes an existing State object.
    
    Args:
        state_id (str): The ID of the State to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the State with the given ID does not exist, returns HTTP status code 404.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        state.delete()
        storage.save()
        return jsonify({}), 200
