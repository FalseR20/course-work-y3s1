import os
import pickle
from typing import Callable, Optional, Tuple, List

import numpy as np
from numpy.typing import NDArray

from src.uninn import funsact


class Layer:
    """Слой нейросети"""

    x: NDArray
    s: NDArray
    y: NDArray

    def __init__(
        self,
        lens: Tuple[int, int],
        f_act: Callable = funsact.linear,
        d_f_act: Callable = funsact.d_linear,
        w=None,
        t=None,
        is_need_vectorize=False,
    ):
        """
        - lens (количество нейронов этого и следующего слоя)
        - функции активации
        """
        self.lens = lens
        self.w = np.random.uniform(-0.5, 0.5, lens) if w is None else w
        self.t = np.random.uniform(-0.5, 0.5, lens[1]) if t is None else t
        if is_need_vectorize:
            self.f_act = np.vectorize(f_act)
            self.d_f_act = np.vectorize(d_f_act)
        else:
            self.f_act = f_act
            self.d_f_act = d_f_act
        self.d_f_act_0 = self.d_f_act(self.f_act(0))

    def go(self, x: NDArray) -> NDArray:
        """Прохождение слоя"""
        self.x = x
        self.s: NDArray = np.dot(x, self.w) - self.t
        self.y: NDArray = self.f_act(self.s)
        return self.y

    def back_propagation(self, error: NDArray, alpha: Optional[float], is_first_layer=False) -> Optional[NDArray]:
        """Обратное распространение ошибки с изменением весов, порога"""
        error_later = np.dot(error * self.d_f_act(self.y), self.w.transpose()) if not is_first_layer else None

        if not alpha:
            alpha = self.adaptive_alpha(error)

        gamma = alpha * error * self.d_f_act(self.y)
        self.w -= np.dot(self.x.reshape(-1, 1), gamma.reshape(1, -1))
        self.t += gamma

        return error_later

    def adaptive_alpha(self, error: NDArray) -> float:
        alpha = (
            (error**2 * self.d_f_act(self.y)).sum()
            / self.d_f_act_0
            / (1 + (self.x**2).sum())
            / ((error * self.d_f_act(self.y)) ** 2).sum()
        )
        return alpha


class NeuralNetwork:
    def __init__(self, args: List[int]) -> None:
        """Создание нейросети с заданием массива слоев"""

        self.layers: List[Layer] = [Layer((args[i], args[i + 1])) for i in range(len(args) - 1)]
        self.back_propagation_range = range(len(self.layers) - 1, 0, -1)

    def go(self, x: NDArray) -> NDArray:
        """Прохождение всех слоев нейросети"""
        for layer in self.layers:
            x = layer.go(x)
        return x

    def learn(self, x: NDArray[NDArray], e: NDArray[NDArray], alpha: Optional[float] = None) -> NDArray:
        """Обучение наборами обучающих выборок

        - x: (n, len_in) ... [[1 2] [2 3]]
        - e: (n, len_out) ....... [[3] [4]]
        """

        square_error = np.zeros(self.layers[-1].lens[1])
        for i in range(len(e)):
            y: NDArray = self.go(x[i])
            error: NDArray = y - e[i]
            square_error += error**2 / 2
            for layer_i in self.back_propagation_range:
                error = self.layers[layer_i].back_propagation(error, alpha)
            self.layers[0].back_propagation(error, alpha, is_first_layer=True)
        return square_error / self.layers[-1].lens[1]

    def learn_n_times(self, x: NDArray[NDArray], e: NDArray[NDArray], alpha: Optional[float] = None, n: int = 1):
        for t in range(n):
            square_error = self.learn(x, e, alpha)
            # print(f"Average square error {t : 3}: {square_error}")

    def learn_until_c(self, x: NDArray[NDArray], e: NDArray[NDArray], alpha: Optional[float] = None, n: int = 1):
        for t in range(n):
            square_error = self.learn(x, e, alpha)
            print(f"Average square error {t : 3}: {square_error}")

    def prediction_results_table(self, x: NDArray[NDArray], e: NDArray[NDArray]) -> None:
        """Красивый вывод прогона тестирующей выборки"""
        print("                эталон        выходное значение                  разница         среднекв. ошибка")
        y = self.go(x)
        y = y.reshape(-1)
        e = e.reshape(-1)
        delta = y - e
        square_error = delta**2 / 2
        for i in range(len(e)):
            print(f"{e[i] : 22}{y[i] : 25}{delta[i] : 25}{square_error[i] : 25}")
        print(f"\n-- Final testing square error: {np.average(square_error) * 2} --")

    def predict(self, x: NDArray, n: int) -> NDArray:
        len_ = self.layers[0].lens[0]
        for i in range(n):
            y = self.go(x[-len_:])
            x = np.append(x, y)
        return x


