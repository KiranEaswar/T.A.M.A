# Import the necessary packages
from flask import Flask, Response
import cv2

# Initialize the Flask application
app = Flask(__name__)

# Initialize the video capture object
camera = cv2.VideoCapture(0)  # Use 0 for the default camera

def generate_frames():
    while True:
        # Read the current frame from the camera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the output frame in the byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media type
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Video Feed</h1><img src='/video_feed'>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
