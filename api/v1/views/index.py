#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views
from models import storage

# Route for stats endpoint
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of each object by type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stats = {cls: storage.count(class_name) for cls, class_name in classes.items()}
    return jsonify(stats)
