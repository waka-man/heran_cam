from flask import Flask, Response, render_template, redirect, url_for, request
import cv2
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define a simple User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Define a user loader function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # Check the user's credentials against the database
        if user_id == 'myusername' and password == 'mypassword':
            user = User(user_id)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Define the logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Define the protected route
@app.route('/stream.mjpg')
@login_required
def stream():
    """Stream frames from the webcam."""
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

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Define the index route
@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')