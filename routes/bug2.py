import heapq

import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def max_bugsfixed(bugseq):
    # Sort bugs by their escalation limits
    bugseq.sort(key=lambda x: x[1])
    
    current_time = 0
    max_heap = []
    
    for difficulty, limit in bugseq:
        if current_time + difficulty <= limit:
            heapq.heappush(max_heap, -difficulty)
            current_time += difficulty
        elif max_heap and -max_heap[0] > difficulty:
            current_time += difficulty + heapq.heappop(max_heap)
            heapq.heappush(max_heap, -difficulty)

    return len(max_heap)


@app.route('/bugfixer/p1', methods=['POST'])
def bug2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = max_bugsfixed(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

# bugseq = [[20, 30], [30, 150], [110, 135], [210, 330]]
# print(max_bugsfixed(bugseq))  # Output: 3