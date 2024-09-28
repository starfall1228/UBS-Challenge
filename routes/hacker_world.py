import json
import logging

from flask import request, jsonify

from routes import app
import requests
logger = logging.getLogger(__name__)

@app.route('/coolcodehack', methods=['POST'])
def coolcodehack():
    # response = {
    #     'username': '123456777',  # Replace with your actual username
    #     'password': 'Abcd!234'   # Replace with your actual password
    # }
    # # # Send a POST request to the external API
    # # url = 'https://api.crazy-collectors.com/coolcode/api/assignment/score'
    # # payload = {
    # #     'username': 'sJH1Fe',  # Replace with the actual username
    # #     'assignmentId': 3,             # Replace with the actual assignment ID
    # #     'score': 100                     # Replace with the desired score
    # # }
    # # api_response = requests.post(url, json=payload)

    # # # Print the response from the external API
    # # print(api_response.status_code)
    # # print(api_response.json())
    # response = {"response": "Hello, World!"}
    # return jsonify(response)
    # return jsonify(response)
    response = {
        'username': '123456777',  # Replace with your actual username
        'password': 'Abcd!234'   # Replace with your actual password
    }

    # Send a POST request to the external API to check the score
    login_url = 'https://api.crazy-collectors.com/coolcode/api/auth/signin'
    login_payload = {
        'username': '123456777',  # Replace with your actual username
        'password': 'Abcd!234'   # Replace with your actual password
    }

    # Send the login request
    login_response = requests.post(login_url, json=login_payload)

    # Check if login was successful
    if login_response.status_code == 200:


        # Define the score check URL and headers
        score_url = 'https://api.crazy-collectors.com/coolcode/api/assignment/score'
        # Define the payload to check the score
        score_payload =	{"username": {"sJH1Fe"},
            "assignmentId": {3},
            "score": {100}}

        # Send the request to check the score
        score_response = requests.post(score_url, json=score_payload)

        # Print the response from the external API
        if score_response.status_code == 200:
            print('Score:', score_response.json().get('score'))
        else:
            print('Failed to check score:', score_response.status_code, score_response.text)
    else:
        print('Login failed:', login_response.status_code, login_response.text)

    return jsonify(response)