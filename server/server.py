

from flask import Flask, render_template, Response, request, jsonify
import cv2
import subprocess
import signal
from flask_api import status
import pprint
from PIL import Image
from api_service import *
from datetime import datetime

app = Flask(__name__)
SOURCE = "rtmp://localhost:1935/live/"
STREAM = None #cv2.VideoCapture(source)
HIGHLIGHTS = []
ACTION = []
DEFAULT_IMAGE = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/server/static/LoadingStream.png'
IMAGE_BYTES = None
IS_STREAM = False
MATCH_ID = None
COOKIES = {
    'jwt': ""
}
COOKIES['jwt'] = loginUser()

with open(DEFAULT_IMAGE, 'rb') as file:
    IMAGE_BYTES = file.read()


def tempTesting():
    my_dict = {
        "minutes": 7,
        "seconds": 5,
        "highlights": "this is a highlight" #response.lstrip('\n')
    }

    # -------- Send to API
    json_obj = json.dumps(my_dict)
    headers = {'Content-type': 'application/json'}
    response = requests.post('http://localhost:5000/recieve_highlight', data=json_obj, headers=headers)


@app.route('/')
def index():
    """Render the HTML template with the video player."""
    #maybe register for the api here ... get the cookie to use for the following requests ..
    return render_template('index.html')


def gen():
    """Generate the video frames and process them."""
    while True:
        
        global STREAM, IS_STREAM, SOURCE
        
        if IS_STREAM :
            print('---------------capturing the stream!!!!')
            STREAM = cv2.VideoCapture(SOURCE)
            IS_STREAM = False
        
        if STREAM is None: 
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + IMAGE_BYTES + b'\r\n')
            continue
        
        
        # Get the next video frame from the camera
        ret, frame = STREAM.read()
        # If the frame is valid, process it
        if ret:
            # Encode the processed frame as JPEG and yield it
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break


@app.route('/view_feed')
def view_feed():
    """Return stream"""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/recieve_highlight', methods=['POST'])
def recieve_highlight():
    json_data = request.get_json()   
    try:
        sendHighlight(
            MATCH_ID,
            json_data['highlights'],
            'N/A',
            ('%2d:%02d' % (json_data['minutes'], json_data['seconds'])).replace(' ', ''),
            COOKIES
        ) #matchID, highlight, action, time
    except:
        print('-----------could not send to api server')
        
    global HIGHLIGHT
    HIGHLIGHTS.append(json_data)
    return 'JSON received!'


@app.route('/recieve_action', methods=['POST'])
def recieve_action():
    json_data = request.get_json()
    global ACTION
    ACTION.append(json_data)
    return 'JSON received!'


@app.route('/get_highlight', methods=['GET'])
def get_highlight():
    return (jsonify(HIGHLIGHTS))


@app.route('/get_action', methods=['GET'])
def get_action():
    return (jsonify(ACTION))


@app.route('/process_stream')
def process_stream():
    print('------------------------------')
    global SOURCE
    process_main = subprocess.Popen(['python', '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/main.py', SOURCE])
    return 'Processing ...'


@app.route('/publish_stream', methods=['POST'])
def publish_stream():
    global IS_STREAM, MATCH_ID, SOURCE
    SOURCE = SOURCE + request.form['name']
    print(SOURCE)
    IS_STREAM = True
    print('--------------- stream is publishing with name', request.form['name'])
    try:
        MATCH_ID = matchIsLive(
            request.form['name'], 
            datetime.today().strftime('%Y-%m-%d'),
            COOKIES,
        ) #matchName, matchDate #match_name get it from the request.from['name']
    except:
        print('-----------could not send to api server')

    return 'OK', status.HTTP_200_OK


@app.route('/end_stream', methods=['POST'])
def end_stream():
    STREAM = None
    print('--------------- stream is Done')
    return 'OK', status.HTTP_200_OK



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 


