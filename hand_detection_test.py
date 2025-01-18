from flask import Flask, Response
import cv2

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)  # Use 0 for the default camera
    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                height,width,_ = frame.shape
                midline = width//2
                cv2.line(frame,(width,0),(width,height),color=(255,0,0),thickness=1.5)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Video Feed</h1><img src='/video_feed'>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
