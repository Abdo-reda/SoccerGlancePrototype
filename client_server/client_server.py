from flask import Flask, render_template, Response, request, jsonify
import cv2
import subprocess
import signal
from flask_api import status
import pprint
from PIL import Image

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
HIGHLIGHTS = []



@app.route('/')
def index():
    """Render the HTML template with the video player."""
    return render_template('client.html')


@app.route('/recieve_highlight', methods=['POST']) 
def recieve_highlight(): 
    json_data = request.get_json() #match_id, body, highlight_action, match_time
    print(json_data)
    global HIGHLIGHTS
    HIGHLIGHTS.append(json_data)
    return 'OK', status.HTTP_200_OK


@app.route('/get_highlight', methods=['GET'])
def get_highlight():
    return (jsonify(HIGHLIGHTS))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 


