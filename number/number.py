from flask import Flask, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)

window_size = 10
numbers_queue = deque(maxlen=window_size)
test_server_url = 'http://20.244.56.144/test/getNumber/'

@app.route('/numbers/<numberid>')
def get_numbers(numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({'error': 'Invalid number ID'}), 400

    try:
        response = requests.get(test_server_url + numberid, timeout=0.5)
        numbers = response.json()
    except (requests.RequestException, ValueError):
        return jsonify({'error': 'Failed to fetch numbers from the test server'}), 500

    # Update numbers queue
    numbers_queue.extend(numbers)

    window_prev_state = list(numbers_queue)
    window_curr_state = list(numbers_queue)[-window_size:]

    if len(window_curr_state) > 0:
        avg = sum(window_curr_state) / len(window_curr_state)
    else:
        avg = 0

    return jsonify({
        'numbers': numbers,
        'windowPrevState': window_prev_state,
        'windowCurrState': window_curr_state,
        'avg': avg
    })

if __name__ == '__main__':
    app.run(debug=True)