import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def get_number(target):
    negative = 1
    value = 0
    result_multiple = 10
    value_multiple = 1
    value_current_multiple = 1
    for i in range(0, len(target)):
        if target[i] == '.':
            result_multiple = 1
            value_multiple = 0.1
        elif target[i] == '-':
            negative = -1
        elif target[i] <= '9' and target[i] >= '0':
            value *= result_multiple
            value_current_multiple *= value_multiple
            value += int(target[i]) * value_current_multiple
        else:
            break
    return value*negative

def weight_of_colony(colony):
    colony_list = []
    sum = 0
    for i in range(len(colony)):
        colony_list.append(get_number(colony[i]))

    for i in range(len(colony_list)):
        sum += colony_list[i]
    return sum

def signature_of_pair(first, second):
    if first > second:
        return first - second
    elif first < second:
        return 10 - (second - first)
    return 0

def new_digit_by_pair(signature, weight):
    return (weight + signature)%10

def colony_of_next_generation(colony):
    colony_list = []
    new_colony_list = []
    result_list = ""
    for i in range(len(colony)):
        colony_list.append(get_number(colony[i]))
    print (colony_list)
    for i in range(len(colony_list) -1 ):
        new_colony_list.append(new_digit_by_pair(signature_of_pair(colony_list[i], colony_list[(i+1)%len(colony_list)]), weight_of_colony(colony)))
    
    colony_list_index = 0
    new_colony_list_index = 0

    for i in range(len(colony_list)+ len(new_colony_list)):
        if (i % 2 == 0):
            result_list+= str(colony_list[colony_list_index])
            colony_list_index += 1
        else :
            result_list+= str(new_colony_list[new_colony_list_index])
            new_colony_list_index += 1
        i+=1

    return result_list

def colony_of_nth_generation(colony, n):
    if n == 0:
        return colony
    return colony_of_nth_generation(colony_of_next_generation(colony), n-1)


@app.route('/digital-colony', methods=['POST'])
def Klotski():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for i in range(len(data)):
        generation = data[i]["generation"]
        colony = data[i]["colony"]
        result.append(colony_of_nth_generation(colony, generation))
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)