import numpy as np
import chess
import chess.svg
import random
from copy import deepcopy
import genetics.utils as utils

def render_board(q_pos):
    positions = utils.position_2_string(q_pos)
    board = chess.Board(positions)
    return chess.svg.board(board=board, size=800)

def chooseKRandomIndividuals(K):
    return [[random.randint(1, 8) for j in range(8)] for i in range(K)]

def mutation(states):
    states = deepcopy(states)
    for i in range(len(states)):
        mutProb = np.random.choice([0, 1], size=1, p=[0.15, 0.85])[0]
        if mutProb == 0:
            swap1 = random.randint(0, 7)
            swap2 = random.randint(0, 7)
            temp = states[i][swap1]
            states[i][swap1] = states[i][swap2]
            states[i][swap2] = temp

    return states

def crossover(states):
    states = deepcopy(states)
    for i in range(1, len(states), 2):
        split = random.randint(1, 7)
        temp = deepcopy(states[i-1][:split])
        states[i-1][:split] = deepcopy(states[i][:split])
        states[i][:split] = temp

    return states

def selection(states):
    h = [] 
    for state in states:
        h.append(getFitnessValue(state))
    if 28 in h:
        max_value = np.max(h)
        max_idx = np.argmax(h)
        return [deepcopy(states[max_idx]) for i in range(len(states))], [max_value for i in h], True
    probs = [val / sum(h) for val in h]
    # print(states)
    # print(probs)
    chosenIndices = np.random.choice(range(len(states)), size=len(states), p=probs) # choose states proportional to their fitness probability
    # print(chosenIndices)
    return [deepcopy(states[i]) for i in chosenIndices], [h[i] for i in chosenIndices], False


def getFitnessValue(state):
    h = 0
    for i in range(len(state)-1):
        for j in range(i+1, len(state)):
            if state[i] == state[j]: # Queens in the same row
                h += 1
            elif state[i] + (j - i) == state[j]: # Queen above in diagonal
                h += 1
            elif state[i] - (j - i) == state[j]: # Queen below in diagonal
                h += 1
    
    return 28 - h
