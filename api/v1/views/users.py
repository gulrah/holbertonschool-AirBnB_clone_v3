#!/usr/bin/python3
"""
Handles RESTful API actions for User objects.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on User objects through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        JSON response containing a list of dictionaries, each representing a User object.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a specific User object.

    Args:
        user_id (str): The ID of the User to retrieve.

    Returns:
        JSON response containing the dictionary representation of the User object.
        If the User with the given ID does not exist, returns HTTP status code 404.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
        return jsonify(user.to_dict())
    
    
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object.

    Returns:
        JSON response containing the dictionary representation of the newly created User object.
        If the request does not contain valid JSON data or the required 'email' or 'password' field is missing,
        returns HTTP status code 400.
    """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
            if 'password' not in data:
                abort(400, 'Missing password')
                new_user = User(**data)
                new_user.save()
                return jsonify(new_user.to_dict()), 201
            
            
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing User object.
    
    Args:
        user_id (str): The ID of the User to update.

    Returns:
        JSON response containing the dictionary representation of the updated User object.
        If the User with the given ID does not exist or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'email', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(user, key, value)
                    user.save()
                    return jsonify(user.to_dict())
                
                
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes an existing User object.
    
    Args:
        user_id (str): The ID of the User to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the User with the given ID does not exist, returns HTTP status code 404.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
        user.delete()
        storage.save()
        return jsonify({}), 200
