from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
app = Flask(__name__)



socketio.run(app, host='0.0.0.0', port=8080, debug=True)