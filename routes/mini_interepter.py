import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

public_var = {}
terminal = []

# format: "[type, value]"
def get_string(target, start):
    value = ""
    for i in range(start, len(target)):
        if target[i] != '"':
            value += target[i]
        else:
            break
    return i, ['s', value]

def get_number(target, start):
    negative = 1
    value = 0
    result_multiple = 10
    value_multiple = 1
    value_current_multiple = 1
    for i in range(start, len(target)):
        if target[i] == '.':
            result_multiple = 1
            value_multiple = 0.1
        elif target[i] == '-':
            negative = -1
        elif target[i] >= '0' and target[i] <= '9':
            value *= result_multiple
            value_current_multiple *= value_multiple
            value += int(target[i]) * value_current_multiple
        else:
            break
    return i, ['n', value * negative]

def check_str(string, start, target):
    if (len(string) - start < len(target)): return start, False

    temp = start
    for i in range(len(target)):
        if string[temp] != target[i]:
            return -1, False
        temp += 1
    return temp, True

def check_var(string, start):
    global public_var
    temp_name = ""
    for i in range(start, len(string)):
        if not ((string[i] >= 'a' and string[i] <= 'z' ) or (string[i] >= "A" and string[i] <= 'Z')): break
        temp_name += string[i]
    if (public_var[temp_name]):
        return i, public_var[temp_name]
    else:
        return i, ['v', temp_name]
    

def put_instruction(var):
    if (var[0] != 's'): return -1, ['u', None]
    global terminal
    terminal.append(var[1])
    return 1, ['u', None]
    
def make_var(var_name, value):
    global public_var
    if (var_name[0] != 'v'): return -1, ['u', None]
    if (value[0] == 'v'): return -1, ['u', None]

    public_var[var_name[1]] = value
    return 1, ['u', None]

def concat(str1, str2):
    if (str1[0] != 's'): return -1, ['u', None]
    if (str2[0] != 's'): return -1, ['u', None]

    return 1, ['s', str1[1] + str2[1]]

def lowercase(str):
    if (str[0] != 's'): return -1, ['u', None]

    return 1, ['s', str.lower()]

def uppercase(str):
    if (str[0] != 's'): return -1, ['u', None]

    return 1, ['s', str.upper()]

def substring_replace(src, target, replace):
    if (src[0] != 's'): return -1, ['u', None]
    if (target[0] != 's'): return -1, ['u', None]
    if (replace[0] != 's'): return -1, ['u', None]

    return 1, ['s', src[1].replace(target[1], replace[1])]

def get_substring(str1, start, end):
    if (str1[0] != 's'): return -1, ['u', None]
    if (start[0] != 'n'): return -1, ['u', None]
    if (end[0] != 'n'): return -1, ['u', None]

    if not (isinstance(start[1], int)): return -1, ['u', None]
    if not (isinstance(end[1], int)): return -1, ['u', None]

    if (len(str1[1]) > end or start < 0): return -1, ['u', None]

    return 1, ['s', str1[1][start:end]]

def add_value(params):
    sum = 0
    for nums in params:
        if (nums[0] != 'n'): return -1, ['u', None]
        sum += nums[1]

    return 1, ['n', sum]

def sub_value(num1, num2):
    if (num1[0] != 'n'): return -1, ['u', None]
    if (num2[0] != 'n'): return -1, ['u', None]

    return 1, ['n', num1[1] - num2[1]]
    
def mul_value(params):
    product = 1
    for nums in params:
        if (nums[0] != 'n'): return -1, ['u', None]
        product *= nums[1]

    return 1, ['n', product]

def div_value(num1, num2):
    if (num1[0] != 'n'): return -1, ['u', None]
    if (num2[0] != 'n'): return -1, ['u', None]

    return 1, ['n', num1[1] / num2[1]]

def abs_value(num):
    if (num[0] != 'n'): return -1, ['u', None]

    return 1, ['n', abs(num)]

def max_value(params):
    maximum = params[0]
    for nums in params:
        if (nums[0] != 'n'): return -1, ['u', None]
        if (nums[1] > maximum): maximum = nums[1]

    return 1, ['n', maximum]

def min_value(params):
    minimum = params[0]
    for nums in params:
        if (nums[0] != 'n'): return -1, ['u', None]
        if (nums[1] < minimum): minimum = nums[1]

    return 1, ['n', minimum]

def greater_value(num1, num2):
    if (num1[0] != 'n'): return -1, ['u', None]
    if (num2[0] != 'n'): return -1, ['u', None]

    return 1, ['b', num1[1] > num2[1]]

def lower_value(num1, num2):
    if (num1[0] != 'n'): return -1, ['u', None]
    if (num2[0] != 'n'): return -1, ['u', None]

    return 1, ['b', num1[1] < num2[1]]

def equal(val1, val2):
    if (val1[0] == 'v'): return -1, ['u', None]
    if (val2[0] == 'v'): return -1, ['u', None]

    return 1, ['b', val1[0] == val2[0] and val1[1] == val2[1]]

