import os
from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import dotenv
from server_commands import *
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

@app.route('/login', endpoint="login", methods=["GET", "POST"])
def admin():
    return "<h1>Admin Commands Page</h1><p>Here you can manage admin commands for React Bot.</p>"

@app.route('/stats', endpoint="stats", methods=["GET", "POST"])
def stats():
    return "<h1>Statistics Page</h1><p>View real-time statistics and analyti"

socketio.run(app, host='0.0.0.0', port=8080, debug=True)