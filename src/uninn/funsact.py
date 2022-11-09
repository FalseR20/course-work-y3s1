import numpy as np


def sigmoid(s):  # sigmoid
    return 1.0 / (1.0 + np.exp(-s))


def d_sigmoid(y):  # sigmoid'
    return y * (1.0 - y)


def linear(s):  # linear
    return s


def d_linear(_):  # linear'
    return 1.0
