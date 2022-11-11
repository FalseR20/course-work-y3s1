from typing import List

import numpy as np

from src.uninn import funsact, uninn

_LAYER_LEN = 20


class NN:
    _instance: uninn.NeuralNetwork = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            layer = uninn.Layer(lens=(_LAYER_LEN, 1))
            cls._instance = uninn.NeuralNetwork(layer)
        return cls._instance


def learn(rates, n: int = 300):
    x, e = uninn.predict_set(0, _LAYER_LEN, len(rates) - _LAYER_LEN, 1, lambda i: rates[int(i)])
    nn = NN()
    nn.learn_n_times(x, e, n=n)


def predicate(rates: List[float], n: int) -> List[float]:
    nn = NN()
    result = nn.predict(np.array(rates[-_LAYER_LEN:]), n)
    result = result.tolist()[_LAYER_LEN - 1 :]
    return result
