import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Thread
import time
from genetics.genetic_chess import render_board

app = Flask(__name__)
socketio = SocketIO(app)

clients = []

@app.route("/")
def home():
    return render_template('main.html', title="Homey")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)
    thread = Thread(target=update_chess)
    thread.daemon = True
    thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

def update_chess():
    for i in range(10):
        socketio.emit('chess board', {'data': render_board()}, room=clients[0]) # "Working... {}/{}".format(i + 1, 10)"
        time.sleep(1)

if __name__ == '__main__':
    socketio.run(app)