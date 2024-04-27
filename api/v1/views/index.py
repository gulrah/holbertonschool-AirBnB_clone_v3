#!/usr/bin/python3
"""Script"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def api_status():
    response = jsonify({"status": "OK"})
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    return response

@app_views.route('/stats', methods=['GET'])
def get_stats():
    counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(counts)
