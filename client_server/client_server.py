from flask import Flask, render_template, Response, request, jsonify
import cv2
import subprocess
import signal
from flask_api import status
import pprint
from PIL import Image


app = Flask(__name__)
HIGHLIGHTS = []



@app.route('/')
def index():
    """Render the HTML template with the video player."""
    return render_template('client.html')


@app.route('/recieve_higlight', methods=['POST'])
def recieve_higlight():
    json_data = request.get_json()
    global HIGHLIGHT
    HIGHLIGHTS.append(json_data)
    return 'JSON received!'


@app.route('/get_highlight', methods=['GET'])
def get_highlight():
    global HIGHLIGHT
    tempDict = {
        "minutes": "5",
        "seconds": "30",
        "highlights": "highlight" #response.lstrip('\n')
    }
    HIGHLIGHTS.append((tempDict))
    return (jsonify(HIGHLIGHTS))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 


