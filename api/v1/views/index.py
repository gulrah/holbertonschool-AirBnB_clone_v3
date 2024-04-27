#!/usr/bin/python3
"""Script"""

from flask import jsonify

from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON with status 'OK'."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieves the number of each object by type."""
    stats = {}
    classes = storage.classes
    for key, value in classes.items():
        stats[key] = storage.count(value)
        return jsonify(stats)
