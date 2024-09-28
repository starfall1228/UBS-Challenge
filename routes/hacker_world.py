import json
import logging

from flask import request, jsonify

from routes import app
import requests
logger = logging.getLogger(__name__)

@app.route('/coolcodehack', methods=['POST'])
def coolcodehack():
    response = {
        'username': '123456777',  # Replace with your actual username
        'password': 'Abcd!234'   # Replace with your actual password
    }
    # Send a POST request to the external API
    url = 'https://api.crazy-collectors.com/coolcode/api/assignment/score'
    payload = {
        'username': 'sJH1Fe',  # Replace with the actual username
        'assignmentId': 123,             # Replace with the actual assignment ID
        'score': 100                     # Replace with the desired score
    }
    api_response = requests.post(url, json=payload)

    # Print the response from the external API
    print(api_response.status_code)
    print(api_response.json())

    return jsonify(response)
    # return jsonify(response)