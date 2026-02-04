from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget, QMainWindow, QToolBar, QToolBox

from .widgets.blochsphere import BlochSphere

from .widgets import Editor


class MainWindow(QMainWindow):
    docks: dict[str, QDockWidget] = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Circuit Designer")
        self.setMinimumSize(QSize(1200, 800))
        self.add_widgets()
        self.add_dockables()
        


    def add_widgets(self):
        self.editor: Editor = Editor()
        self.toolbar: QToolBar = QToolBar()

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_new = QAction("&New", self)
        file_menu.addAction(file_new)


        self.view_menu = menu.addMenu("&View")

        self.toolbar.addAction(QAction("&Line tool"))
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.editor)


    def add_dockables(self):
        toolboxdock = QDockWidget("Tool box")
        blochsphere = QDockWidget("Bloch Sphere")
        self.toolbox: QToolBox  = QToolBox()

        blochsphere.setWidget(BlochSphere())
        toolboxdock.setWidget(self.toolbox)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, toolboxdock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, blochsphere)

        view_toolbox = toolboxdock.toggleViewAction()
        view_bloch = blochsphere.toggleViewAction()
        self.view_menu.addActions([view_bloch, view_toolbox])
        self.docks["toolbox"] = toolboxdock
        self.docks["bloch"] = blochsphere
    


        
        
    


