import math
import time
import random

P = 0  # transition probability
pij = []  # emission probability
Emissions = []  # emmisions/observations
Pd1 = []  # probability for dice1
Pd2 = []  # probability for dice2
Pd3 = []  # probability for dice3
V = [{}]  # probability of each states in this obervastion sequence
Sequence = [{}]  # the most explainable sequence of states


def get_probability(x):
    global P  # transition probability
    global pij
    global Emissions
    with open(x, 'r') as f:
        data = f.readlines()
    for i in range(len(data)):
        data[i].strip()

    P = float(data[3])
    pij.append(data[5].split())
    pij[0][0] = float(pij[0][0])
    pij[0][1] = float(pij[0][0])
    pij[0][2] = float(pij[0][0])
    pij.append(data[6].split())
    pij[1][0] = float(pij[1][0])
    pij[1][1] = float(pij[1][1])
    pij[1][2] = float(pij[1][2])
    pij.append(data[7].split())
    pij[2][0] = float(pij[2][0])
    pij[2][1] = float(pij[2][1])
    pij[2][2] = float(pij[2][2])
    Emissions = data[10].split(',')
    for i in range(len(Emissions)):
        Emissions[i] = int(Emissions[i])


def viterbi_algorithm():
    global V  # probability of each states in this obervastion sequence
    global Sequence  # the most explainable sequence of states
    X = []
    for i in range(len(Emissions)):
        X.append(0)
    for i in range(3):
        V[0][i] = (1 / 3.0) * pij[i][Emissions[0] - 1]
        Sequence[0][i] = 0

    for i in range(len(Emissions)):
        if i == 0:
            continue
        V.append({})
        Sequence.append({})
        for j in range(3):
            if j == 0:
                d1 = V[i - 1][0] * P * pij[0][Emissions[i] - 1]
                d2 = V[i - 1][1] * ((1 - P) / 2) * pij[0][Emissions[i] - 1]
                d3 = V[i - 1][2] * ((1 - P) / 2) * pij[0][Emissions[i] - 1]
            elif j == 1:
                d1 = V[i - 1][0] * ((1 - P) / 2) * pij[1][Emissions[i] - 1]
                d2 = V[i - 1][1] * P * pij[1][Emissions[i] - 1]
                d3 = V[i - 1][2] * ((1 - P) / 2) * pij[1][Emissions[i] - 1]
            elif j == 2:
                d1 = V[i - 1][0] * ((1 - P) / 2) * pij[2][Emissions[i] - 1]
                d2 = V[i - 1][1] * ((1 - P) / 2) * pij[2][Emissions[i] - 1]
                d3 = V[i - 1][2] * P * pij[2][Emissions[i] - 1]
            V[i][j] = max(d1, d2, d3)
            if V[i][j] == d1:
                Sequence[i][j] = 0
            elif V[i][j] == d2:
                Sequence[i][j] = 1
            elif V[i][j] == d3:
                Sequence[i][j] = 2

    l = len(Emissions)
    (Prob, D) = max([(V[l - 1][k], k) for k in range(3)])
    for i in range(l - 1, -1, -1):
        X[i] = Sequence[i][D]
        D = X[i]
    return X


def main():
    path = "dice\\hmm_dice_1586654132710.txt"
    print("The file path is :" + path)
    get_probability(path)
    print("The emissions rolls are:")
    for i in Emissions:
        print(int(i), end=",")
    print()
    X = []
    X = viterbi_algorithm()
    print("A sequence of states which best explains the sequence of rolls:")
    for i in X:
        print(i + 1, end=',')
    print()
    input("press enter to quit")


main()





