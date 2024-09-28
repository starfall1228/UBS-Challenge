import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/coolcodehack', methods=['POST'])
def coolcodehack():
    response = {
        'username': '123456777',  # Replace with your actual username
        'password': 'Abcd!234'   # Replace with your actual password
    }
    return jsonify(response)