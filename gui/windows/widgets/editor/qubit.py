from PySide6.QtCore import QPointF
from quantsim.core import Qubit
from .caditem import CADItem


class QubitCADItem(CADItem):
    qubit: Qubit

    def __init__(self, qubit: Qubit | None = None):
        super().__init__("./assets/qubit.svg", None, QPointF(0, 0))
        self.qubit = qubit if qubit else Qubit()
        self.ouputItems = []
