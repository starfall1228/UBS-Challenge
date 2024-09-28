import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/lab_work', methods=['POST'])
def lab_work():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    # for i in range(len(data)):
        # board = data[i]["board"]
        # moves = data[i]["moves"]
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)