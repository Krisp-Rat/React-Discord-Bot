import os
from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import dotenv
from text_processing import *
app = Flask(__name__)
dotenv.load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/', methods=["GET", "POST"])
def index():
    authenticationTOKEN = request.cookies.get("authenticationTOKEN", "none")
    auth, usr = authenticate(authenticationTOKEN)
    if auth:
        return render_template("index.html", username=usr)

    return render_template("index.html")




socketio.run(app, host='0.0.0.0', port=8080, debug=True)