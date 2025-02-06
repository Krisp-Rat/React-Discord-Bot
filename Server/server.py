import os
from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import dotenv
import json

from server_commands import *
app = Flask(__name__)
dotenv.load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/', methods=["GET", "POST"])
def index():
    authenticationTOKEN = request.cookies.get("auth_token", "69")
    auth, usr = authenticate(convert(authenticationTOKEN))
    return render_template("index.html", username=usr, auth=auth)

@app.route('/login', endpoint="login", methods=["GET", "POST"])
def login():
    password = request.json.get('password')
    auth, usr = authenticate(password)
    if auth:
        message = {"status": "success", "message": "Access granted!"}
    else:
        message = {"status": "failure", "message": "Incorrect password."}
    # Create a response object
    response = make_response(json.dumps(message))
    # Convert the password to a byte string
    token = str(int.from_bytes(password.encode(), "big"))
    response.set_cookie('auth_token', token, max_age=60 * 60)  # cookie expires in 1 day
    return response

@app.route('/admin', endpoint="admin", methods=["GET", "POST"])
def admin():
    authenticationTOKEN = request.cookies.get("auth_token", "69")
    auth, usr = authenticate(convert(authenticationTOKEN))
    msg = request.args.get('message', "")

    return render_template("admin.html", auth=auth, message=msg)

@app.route("/ban", methods=["POST"])
def edit_ban_list():
    authenticationTOKEN = request.cookies.get("auth_token", "69")
    auth, usr = authenticate(convert(authenticationTOKEN))
    channel_id = request.form.get("channel_id")
    valid, name = grabChannelName(channel_id)
    message = ""
    if auth and valid:
        action = request.form.get('action') == "Ban"
        message = edit_banned_list(channel_name=name, channel_id=channel_id, ban=action)

    return redirect(url_for("admin", message=message))
@app.route('/stats', endpoint="stats", methods=["GET", "POST"])
def stats():
    return "<h1>Statistics Page</h1><p>View real-time statistics and analytics"

@app.route("/react_icon", methods=["GET", "POST"])
def react_icon():
    file_path = "../Reactions/reactbot_profile.png"
    return send_file(file_path)



socketio.run(app, host='0.0.0.0', port=8080, debug=True)