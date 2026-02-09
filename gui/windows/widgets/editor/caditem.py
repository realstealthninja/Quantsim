class CADItem(QGraphicsPixmapItem):
    pixmap: QPixmap
    def __init__(self, pixmap: QPixmap):
        self.pixmap = pixmap
        super().__init__(pixmap)