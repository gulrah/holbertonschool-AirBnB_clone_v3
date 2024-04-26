#!/usr/bin/python3
"""
This script defines a Flask API to retrieve city data by city ID.
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Retrieve city data by city ID.

    Args:
        city_id (str): The unique identifier of the city.

    Returns:
        JSON: A JSON response containing the city data.
    """
    city_data = {
        "__class__": "City",
        "id": city_id,
        "name": "New Orleans",
        "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
        "created_at": "2017-03-25T02:17:06",
        "updated_at": "2017-03-25T02:17:06"
    }
    return jsonify(city_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