def notequal(val1, val2):
    if (val1[0] == 'v'): return -1, ['u', None]
    if (val2[0] == 'v'): return -1, ['u', None]

    return 1, ['b', val1[0] != val2[0] or val1[1] != val2[1]]

def convert_string(val):
    if val[0] == 's':
        return 1, val
    elif val[0] == 'b':
        if (val[1]):
            return 1, ['s', "true"]
        else:
            return 1, ['s', "false"]
    elif val[0] == 'u':
        return 1, ['s', "null"]
    elif val[0] == 'n':
        return 1, ['s', str(val[1])]
    else:
        return -1, ['u', None]

def decode_instructions(instruction, start):
    types = ""
    params = []
    temp_param = None
    char_i = start
    while char_i < len(instruction):
        if (instruction[char_i] >= 'a' and instruction[char_i] <= 'z' ) or (instruction[char_i] >= "A" and instruction[char_i] <= 'Z'):
            types += instruction[char_i]
        else:
            break
        char_i += 1

    while char_i < len(instruction):
        if instruction[char_i] == '(':
            char_i, temp_param = decode_instructions(instruction, char_i + 1)
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
            continue
        elif instruction[char_i] == '"':
            char_i, temp_param = get_string(instruction, char_i + 1)
            if instruction[char_i] != '"': return -1, ['u', None]
            char_i += 1
            continue
        elif (instruction[char_i] >= '0' and instruction[char_i] <= '9') or instruction[char_i] == '-':
            char_i, temp_param = get_number(instruction, char_i)
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
            continue
        elif instruction[char_i] == 'n':
            char_i, result = check_str(instruction, char_i, "null")
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
            if result: temp_param = ['u', None]
        elif instruction[char_i] == 't':
            char_i, result = check_str(instruction, char_i, "true")
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
            if result: temp_param = ['b', True]
        elif instruction[char_i] == 'f':
            char_i, result = check_str(instruction, char_i, "false")
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
            if result: temp_param = ['b', False]
        elif instruction[char_i] == ' ':
            if (temp_param): params.append(temp_param)
            temp_param = None
            char_i += 1
            continue
        elif instruction[char_i] == ')':
            if (temp_param): params.append(temp_param)
            temp_param = None

            if (types == "puts"):
                if len(params) != 1: return -1, ['u', None]
                error_code, results = put_instruction(params[0])
            elif (types == "set"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = make_var(params[0], params[1])
            elif (types == "concat"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = concat(params[0], params[1])
            elif (types == "lowercase"):
                if len(params) != 1: return -1, ['u', None]
                error_code, results = lowercase(params[0])
            elif (types == "uppercase"):
                if len(params) != 1: return -1, ['u', None]
                error_code, results = uppercase(params[0])
            elif (types == "replace"):
                if len(params) != 3: return -1, ['u', None]
                error_code, results = substring_replace(params[0], params[1], params[2])
            elif (types == "substring"):
                if len(params) != 3: return -1, ['u', None]
                error_code, results = get_substring(params[0], params[1], params[2])
            elif (types == "add"):
                if len(params) < 1: return -1, ['u', None]
                error_code, results = add_value(params)
            elif (types == "subtract"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = sub_value(params[0], params[1])
            elif (types == "multiply"):
                if len(params) < 1: return -1, ['u', None]
                error_code, results = mul_value(params)
            elif (types == "divide"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = div_value(params[0], params[1])
            elif (types == "abs"):
                if len(params) != 1: return -1, ['u', None]
                error_code, results = abs_value(params[0])
            elif (types == "max"):
                if len(params) < 1: return -1, ['u', None]
                error_code, results = max_value(params)
            elif (types == "min"):
                if len(params) < 1: return -1, ['u', None]
                error_code, results = min_value(params)
            elif (types == "gt"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = greater_value(params[0], params[1])
            elif (types == "lt"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = lower_value(params[0], params[1])
            elif (types == "equal"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = equal(params[0], params[1])
            elif (types == "not_equal"):
                if len(params) != 2: return -1, ['u', None]
                error_code, results = notequal(params[0], params[1])
            elif (types == "str"):
                if len(params) != 1: return -1, ['u', None]
                error_code, results = convert_string(params[0])
            else:
                return -1, ['u', None]
            
            if (error_code < 0): return -1, ['u', None]
            return char_i + 1, results
        
        if (instruction[char_i] >= 'a' and instruction[char_i] <= 'z' ) or (instruction[char_i] >= "A" and instruction[char_i] <= 'Z'):
            char_i, temp_param = check_var(instruction, char_i)
            if char_i < 0 or char_i >= len(instruction): return -1, ['u', None]
        else:
            return -1, ['u', None]
        
    return -1, ['u', None]


@app.route('/lisp-parser', methods=['POST'])
def mini_interpreter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    global public_var
    global terminal
    public_var = {}
    terminal = []

    for instruction_line in range(len(data["expressions"])):
        error_code, value = decode_instructions(data["expressions"][instruction_line], 0)
        if (error_code < 0): 
            terminal = ["ERROR at line " + instruction_line] 
            break

    result = [{"output": terminal}]

    logging.info("My result :{}".format(result))
    return json.dumps(result)
