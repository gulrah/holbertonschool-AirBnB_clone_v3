#!/usr/bin/python3
"""
Handles RESTful API actions for Place objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    
    
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        return jsonify(place.to_dict())
    
    
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
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
                        new_place = Place(**data)
                        new_place.save()
                        return jsonify(new_place.to_dict()), 201
                    
                    
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
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
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        place.delete()
        storage.save()
        return jsonify({}), 200
