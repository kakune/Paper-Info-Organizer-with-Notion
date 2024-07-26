import logging
from flask import Flask, request
import subprocess
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig()


@app.route('/run_script', methods=['POST'])
def run_script():
    lData = request.json
    app.logger.debug(f"Received data: {json.dumps(lData)}")
    url = lData.get('url')
    ids = lData.get('ids', [])
    app.logger.debug(f"URL: {url}, IDs: {ids}")
    result = subprocess.run([
        os.path.join(os.path.dirname(__file__), '.venv', 'bin', 'python'),
        os.path.join(os.path.dirname(__file__), 'adder_for_chrome.py'), url] + ids, capture_output=True, text=True)
    app.logger.debug(f"Script output: {result.stdout}")
    return result.stdout


if __name__ == '__main__':
    app.run(port=5000)
