import cv2
import time
import threading
from flask import Flask, Response

class CameraStream:
    """
    Description:
        Captures frames from a specific camera at a given resolution and frame rate.
        This class runs a separate thread to continuously capture frames and store them.
    
    Modules:
        __init__(self, camera_id, resolution=(640, 480), fps=10):
            Initializes the CameraStream with the specified camera ID, resolution, and frame rate.
        
        update(self):
            Continuously captures frames and updates the frame attribute.
        
        get_frame(self):
            Returns the latest captured frame.
        
        stop(self):
            Stops the camera stream and releases the camera.
    """

    def __init__(self, camera_id, resolution=(640, 480), fps=10):
        """
        Initializes the camera stream with the given camera ID, resolution, and desired frame rate.
        """
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.fps = fps
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        """
        Continuously captures frames from the camera and updates the frame.
        """
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            time.sleep(1 / self.fps)

    def get_frame(self):
        """
        Returns a copy of the latest captured frame.
        """
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """
        Stops the camera stream and releases the camera resources.
        """
        self.running = False
        self.cap.release()


class StitcherTool:
    """
    Description:
        Takes two CameraStream objects and stitches their frames together to create a panorama.
        The class continuously processes the frames from both cameras and outputs the stitched image stream.
    
    Modules:
        __init__(self, cam1, cam2, fps=10):
            Initializes the StitcherTool with two CameraStream objects and a frame rate.
        
        generate_stitched_stream(self):
            Continuously captures frames from both cameras, stitches them, and streams the stitched output.
    """

    def __init__(self, cam1, cam2, fps=10):
        """
        Initializes the StitcherTool with two camera streams and the desired frame rate.
        """
        self.cam1 = cam1
        self.cam2 = cam2
        self.fps = fps
        self.stitcher = cv2.Stitcher_create()

    def generate_stitched_stream(self):
        """
        Continuously captures frames from both cameras, stitches them together, and yields the stitched stream.
        """
        while True:
            frame1 = self.cam1.get_frame()
            frame2 = self.cam2.get_frame()
            if frame1 is None or frame2 is None:
                continue
            status, stitched = self.stitcher.stitch([frame1, frame2])
            if status == cv2.STITCHER_OK:
                height, width = stitched.shape[:2]
                text = f"{width}x{height}"
                cv2.putText(stitched, text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                ret, jpeg = cv2.imencode('.jpg', stitched)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(1 / self.fps)


# Flask application setup
app1 = Flask(__name__)
app2 = Flask(__name__)
app_stitch = Flask(__name__)

@app1.route('/')
def stream_cam1():
    """
    Streams the video feed from Camera 1 at the desired frame rate.
    """
    def gen():
        while True:
            frame = cam1.get_frame()
            if frame is not None:
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(1 / cam1.fps)
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app2.route('/')
def stream_cam2():
    """
    Streams the video feed from Camera 2 at the desired frame rate.
    """
    def gen():
        while True:
            frame = cam2.get_frame()
            if frame is not None:
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(1 / cam2.fps)
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app_stitch.route('/')
def stream_stitched():
    """
    Streams the stitched video feed from both Camera 1 and Camera 2 at the desired frame rate.
    """
    stitcher = StitcherTool(cam1, cam2)
    return Response(stitcher.generate_stitched_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def run_all():
    """
    Starts the Flask servers for streaming both individual camera feeds and the stitched panorama.
    Each server runs on a separate thread to handle multiple streams simultaneously.
    """
    threading.Thread(target=lambda: app1.run(host='0.0.0.0', port=40000), daemon=True).start()
    threading.Thread(target=lambda: app2.run(host='0.0.0.0', port=40001), daemon=True).start()
    app_stitch.run(host='0.0.0.0', port=40002)


if __name__ == '__main__':
    run_all()
