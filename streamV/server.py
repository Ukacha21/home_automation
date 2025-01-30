from flask import Flask, Response
import cv2
import gevent
from gevent.pywsgi import WSGIServer

"""
Ethernet
IPv4 Address. . . . . . . . . . . : 192.168.42.27

Wirels
IPv4 Address. . . . . . . . . . . :
"""

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    cap = cv2.VideoCapture('streamV/video.mp4')  # Replace with your video file path

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: %d\r\n\r\n' % len(frame) +
               frame + b'\r\n')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()