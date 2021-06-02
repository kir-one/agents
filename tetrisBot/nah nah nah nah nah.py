import numpy as np

def tip(i, h, o):

    iNodes = i
    hNodes = h
    oNodes = o

    h = [1, 44, 7]
    i = [9, 67, 5]

    iWeights = 2 * np.random.random((h, i + 1)) - 1
    hWeights = 2 * np.random.random((h, h + 1)) - 1
    oWeights = 2 * np.random.random((o, h + 1)) - 1

    print(iWeights)