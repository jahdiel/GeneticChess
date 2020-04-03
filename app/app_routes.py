import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Thread
import time
import numpy as np
from genetics.genetic_chess import render_board, chooseKRandomIndividuals, selection, crossover, mutation, getFitnessValue

app = Flask(__name__)
socketio = SocketIO(app)

MAX_ITER = 1000
clients = []

@app.route("/")
def home():
    return render_template('main.html')

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
    K = 500  # Population size 
    # Initialize population
    states = chooseKRandomIndividuals(K)
    # print(states)
    for i in range(MAX_ITER):
        # Selection
        states, h_vals, is_solution = selection(states)
        if is_solution:
            print("Iteration:", i)
            print(states[0])
            socketio.emit('chess board', {'data': render_board(states[0])}, room=clients[0])
            time.sleep(1)
            return
        # Cross Over
        states = crossover(states)
        # Mutation
        states = mutation(states)

        if i % 10 == 0:
            print("Iter "+str(i)+":", np.max(h_vals))
            socketio.emit('chess board', {'data': render_board(states[np.argmax(h_vals)])}, room=clients[0])
            time.sleep(1)



if __name__ == '__main__':
    socketio.run(app)