def save(nn: NeuralNetwork, filename=None) -> bool:
    # ans = input("Желаете сохранить? (y/n): ")
    ans = "y"
    if ans and (ans[0] == "y" or ans[0] == "н"):
        if filename is None:
            filename = input("Имя файла (*.nn): ") + ".nn"
        filename = "nn_files/" + filename
        if not os.path.exists("nn_files"):
            os.mkdir("nn_files")
        with open(filename, "wb") as file:
            pickle.dump(nn, file)
        print("Сохранено в", filename)
        return True
    print("Сохранение отклонено")
    return False


def load(filename=None) -> NeuralNetwork:
    if filename is None:
        filename = input("Имя файла (*.nn): ") + ".nn"
    filename = "nn_files/" + filename
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            new_nn: NeuralNetwork = pickle.load(file)
        return new_nn
    else:
        raise FileNotFoundError


class LayerSigmoid(Layer):
    """Слой нейросети с сигмоидной функцией активации"""

    def __init__(self, lens: Tuple[int, int]):
        """Слой нейросети с сигмоидной функцией активации"""
        super().__init__(lens, f_act=funsact.sigmoid, d_f_act=funsact.d_sigmoid)

    def back_propagation(self, error: NDArray, alpha: Optional[float], is_first_layer=False) -> Optional[NDArray]:
        """Обратное распространение ошибки с изменением весов, порога"""
        error_later = np.dot(error * self.y * (1 - self.y), self.w.transpose()) if not is_first_layer else None

        if not alpha:
            alpha = self.adaptive_alpha(error)

        gamma = alpha * error * self.y * (1 - self.y)
        self.w -= np.dot(self.x.reshape(-1, 1), gamma.reshape(1, -1))
        self.t += gamma

        return error_later

    def adaptive_alpha(self, error) -> float:
        alpha = (
            4
            * (error**2 * self.y * (1 - self.y)).sum()
            / (1 + (self.x**2).sum())
            / np.square(error * self.y * (1 - self.y)).sum()
        )
        return alpha


class LayerLinear(Layer):
    """Слой нейросети с линейной функцией активации"""

    def __init__(self, lens: Tuple[int, int]):
        """Слой нейросети с линейной функцией активации"""
        super().__init__(lens, funsact.linear, funsact.d_linear)

    def back_propagation(self, error: NDArray, alpha: Optional[float], is_first_layer=False) -> Optional[NDArray]:
        """Обратное распространение ошибки с изменением весов, порога"""
        error_later = np.dot(error, self.w.transpose()) if not is_first_layer else None

        if not alpha:
            alpha = self.adaptive_alpha(error)

        gamma = alpha * error
        self.w -= np.dot(self.x.reshape(-1, 1), gamma.reshape(1, -1))
        self.t += gamma

        return error_later

    def adaptive_alpha(self, error) -> float:
        alpha = 1 / (1 + np.square(self.x).sum())
        # alpha = np.square(error).sum() / (1 + np.square(self.x).sum()) / error.sum()
        return alpha


def predict_set(
    begin: float, lenght: float, count: int, step: float, function: Optional[Callable]
) -> Tuple[NDArray[NDArray], NDArray[NDArray]]:
    """Набор обучающей выборки типа:

    x = [ [1 2 3] [2 3 4] [3 4 5] ]\n
    e = [ [4] [5] [6] ]"""

    base_array = np.arange(count + lenght, dtype=np.float)
    x = np.zeros(shape=(count, lenght))
    for i in range(count):
        x[i] = base_array[i : lenght + i]
    e = base_array[lenght : lenght + count].reshape(-1, 1)

    x = x * step + begin
    e = e * step + begin
    for i in range(len(x)):
        for j in range(len(x[i])):
            x[i][j] = function(x[i][j])
    for i in range(len(e)):
        e[i][0] = function(e[i][0])
    return x, e


def shuffle_set(x: NDArray[NDArray], e: NDArray[NDArray]) -> Tuple[NDArray[NDArray], NDArray[NDArray]]:
    """Перемешивание набора обучающей выборки"""
    randomize = np.arange(len(x))
    np.random.shuffle(randomize)
    x = x[randomize]
    e = e[randomize]
    return x, e
