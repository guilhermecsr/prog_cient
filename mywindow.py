from PyQt5.QtWidgets import *
from mycanvas import *
from mymodel import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)

    def tbpressed(self, a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
