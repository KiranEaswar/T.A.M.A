import cv2
from flask import Flask, Response
import time

# Camera index and cascade file
CAMERA_INDEX = 1  # Set to 0 if this is the default camera
CASCADE_HAND = 'palm.xml'

# Initialize Flask app
app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened():
    print("Error: Camera could not be opened.")
    exit(1)

print('Camera Available')

# Load hand detection classifier
hand_casc = cv2.CascadeClassifier(CASCADE_HAND)
if hand_casc.empty():
    print("Error: Cascade classifier not loaded correctly.")
    exit(1)

print('Cascade Loaded')

def gen_frames():
    while True:
        # Capture frame from camera
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Draw midline (blue color)
        midline = frame.shape[1] // 2
        cv2.line(frame, (midline, 0), (midline, frame.shape[0]), (255, 0, 0), 2)  # Blue line
        
        # Convert the frame to grayscale for hand detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect hands in the frame
        hands = hand_casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        # Check if hands were detected
        if len(hands) > 0:
            (x, y, w, h) = hands[0]  # Get the first detected hand
            print(f'Hand detected at ({x},{y},{x+w},{y+h})')
            
            # Check if the hand's bounding box touches or crosses the midline
            if x < midline < (x + w):
                # Hand is near or crossing the midline, draw a green rectangle
                color = (0, 255, 0)  # Green
            else:
                # Hand is not near the midline, draw a red rectangle
                color = (0, 0, 255)  # Red
            
            # Draw the rectangle around the hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

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

@app.route('/')
def index():
    # Return a simple webpage displaying the video stream
    return '''<html>
                <body>
                    <h1>Hand Detection Stream</h1>
                    <img src="/video_feed">
                </body>
              </html>'''

@app.route('/video_feed')
def video_feed():
    # Return the video stream from the camera
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run Flask app on IP and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
