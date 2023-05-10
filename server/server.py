from flask import Flask, render_template, Response, request, jsonify
import cv2
import subprocess
import signal
from flask_api import status
import pprint
from PIL import Image


app = Flask(__name__)
source = "rtmp://localhost:1935/live/mystream"
STREAM = None #cv2.VideoCapture(source)
HIGHLIGHTS = []
ACTION = []
DEFAULT_IMAGE = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/server/static/SoccerGlanceLogo.png'
IMAGE_BYTES = None
IS_STREAM = False


with open(DEFAULT_IMAGE, 'rb') as file:
    IMAGE_BYTES = file.read()


@app.route('/')
def index():
    """Render the HTML template with the video player."""
    return render_template('index.html')


def gen():
    """Generate the video frames and process them."""
    while True:
        
        global STREAM
        global IS_STREAM
        
        if IS_STREAM :
            print('---------------capturing the stream!!!!')
            STREAM = cv2.VideoCapture(source)
            IS_STREAM = False
        
        if STREAM is None: 
            print('------------NONE')
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


@app.route('/recieve_higlight', methods=['POST'])
def recieve_higlight():
    json_data = request.get_json()
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
    process_main = subprocess.Popen(['python', '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/main.py'])
    return 'Processing ...'


@app.route('/publish_stream', methods=['POST'])
def publish_stream():
    global IS_STREAM
    IS_STREAM = True
    print('--------------- stream is publishing with name', request.form['name'])
    return 'OK', status.HTTP_200_OK


@app.route('/end_stream', methods=['POST'])
def end_stream():
    print('--------------- stream is Done')
    return 'OK', status.HTTP_200_OK



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 


