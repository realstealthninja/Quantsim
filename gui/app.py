import sys


from PySide6.QtWidgets import QApplication

from windows import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()


_ = app.exec()

