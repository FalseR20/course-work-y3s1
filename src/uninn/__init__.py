import sys
from typing import List

import numpy as np

from src.parser import parse_dataset
from src.uninn import funsact, uninn

LAYER_LEN = 20


class NN:
    _instance: uninn.NeuralNetwork = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # try:
            #     cls._instance = uninn.load("unknown.nn")
            # cls._instance = uninn.load("20v2.nn")
            # assert cls._instance.layers[0].lens == (LAYER_LEN, 1)
            # except FileNotFoundError or AssertionError:
            layer = uninn.Layer(lens=(LAYER_LEN, 1))
            cls._instance = uninn.NeuralNetwork(layer)
        return cls._instance


def main():
    rates, times = parse_dataset("")
    x, e = uninn.predict_set(0, LAYER_LEN, len(rates) - LAYER_LEN, 1, lambda i: rates[int(i)])
    nn = NN()
    # nn.learn_n_times(x, e, None, 50_000)
    # nn.learn_until_c(x, e, None)
    # uninn.save(nn)

    res = nn.predict(np.array(rates[-LAYER_LEN:]), 10)
    print(res)


def learn(rates):
    x, e = uninn.predict_set(0, LAYER_LEN, len(rates) - LAYER_LEN, 1, lambda i: rates[int(i)])
    nn = NN()
    nn.learn_n_times(x, e, n=300)


def predicate(rates: List[float], n: int) -> List[float]:
    nn = NN()
    result = nn.predict(np.array(rates[-LAYER_LEN:]), n)
    result = result.tolist()[LAYER_LEN - 1:]
    print(result, file=sys.stderr)
    return result


if __name__ == "__main__":
    main()
