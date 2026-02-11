from PySide6.QtCore import QPointF, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem


class CADItem(QGraphicsPixmapItem):
    input_position: QPointF | None
    output_position: QPointF | None

    def __init__(self, path: str, input_position: QPointF | None, output_postion: QPointF | None) -> None:
        super().__init__(QPixmap(path).scaled(QSize(64, 64)))
        self.input_position = input_position
        self.output_position = output_postion

    