#!/usr/bin/python3
"""Script"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "OK"})
