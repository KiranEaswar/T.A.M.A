import cv2
from flask import Flask, Response

# Initialize Flask app
app = Flask(__name__)

# Initialize camera (use index 0 or 1 depending on the camera)
camera = cv2.VideoCapture(0)  # Change to 1 if your camera is on index 1

# Function to generate frames for streaming
def gen_frames():
    while True:
        # Capture frame from camera
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Error: Failed to encode frame.")
            break

        # Convert the frame to bytes
        frame = buffer.tobytes()

        # Yield the frame in the appropriate format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route to serve the video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Main route to serve a simple HTML page
@app.route('/')
def index():
    return '''<html>
                <body>
                    <h1>Video Feed</h1>
                    <img src="/video_feed">
                </body>
              </html>'''

# Run the Flask app on the local machine, port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
