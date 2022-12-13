from typing import List

import numpy as np

from src import config
from src.uninn import funsact, uninn


class NN:
    _instance: uninn.NeuralNetwork = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = uninn.NeuralNetwork(config.LAYERS)
        return cls._instance


def learn(rates, n: int):
    x, e = uninn.predict_set(0, config.INPUT_LAYER_LEN, len(rates) - config.INPUT_LAYER_LEN, 1, lambda i: rates[int(i)])
    nn = NN()
    nn.learn_n_times(x, e, n=n)


def predict(rates: List[float], n: int) -> List[float]:
    nn = NN()
    result = nn.predict(np.array(rates[-config.INPUT_LAYER_LEN:]), n)
    result = result.tolist()[config.INPUT_LAYER_LEN - 1:]
    return result
