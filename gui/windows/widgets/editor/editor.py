from enum import Enum
from math import isclose
from typing import override
from PySide6 import QtGui
from PySide6.QtCore import QPoint, QPointF, QRect, QRectF, Qt
from PySide6.QtGui import QKeyEvent, QPainter, QPainterPath, QPen, Qt
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
)

from .caditem import CADItem
from .qubit import QubitCADItem

class Tools(Enum):
    NONE = 0
    WIRE = 1


class GraphicsCanvas(QGraphicsScene):
    previous_click: QPointF
    current_pos: QPointF
    temp_paths: list[QGraphicsItem] = []
    grid: list[int] = []

    wires: list[QGraphicsItem] = []

    cad_items: list[CADItem] = []
    first_press: bool = True


    def __init__(self, tool: Tools, grid = []) -> None:
        self.tool: Tools = tool
        super().__init__()

        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.grid = [1200, 800]
        self.add_caditem(QubitCADItem())    

    def add_caditem(self, item: CADItem) -> None:
        self.addItem(item)
        self.cad_items.append(item)
    
    def set_tool(self, tool: Tools):
        self.tool = tool
    

    def snap(self, pos: QPointF) -> QPointF:
        base = 100

        for caditem in self.cad_items:
            inputpos = caditem.input_position
            if inputpos and isclose(inputpos.x(), pos.x()) and isclose(inputpos.y(), pos.y(), rel_tol=1e-1):

                return inputpos
            outputpos = caditem.output_position
            if outputpos and isclose(outputpos.x(), pos.x()) and isclose(outputpos.y(), pos.y(), rel_tol=1e-1):
                return outputpos
            
        point = pos.toPoint()
        if point.x()  % 100 < 15:
            point.setX(point.x() - point.x() % 100) 
        
        if point.y()  % 100 < 15:
            point.setY(point.y() - point.y() % 100)

        return point.toPointF()


    @override
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        path = QPainterPath()

        for _ in self.temp_paths:
            self.removeItem(self.temp_paths.pop())
            
        if not self.first_press:
            path.moveTo(self.snap(self.previous_click))
            pos = self.snap(event.scenePos())
            if abs(pos.x()) >= abs(pos.y()):
                path.lineTo(QPointF(pos.x(), self.previous_click.y()))
                path.moveTo(QPointF(pos.x(), self.previous_click.y()))
                path.lineTo(QPointF(pos.x(),pos.y()))
            else:
                path.lineTo(QPointF(self.previous_click.x(), pos.y()))
                path.moveTo(QPointF(self.previous_click.x(), pos.y()))
                path.lineTo(QPointF(pos.x(), pos.y()))
            

            self.temp_paths.append(self.addPath(path))

    @override
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        if self.tool == Tools.WIRE:
            if self.first_press:
                self.previous_click = event.scenePos()
                self.first_press = False
            else:
                path = QPainterPath()
                path.moveTo(self.snap(self.previous_click))
                pos = self.snap(event.scenePos())
                if abs(pos.x()) >= abs(pos.y()):
                    path.lineTo(QPointF(pos.x(), self.previous_click.y()))
                    path.moveTo(QPointF(pos.x(), self.previous_click.y()))
                    path.lineTo(QPointF(pos.x(), pos.y()))
                else:
                    path.lineTo(QPointF(self.previous_click.x(), pos.y()))
                    path.moveTo(QPointF(self.previous_click.x(), pos.y()))
                    path.lineTo(QPointF(pos.x(), pos.y()))                
                self.wires.append(self.addPath(path))
                self.first_press = True
    
    @override
    def keyReleaseEvent(self, event: QKeyEvent, /) -> None:
        pass

    


class Editor(QGraphicsView):
    """
    Custom editor widget which draws all the symbols and connections
    """
    previous_click: QPoint | None = None
    current_pos: QPoint = QPoint()
    paths: list[QGraphicsItem] = []
    wires: list[tuple[QPoint, QPoint]] = []

    grid_step: int = 100
    grid_pen: QPen = QPen(Qt.GlobalColor.lightGray)


    _scene: GraphicsCanvas

    def __init__(self):
        self.tool: Tools = Tools.WIRE
        self._scene = GraphicsCanvas(self.tool)
        _ = self._scene.changed.connect(self.scene_changed)
        
        super().__init__(self._scene)
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)

        
    
    @override
    def drawBackground(self, painter: QtGui.QPainter, rect: QRectF | QRect, /) -> None:
        painter.translate(.5, .5)
        painter.setPen(self.grid_pen)
        painter.fillRect(rect, Qt.GlobalColor.white)

        rect = rect.toRect() if isinstance(rect, QRectF) else rect
        y = rect.y()
        x = rect.x()

        right = rect.right()
        bottom = rect.bottom()

        top = y
        left = x
        step  = self.grid_step

        yrest = y % step
        if yrest:
            y += step - yrest
        for y in range(y, bottom, step):
            painter.drawLine(left, y, right, y)

        xrest = x % step
        if xrest:
            x += step - xrest
        for x in range(x, right, step):
            painter.drawLine(x, top, x, bottom)



    def scene_changed(self):
        # do something
        pass


    
        
