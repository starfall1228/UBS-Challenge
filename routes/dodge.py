from typing import List, Dict, Optional, Tuple


import json
import logging

from flask import request, jsonify

from routes import app

# # print(dodge_bullets(map_input))
from typing import Tuple, List

class Bullet:
    def __init__(self, direction: str, position: Tuple[int, int]):
        self.direction = direction
        self.position = position
        self.prev_position = position
    
    def move(self, rows: int, cols: int):
        directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
        if self.position is None:
            return
        dr, dc = directions[self.direction]
        r, c = self.position
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            self.position = (nr, nc)
            self.prev_position = (r, c)
        else:
            self.position = None  # Bullet moves out of the map

def is_safe(position, bullets, current_direction):
    for bullet in bullets:
        if bullet.position == position:
            return False
            # if bullet direction and human direction are opposite, then it is not safe
        if bullet.prev_position == position and (current_direction in ['u', 'd'] and bullet.direction in ['u', 'd'] or current_direction in ['l', 'r'] and bullet.direction in ['l', 'r']):
            return False
    return True

def find_safe_path(current_position: Tuple[int, int], bullets: List[Bullet], path: List[str] = [], counter: int = 0, rows: int = 0, cols: int = 0): 
    r, c = current_position

    if not (0 <= r < rows and 0 <= c < cols):
        return None  # Out of bounds

    if not is_safe(current_position, bullets, path[-1] if path else None):
        return None  # Current position is not safe

    if counter >= rows - 1:
        return path  # Reached the maximum recursion depth, we win

    # Move bullets
    for bullet in bullets:
        bullet.move(rows, cols)

    # Explore all possible directions
    directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    for direction, (dr, dc) in directions.items():
        next_position = (r + dr, c + dc)
        if next_position not in path:  # Avoid cycles
            result = find_safe_path(next_position, bullets, path + [direction], counter + 1)
            if result:
                return result

    return None  # No safe path found
def find_player(map, rows, cols):
    for r in range(rows):
        for c in range(cols):
            if map[r][c] == '*':
                return r, c
    return None

logger = logging.getLogger(__name__)

@app.route('/dodge', methods=['POST'])
def dodge():
    # logging.info("dodge route called")
    data = request.data.decode('utf-8')  # Get raw data and decode it
    logging.info("data received: {}".format(data))
    
    # Split the input text into a list of strings
    map_input = data.splitlines()
    # logging.info("map_input: {}".format(map_input))
    # logging.info("dodge route called2")
    print(map_input)
    start_position = find_player(map_input, len(map_input), len(map_input[0]))
    print(start_position)
    bullets_arr = []

    directions2 = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    for r in range(len(map_input)):
        for c in range(len(map_input[0])):
            if map_input[r][c] in directions2:
                bullets_arr.append(Bullet(map_input[r][c], (r, c)))

    print(bullets_arr)

    
    result = find_safe_path(current_position=start_position, bullets=bullets_arr, rows=len(map_input), cols=len(map_input[0]))
    logging.info("result: {}".format(result))
    return jsonify(result)

# # Example usage
# bullets = [Bullet('d', (0, 1)), Bullet('d', (0, 2)), Bullet('r', (1, 0))]
# current_position = (1,1)

# safe_path = find_safe_path(current_position, bullets, rows, cols)
# print(safe_path)  # Output the safe path if found