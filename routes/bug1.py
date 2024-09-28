import json
import logging

from flask import request

from routes import app

from typing import List, Tuple, Dict
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

def calculate_min_hours(time: List[int], prerequisites: List[Tuple[int, int]]) -> int:
    # Create a graph and in-degree count
    graph = defaultdict(list)
    in_degree = [0] * (len(time) + 1)
    
    for a, b in prerequisites:
        graph[a].append(b)
        in_degree[b] += 1
    
    # Queue for projects with no prerequisites
    queue = deque()
    for i in range(1, len(time) + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Array to store the minimum time to complete each project
    min_time = [0] * (len(time) + 1)
    
    while queue:
        project = queue.popleft()
        min_time[project] += time[project - 1]
        
        for neighbor in graph[project]:
            in_degree[neighbor] -= 1
            min_time[neighbor] = max(min_time[neighbor], min_time[project])
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(min_time)

# Example usage
projects = [
    {
        "time": [3, 6, 9],
        "prerequisites": []
    },
    {
        "time": [1, 2, 3, 4, 5],
        "prerequisites": [(1, 2), (3, 4), (2, 5), (4, 5)]
    }
]

# results = [calculate_min_hours(p["time"], p["prerequisites"]) for p in projects]
# print(results)  # Output: [15, 12]

@app.route('/bugfixer/p1', methods=['POST'])
def bug1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    projects = data

    result = [calculate_min_hours(p["time"], p["prerequisites"]) for p in projects]
    # result  = calculate_min_hours(time, prerequisites)
    logging.info("My result :{}".format(result))
    return json.dumps(result)