import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', methods=['POST'])
def colony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for i in range(len(data)):
        # generations = data[i]["generations"]
        # colony = data[i]["colony"]
        result.append(str(np.sum(colony_of_nth_generation(data[i]["colony"], data[i]["generations"]))))
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)

# def get_number(target):
#     negative = 1
#     value = 0
#     result_multiple = 10
#     value_multiple = 1
#     value_current_multiple = 1
#     for i in range(0, len(target)):
#         if target[i] == '.':
#             result_multiple = 1
#             value_multiple = 0.1
#         elif target[i] == '-':
#             negative = -1
#         elif target[i] <= '9' and target[i] >= '0':
#             value *= result_multiple
#             value_current_multiple *= value_multiple
#             value += int(target[i]) * value_current_multiple
#         else:
#             break
#     return value*negative

# def weight_of_colony(colony):
#     colony_list = []
#     sum = 0
#     for i in range(len(colony)):
#         colony_list.append(get_number(colony[i]))

#     for i in range(len(colony_list)):
#         sum += colony_list[i]
#     return sum

# def signature_of_pair(first, second):
#     if first > second:
#         return first - second
#     elif first < second:
#         return 10 - (second - first)
#     return 0

# def new_digit_by_pair(signature, weight):
#     return (weight + signature)%10

# def colony_of_next_generation(colony):
#     colony_list = []
#     new_colony_list = []
#     result_list = ""
#     for i in range(len(colony)):
#         colony_list.append(get_number(colony[i]))
#     # print (colony_list)
#     for i in range(len(colony_list) -1 ):
#         new_colony_list.append(new_digit_by_pair(signature_of_pair(colony_list[i], colony_list[(i+1)%len(colony_list)]), weight_of_colony(colony)))
    
#     colony_list_index = 0
#     new_colony_list_index = 0

#     for i in range(len(colony_list)+ len(new_colony_list)):
#         if (i % 2 == 0):
#             result_list+= str(colony_list[colony_list_index])
#             colony_list_index += 1
#         else :
#             result_list+= str(new_colony_list[new_colony_list_index])
#             new_colony_list_index += 1
#         i+=1

#     return result_list

# def colony_of_nth_generation(colony, n):
#     if n == 0:
#         return colony
#     return colony_of_nth_generation(colony_of_next_generation(colony), n-1)



# #     import numpy as np
# # from functools import reduce

# # def weight_of_colony(colony):
# #     digits = np.array(list(colony), dtype=int)
# #     return np.sum(digits)

# # def signature_of_pair(first, second):
# #     return (first - second ) %10

# # def new_digit_by_pair(signature, weight):
# #     return (weight + signature)%10

# # # def colony_of_next_generation(colony):
# # #     # colony_list = []
# # #     new_colony_list = []
# # #     result_list = ""

# # #     # for i in range(len(colony)):
# # #     #     colony_list.append(get_number(colony[i]))
    
# # #     len_of_colony_list = len(colony)
# # #     # print (colony_list)
# # #     for i in range(len_of_colony_list -1 ):
# # #         new_colony_list.append(new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)%len_of_colony_list])), weight_of_colony(colony)))
# # #     # print(new_colony_list)

# # #     colony_list_index = 0
# # #     new_colony_list_index = 0
    
# # #     for i in range(len_of_colony_list+ len(new_colony_list)):
# # #         if (i % 2 == 0):
# # #             result_list+= str(colony[colony_list_index])
# # #             colony_list_index += 1
# # #         else :
# # #             result_list+= str(new_colony_list[new_colony_list_index])
# # #             new_colony_list_index += 1
# # #         i+=1

# # #     return result_list

# # def colony_of_next_generation(colony):
# #     colony_array = np.array(list(colony), dtype=int)
# #     len_of_colony_list = len(colony)
# #     new_colony_list = np.array(list(), dtype=int)
 
# #     # new_colony_list = [
# #     #     new_digit_by_pair(
# #     #         signature_of_pair(colony_array[i], colony_array[(i + 1) % len_of_colony_list]),
# #     #         np.sum(colony_array)
# #     #     )
# #     #     for i in range(len_of_colony_list - 1)
# #     # ]
    
# #     for i in range(len_of_colony_list -1 ):
# #         new_colony_list = np.append(new_colony_list, new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)%len_of_colony_list])), np.sum(colony_array)))

