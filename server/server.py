from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
source = "rtmp://localhost:1935/live/mystream"
STREAM = None

def handle_stream(stream):
    # Do something with the stream
    print(f"Received stream from {stream.client_id}")


@app.route('/')
def index():
    """Render the HTML template with the video player."""
    global STREAM
    if STREAM is None or not STREAM.isOpened():
        STREAM = cv2.VideoCapture(source)
        print('Warning: unable to open video source: ', source)
    return render_template('index.html')

def gen():
    """Generate the video frames and process them."""
    while True:
        # Get the next video frame from the camera
        ret, frame = STREAM.read() 
        # If the frame is valid, process it
        if ret:
            # Encode the processed frame as JPEG and yield it
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break


@app.route('/view_feed')
def view_feed():
    """Return stream"""
    global STREAM
    if STREAM is None or not STREAM.isOpened():
        return Response(status=204)
    else :
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
      

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True) #app.run(host='0.0.0.0', port=5000, debug=True) #10.7.57.90
    

# from rtmplite3.rtmp import FlashServer
# from rtmplite3 import multitask
#  rtmpServer = FlashServer()   # a new RTMP server instance
#     rtmpServer.root = 'flvs/'    # set the document root to be 'flvs' directory. Default is current './' directory.
#     rtmpServer.start()           # start the server
#     multitask.run()         # this is needed somewhere in the application to actually start the co-operative multitasking.