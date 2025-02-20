from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session, send_file, \
    send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
from dotenv import load_dotenv
import json
from statistics import createMC
from server_commands import *

dotenv.load_dotenv(dotenv_path='../Storage/.env')
app = Flask(__name__)
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


    return render_template("admin.html", auth=auth)

@app.route("/ban", endpoint="ban", methods=["GET","POST"])
def edit_ban_list():
    authenticationTOKEN = request.cookies.get("auth_token", "69")
    auth, usr = authenticate(convert(authenticationTOKEN))
    if request.method == "GET":
        msg = request.args.get('message', "")
        print(msg)
        return render_template("ban.html", auth=auth, message=msg)
    channel_id = request.form.get("channel_id")
    valid, name = grabChannelName(channel_id)
    message = ""
    if auth and valid:
        action = request.form.get('action') == "Ban"
        message = edit_banned_list(channel_name=name, channel_id=channel_id, ban=action)

    return redirect(url_for("ban", message=message))
@app.route('/stats', endpoint="stats", methods=["GET", "POST"])
def stats():
    message_history = createMC()
    return render_template("stats.html", reactions=message_history)


@app.route('/add-phrase',endpoint= "add_phrase", methods=['GET', 'POST'])
def add_phrase():
    if request.method == 'POST':
        phrase = request.form.get('phrase')
        # Handle adding phrase logic here
        return f"Phrase '{phrase}' has been added!"
    return render_template('add_phrase.html')

@app.route('/speak',endpoint="speak", methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        # Handle sending message logic here

        return f"Message '{message}' has been sent!"
    return render_template('send_message.html')


@app.route("/react_icon", methods=["GET", "POST"])
def react_icon():
    file_path = "../Storage/reactbot_profile.png"
    return send_file(file_path, mimetype='image/png')


@app.route("/<path:filename>")
def serve_static(filename):
    static_dir = os.path.join(app.root_path, 'static')
    return send_from_directory(static_dir, filename)

socketio.run(app, host='0.0.0.0', port=8080, debug=True)