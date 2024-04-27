#!/usr/bin/python3
"""
Handles RESTful API actions for Amenity objects.

This module provides endpoints to perform CRUD (Create, Read, Update, Delete)
operations on Amenity objects through a RESTful API.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        JSON response containing a list of dictionaries, each representing an Amenity object.
    """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a specific Amenity object.
                
    Args:
        amenity_id (str): The ID of the Amenity to retrieve.
    
    Returns:
        JSON response containing the dictionary representation of the Amenity object.
        If the Amenity with the given ID does not exist, returns HTTP status code 404.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
        return jsonify(amenity.to_dict())
    
    
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.

    Returns:
        JSON response containing the dictionary representation of the newly created Amenity object.
        If the request does not contain valid JSON data or the required 'name' field is missing,
        returns HTTP status code 400.
    """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
            new_amenity = Amenity(**data)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
    

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an existing Amenity object.
    
    Args:
        amenity_id (str): The ID of the Amenity to update.

    Returns:
        JSON response containing the dictionary representation of the updated Amenity object.
        If the Amenity with the given ID does not exist or the request does not contain valid JSON data,
        returns HTTP status code 404 or 400 respectively.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(amenity, key, value)
                    amenity.save()
                    return jsonify(amenity.to_dict())
                
            
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an existing Amenity object.

    Args:
        amenity_id (str): The ID of the Amenity to delete.

    Returns:
        Empty JSON response with HTTP status code 200 if successful.
        If the Amenity with the given ID does not exist, returns HTTP status code 404.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
