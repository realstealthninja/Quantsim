from enum import Enum
from math import isclose
from turtle import position
from typing import override

from PySide6.QtCore import QPoint, QPointF, QRect
from PySide6.QtGui import QKeyEvent, QPainterPath, Qt
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
            if inputpos and isclose(inputpos.x(), pos.x()) and isclose(inputpos.y(), pos.y()):
                return inputpos
            outputpos = caditem.output_position
            if outputpos and isclose(outputpos.x(), pos.x()) and isclose(outputpos.y(), pos.y()):
                return outputpos
            
        _x = round(pos.x() * self.grid[0])
        _y = round(pos.y() * self.grid[1])
        
        _x = base * round(_x / base)
        _y = base * round(_y / base)
    

        

        return QPointF(_x / self.grid[0], _y / self.grid[1])


    @override
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        path = QPainterPath()

        for _ in self.temp_paths:
            self.removeItem(self.temp_paths.pop())
            
        if not self.first_press:
            path.moveTo(self.previous_click)
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
                path.moveTo(self.previous_click)
                if abs(event.scenePos().x()) >= abs(event.scenePos().y()):
                    path.lineTo(QPointF(event.scenePos().x(), self.previous_click.y()))
                    path.moveTo(QPointF(event.scenePos().x(), self.previous_click.y()))
                    path.lineTo(QPointF(event.scenePos().x(), event.scenePos().y()))
                else:
                    path.lineTo(QPointF(self.previous_click.x(), event.scenePos().y()))
                    path.moveTo(QPointF(self.previous_click.x(), event.scenePos().y()))
                    path.lineTo(QPointF(event.scenePos().x(), event.scenePos().y()))                
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


    _scene: GraphicsCanvas

    def __init__(self):
        self.tool: Tools = Tools.WIRE
        self._scene = GraphicsCanvas(self.tool)
        _ = self._scene.changed.connect(self.scene_changed)
        
        super().__init__(self._scene)
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setMouseTracking(True)


    def scene_changed(self):
        # do something
        pass


    
        
