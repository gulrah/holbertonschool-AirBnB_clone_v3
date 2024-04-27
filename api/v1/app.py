#!/usr/bin/python3
""" App Module """


from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

@app.errorhandler(NotFound)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
