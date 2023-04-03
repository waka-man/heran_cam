from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def gen_frames():
    """Generate frames from the webcam."""
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()

        if not ret:
            break

        # Encode the frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, img_encoded = cv2.imencode('.jpg', frame, encode_param)

        # Yield the encoded image
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
               bytearray(img_encoded) + b'\r\n')

    # Release the webcam and clean up
    cam.release()

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/stream.mjpg')
def stream():
    """Stream frames from the webcam."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)