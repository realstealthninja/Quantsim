from math import atan
from PySide6 import QtCore
from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget

from quantsim.core import Qubit

class BlochSphere(QQuickWidget):
    def __init__(self):
        super().__init__()
        self.setSource(QUrl("qml/bloch.qml"))

        self.view3d = self.findChild(QtCore.QObject, "View3D")
    


    def set_qubit(self, qubit: Qubit) :

        if self.view3d:
            self.view3d.setProperty("theta", atan(qubit.alpha.imag / qubit.alpha.real))
            self.view3d.setProperty("psi", atan(qubit.beta.imag / qubit.beta.real))
