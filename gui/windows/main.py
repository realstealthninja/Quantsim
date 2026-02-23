from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QToolBar,
    QToolBox,
    QToolButton,
)
from quantsim.core import Qubit

from .widgets.blochsphere import BlochSphere
from .widgets.editor import Editor
from .widgets.editor.editor import Tools
from .widgets.editor.qubit import QubitCADItem


class MainWindow(QMainWindow):
    docks: dict[str, QDockWidget] = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Circuit Designer")
        self.setMinimumSize(QSize(1200, 800))
        self.add_widgets()
        self.add_dockables()

        _ = self.editor.qubititem_selected.connect(self.render_qubit)

    def render_qubit(self, qubit: Qubit) -> None:
        self.bloch.set_qubit(qubit)

    def add_widgets(self):
        self.editor: Editor = Editor()
        self.toolbar: QToolBar = QToolBar("Tool Bar")

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_new = QAction("&New", self)
        file_menu.addAction(file_new)

        self.view_menu = menu.addMenu("&View")

        wire_action = QAction("&Wire tool", self.toolbar)
        _ = wire_action.triggered.connect(self.wire_selected)
        self.toolbar.addAction(wire_action)
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.editor)

    def wire_selected(self) -> None:
        if self.editor.tool == Tools.WIRE:
            self.editor.tool = Tools.NONE
        else:
            self.editor.set_tool(Tools.WIRE)
        self.editor.cadItem = None

    def qubit_selected(self, action: QAction) -> None:
        if self.editor.tool == Tools.PLACE:
            self.editor.tool = Tools.NONE
        else:
            self.editor.set_tool(Tools.PLACE)
            self.editor.cadItem = QubitCADItem()

    def add_dockables(self):
        """
        adds dockable widgets to the main window

        :param self: Description
        """
        toolboxdock = QDockWidget("Tool box")
        blochsphere = QDockWidget("Bloch Sphere")
        self.toolbox: QToolBox = QToolBox()
        qubitbtn = QToolButton()
        qubitbtn.setIcon(QIcon("./assets/qubit.svg"))

        qubitbtn.setIconSize(QSize(128, 128))
        qubitaction = QAction("", qubitbtn)
        _ = qubitaction.triggered.connect(self.qubit_selected)
        qubitbtn.setDefaultAction(qubitaction)
        _ = self.toolbox.addItem(qubitbtn, "core")

        self.bloch = BlochSphere()
        blochsphere.setWidget(self.bloch)
        toolboxdock.setWidget(self.toolbox)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, toolboxdock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, blochsphere)

        view_toolbox = toolboxdock.toggleViewAction()
        view_bloch = blochsphere.toggleViewAction()
        self.view_menu.addActions([view_bloch, view_toolbox])
        self.docks["toolbox"] = toolboxdock
        self.docks["bloch"] = blochsphere
