import json
import logging

from flask import request
from flask import jsonify

from routes import app

logger = logging.getLogger(__name__)

def check_efficiency(monsters, wave, attackable, force_rest):
    # last wave
    if wave == len(monsters) - 1:
        if attackable: 
            return monsters[wave]
        else:
            return 0
    else:
        rest_efficiency = check_efficiency(monsters, wave + 1, attackable, False)
        if force_rest:
            return rest_efficiency

        if attackable:
            attack_efficiency = monsters[wave] * 1 + check_efficiency(monsters, wave + 1, False, True)
        else:
            attack_efficiency = 0

        prepare_efficiency = monsters[wave] * -1 + check_efficiency(monsters, wave + 1, True, False)

        return max(rest_efficiency, attack_efficiency, prepare_efficiency)

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def hunter_kazuma():
    datas = request.get_json()
    logging.info("data sent for evaluation {}".format(datas))

    efficiency = [{"efficiency": check_efficiency(data["monsters"], 0, False, False)} for data in datas]

    logging.info("My result :{}".format(efficiency))
    return jsonify(efficiency), 200
