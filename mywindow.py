from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mycanvas import *
from mymodel import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)

        # create a Toolbar
        tb = self.addToolBar("File")

        fit = QAction(QIcon("icons/zoom.png"), "fit", self)
        tb.addAction(fit)

        grid = QAction(QIcon("icons/grid.png"), "grid", self)
        tb.addAction(grid)

        # clearAll = QAction(QIcon("icons/trash.png"), "clear", self)
        # tb.addAction(clearAll)

        rect = QAction(QIcon("icons/selecao_rect.png"), "rect", self)
        tb.addAction(rect)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self, a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()

        if a.text() == "grid":
            self.canvas.criaDialogBox(grid=True)

        if a.text() == "clear":
            self.canvas.clearAll()

        if a.text() == "rect":
            self.canvas.retangular = True
