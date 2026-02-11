from PySide6.QtCore import QPointF
from quantsim.core.qubit import Qubit
from .caditem import CADItem


class QubitCADItem(CADItem):
    qubit: Qubit

    def __init__(self, qubit: Qubit | None = None):
        super().__init__("./assets/qubit.svg", None, QPointF(490/512, 260/512))
        self.qubit = qubit if qubit else Qubit()