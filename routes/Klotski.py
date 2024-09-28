import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def map_generation(input):
    game_map = []
    row = []
    input_index = 0
    for j in range(5):
        for k in range(4):
            row.append(input[input_index])
            input_index+=1
            k+=1
        game_map.append(row)
        row = []
        j+=1
    return game_map

def translate_instruction(instruction):
    instruction_list = []
    temp_instruction_row = []
    i = 0

    while (i < len(instruction)):
        temp_instruction_row.append(instruction[i])
        temp_instruction_row.append(instruction[i+1])
        # print(temp_instruction_row)
        i+=2
        instruction_list.append(temp_instruction_row)
        temp_instruction_row = []
    return instruction_list

def move_block(map, instruction_list):
    for i in range(len(instruction_list)):
        # print(instruction_list[i][0])
        # print(instruction_list[i][1])

        target = instruction_list[i][0]
        direction = instruction_list[i][1]

        if direction == 'N':
            for j in range(len(map)):
                for k in range(len(map[j])):
                    if map[j][k] == target:
                        if map[j-1][k] == '@':
                            map[j-1][k] = target
                            map[j][k] = '@'
        elif direction == 'E':
            for j in range(len(map)):
                for k in range(len(map[j]) - 1, -1, -1):
                    if  map[j][k] == target:
                        if  map[j][k+1] == '@':
                            map[j][k+1] = target
                            map[j][k] = '@'
        elif direction == 'S':
            for j in range(len(map) - 1, -1, -1):
                for k in range(len(map[j])):
                    if  map[j][k] == target:
                        if  map[j+1][k] == '@':
                            map[j+1][k] = target
                            map[j][k] = '@'
        elif direction == 'W':
            for j in range(len(map)):
                for k in range(len(map[j])):
                    if map[j][k] == target:
                        if  map[j][k-1] == '@':
                            map[j][k-1] = target
                            map[j][k] = '@'
    return map

def convert_map_to_string(map):
    result = ""
    for i in range(len(map)):
        for j in range(len(map[i])):
            result += map[i][j]
    return result


@app.route('/klotski', methods=['POST'])
def Klotski():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    board = data[0]["board"]
    moves = data[0]["moves"]

    result = convert_map_to_string(move_block(map_generation(board),translate_instruction(moves)))
    logging.info("My result :{}".format(result))
    return json.dumps(result)