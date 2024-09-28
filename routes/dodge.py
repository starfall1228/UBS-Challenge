from typing import List, Dict, Optional, Tuple


import json
import logging

from flask import request

from routes import app

class Bullet:
    def __init__(self, direction: str, position: Tuple[int, int]):
        self.direction = direction
        self.position = position
        self.prev_position = None
    
    def move(self, rows: int, cols: int):
        directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
        dr, dc = directions[self.direction]
        r, c = self.position
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            self.position = (nr, nc)
            self.prev_position = (r, c)
        else:
            self.position = None  # Bullet moves out of the map

def dodge_bullets(map: List[str]) -> Dict[str, Optional[List[str]]]:
    rows = len(map)
    cols = len(map[0])
    directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    
    def find_player(map):
        for r in range(rows):
            for c in range(cols):
                if map[r][c] == '*':
                    return r, c
        return None
    
    def is_safe(map, r, c, bullets):
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        # if map[r][c] != '.':
        #     return False
        for bullet in bullets:
            if bullet.position == (r, c):
                return False
            if bullet.prev_position == (r, c):
                return False
        return True
    
    def simulate(map):
        bullets = []
        for r in range(rows):
            for c in range(cols):
                if map[r][c] in directions:
                    bullets.append(Bullet(map[r][c], (r, c)))
        
        player_pos = find_player(map)
        if not player_pos:
            return {"instructions": None}
        
        pr, pc = player_pos
        instructions = []
        counter = 0
        while True:
            for bullet in bullets:
                bullet.move(rows, cols)
            
            possible_moves = []

            # if dont need to move, dont move and return as you win
            if is_safe(map, pr, pc, bullets) and counter > 0:
                return {"instructions": instructions}

            for move, (dr, dc) in directions.items():

                
                nr, nc = pr + dr, pc + dc
                if is_safe(map, nr, nc, bullets):
                    possible_moves.append(move)
            
            if not possible_moves:
                return {"instructions": None}
            
            # Choose the first possible move (can be improved with better strategy)
            move = possible_moves[0]
            instructions.append(move)
            dr, dc = directions[move]
            pr, pc = pr + dr, pc + dc
            
            # if is_safe(map, pr, pc, bullets):
            #     print("You win")
            #     break
            counter += 1
        return {"instructions": instructions}
    
    return simulate(map)

# # Example usage:
# map_input = [
#     ".dd",
#     "r*.",
#     "..."
# ]

# print(dodge_bullets(map_input))
logger = logging.getLogger(__name__)

@app.route('/dodge', methods=['POST'])
def dodge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = dodge_bullets(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
