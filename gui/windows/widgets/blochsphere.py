from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget

class BlochSphere(QQuickWidget):
    def __init__(self):
        super().__init__()

        self.setSource(QUrl("qml/bloch.qml"))
    