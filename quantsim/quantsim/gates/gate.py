from abc import ABC
import numpy
from numpy import complex128
from numpy.typing import NDArray


class QuantumGate(ABC):
    matrix: NDArray[complex128]

    def __init__(self, matrix: NDArray[complex128], symbol: str):
        self.matrix = matrix
        self.symbol: str = symbol

    def __array__(self):
        return numpy.matrix(self.matrix)



    def __mul__(self, rhs):
        return numpy.matrixlib.matrix(self.matrix) *  numpy.matrixlib.matrix(rhs)