# #     result_list = ''.join(
# #         str(colony_array[i // 2]) if i % 2 == 0 else str(new_colony_list[i // 2])
# #         for i in range(len_of_colony_list + len(new_colony_list))
# #     )

# #     return result_list


# # def colony_of_nth_generation(colony, n):
# #     # if n == 0:
# #     #     return colony
# #     # return colony_of_nth_generation(colony_of_next_generation(colony), n - 1)
# #     for _ in range(n):
# #         print(n)
# #         colony = colony_of_next_generation(colony)
# #         n-=1
# #     return colony
    
# # # print(weight_of_colony("914"))
# # # print(signature_of_pair(int(1), int(4)))
# # # print(new_digit_by_pair(signature_of_pair(9,1), weight_of_colony("914")))
# # # print(colony_of_next_generation("914"))
# # # print (colony_of_nth_generation("914", 4))
# # print(colony_of_nth_generation("2523", 50))



import numpy as np

def weight_of_colony(colony):
    return np.sum(colony)

def signature_of_pair(first, second):
    return (first - second ) %10

def new_digit_by_pair(first, second, weight):
    return (weight + (first - second ) %10)%10

# def colony_of_next_generation(colony):
#     # colony_list = []
#     new_colony_list = []
#     result_list = ""

#     # for i in range(len(colony)):
#     #     colony_list.append(get_number(colony[i]))
    
#     len_of_colony_list = len(colony)
#     # print (colony_list)
#     for i in range(len_of_colony_list -1 ):
#         new_colony_list.append(new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)%len_of_colony_list])), weight_of_colony(colony)))
#     # print(new_colony_list)

#     colony_list_index = 0
#     new_colony_list_index = 0
    
#     for i in range(len_of_colony_list+ len(new_colony_list)):
#         if (i % 2 == 0):
#             result_list+= str(colony[colony_list_index])
#             colony_list_index += 1
#         else :
#             result_list+= str(new_colony_list[new_colony_list_index])
#             new_colony_list_index += 1
#         i+=1

#     return result_list

# def colony_of_next_generation(colony):
#     len_of_colony_list = len(colony)
 
#     # new_colony_list = [
#     #     new_digit_by_pair(
#     #         signature_of_pair(colony_array[i], colony_array[(i + 1) % len_of_colony_list]),
#     #         np.sum(colony_array)
#     #     )
#     #     for i in range(len_of_colony_list - 1)
#     # ]
    
#     # for i in range(len_of_colony_list -1 ):
#     #     print (new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)%len_of_colony_list])), np.sum(colony)))
#     #     new_colony_list = np.append(new_colony_list, new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)%len_of_colony_list])), np.sum(colony)))

#     weight = np.sum(colony)
#     i = 0
#     num_of_new_colony = 0

#     while (num_of_new_colony < len_of_colony_list -1 ):
#         # print(i)
#         # print(colony)
#         # print(colony[i])
#         # print(colony[(i+1)])
#         # print(new_digit_by_pair(signature_of_pair(int (colony[i]), int(colony[(i+1)])), weight))
#         colony = np.insert(colony, i+1, new_digit_by_pair(colony[i], colony[(i+1)], weight))
#         i+=2
#         num_of_new_colony+=1

#     return colony

def colony_of_next_generation(colony):
    len_of_colony_list = len(colony)
    weight = np.sum(colony)
    
    # Preallocate the new colony array
    new_colony = np.empty(len_of_colony_list + len_of_colony_list - 1, dtype=int)
    
    # Fill the new colony array
    new_colony[0::2] = colony
    new_colony[1::2] = [
        new_digit_by_pair(colony[i], colony[(i + 1) % len_of_colony_list], weight)
        for i in range(len_of_colony_list - 1)
    ]
    
    return new_colony

def colony_of_nth_generation(colony, n):
    # if n == 0:
    #     return colony
    # return colony_of_nth_generation(colony_of_next_generation(colony), n - 1)
    colony_arr = np.array(list(colony), dtype=int)

    for _ in range(n):
        # print(n)
        colony_arr = colony_of_next_generation(colony_arr)
        # n-=1
    return colony_arr
    
# print(weight_of_colony("914"))
# print(signature_of_pair(int(1), int(4)))
# print(new_digit_by_pair(signature_of_pair(1,4), weight_of_colony("914")))
# print(colony_of_next_generation("914"))
# print (colony_of_nth_generation("914", 10))
# print(colony_of_nth_generation("2523", 50))