import random
import numpy as np
import copy
import operator
import time
import datetime


class Brain():

    def __init__(self, i, h, o):
        # estructura de la red neuronal
        self.iNodes = i
        self.hNodes = h
        self.oNodes = o

        self.iWeights = 2 * np.random.random((h, i + 1)) - 1
        self.hWeights = 2 * np.random.random((i, h + 1)) - 1
        self.oWeights = 2 * np.random.random((o, h + 1)) - 1

    def mutate(self, matrix, rate):
        for i, r in enumerate(matrix):
            for k, c in enumerate(r):
                if random.uniform(0, 1) < rate:
                    matrix[i][k] += matrix[i][k] * np.random.normal(0, 0.25)
                    if matrix[i][k] > 1:
                        matrix[i][k] = 1
                    elif matrix[i][k] < -1:
                        matrix[i][k] = -1

    def mutate_all(self, rate):
        self.mutate(self.iWeights, rate)
        self.mutate(self.hWeights, rate)
        self.mutate(self.oWeights, rate)

    # función sigmoide σ(x) = 1 / 1 + e^-x
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # aplicaión de la función sigmoide
    def activate(self, matrix):
        for i, r in enumerate(matrix):
            for k, c in enumerate(r):
                matrix[i][k] = self.sigmoid(matrix[i][k])
        return matrix

    def add_bias(self, m, sz):
        n = np.array(m).flatten()
        n = np.append(n, [1]).reshape(sz + 1, 1)
        return n

    def output(self, matrix):

        # ---------------Primer capa------------------#
        input = self.add_bias(matrix, self.iNodes)
        # r1·c1 + r1·c2 + ... + rn·cn
        hiddenIn = np.dot(self.iWeights, input)
        hiddenOut = self.activate(hiddenIn)

        # --------------Segunda capa-----------------#
        hiddenOut = self.add_bias(hiddenOut, self.hNodes)
        secHiddenIn = np.dot(self.hWeights, hiddenOut)
        secHiddenOut = self.activate(secHiddenIn)

        # -------------Valor de salida---------------#
        secHiddenOut = self.add_bias(secHiddenOut, self.hNodes)
        outputInput = np.dot(self.oWeights, secHiddenOut)
        output = self.activate(outputInput)

        highest = max(output.flatten())
        for i, k in enumerate(output.flatten()):
            if k == highest:
                return i
