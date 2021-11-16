import sys
from OpenGL.GL import *
import Qt
from PyQt5 import QtOpenGL
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# app = QApplication([])
# label = QLabel("Hello Qt for Python")
# label.show()
# app.exec_()

# def window():
#     app = QApplication(sys.argv)
#     w = QWidget()
#     b = QLabel()
#     b.setText("Hello World!")
#
#     b.setAlignment(Qt.AlignCenter)
#
#     w.setGeometry(100, 100, 200, 50)
#     # b.move(50, 20)
#
#     vbox = QVBoxLayout()
#     vbox.addWidget(b)
#     w.setLayout(vbox)
#
#     w.setWindowTitle("PyQt")
#     w.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     window()

# class MyWidget(QWidget):
#
#     def __init__(self):
#         super(MyWidget, self).__init__()
#         self.setGeometry(100, 100, 200, 50)
#         self.setWindowTitle("PyQt")
#
# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     widget = MyWidget()
#     widget.show()
#     sys.exit(app.exec_())

# class MyWidget(QWidget):
#
#     def __init__(self):
#         super(MyWidget, self).__init__()
#         self.setGeometry(100, 100, 200, 150)
#         self.setWindowTitle("Ex1")
#         self.r1 = QLabel("a =")
#         self.r2 = QLabel("b =")
#         self.r3 = QLabel("a + b =")
#
#         self.t1 = QLineEdit()
#         self.t2 = QLineEdit()
#         self.t3 = QLineEdit()
#
#         self.b1 = QPushButton("Calcula")
#
#         self.vbox = QVBoxLayout()
#
#         self.vbox.addWidget(self.r1)
#         self.vbox.addWidget(self.t1)
#
#         self.vbox.addWidget(self.r2)
#         self.vbox.addWidget(self.t2)
#
#         self.vbox.addWidget(self.b1)
#
#         self.vbox.addWidget(self.r3)
#         self.vbox.addWidget(self.t3)
#
#         self.setLayout(self.vbox)
#
#         self.b1.clicked.connect(self.magic)
#
#     # @Slot()
#     def magic(self):
#         print("*CLICK*")
#         a = float(self.t1.text())
#         b = float(self.t2.text())
#         self.t3.setText(str(a+b))
#
#
# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     widget = MyWidget()
#     widget.show()
#     sys.exit(app.exec_())

class MyCanvas(QtOpenGL.QGLWidget):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("MyGLDrawer")

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 0.5)
        glClear(GL_COLOR_BUFFER_BIT)

    def resizeGL(self, _width, _height):

        # store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        # setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        # reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # establish the clipping volume by setting up an
        # orthographic projection
        glOrtho(0.0, self.m_w, 0.0, self.m_h, -1.0, 1.0)

        # setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        # clear the buffer with the current clear color
        glClear(GL_COLOR_BUFFER_BIT)
        # draw a triangle with RGB color at the 3 vertices
        # interpolating smoothly the color in the interior
        glShadeModel(GL_SMOOTH)
        xA = self.m_w / 3.0
        yA = self.m_h / 3.0
        xB = self.m_w * (2.0 / 3.0)
        yB = self.m_h / 3.0
        xC = self.m_w / 2.0
        yC = self.m_h * (2.0 / 3.0)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # red
        glVertex2f(xA, yA)

        glColor3f(0.0, 1.0, 0.0)  # green
        glVertex2f(xB, yB)

        glColor3f(0.0, 0.0, 1.0)  # blue
        glVertex2f(xC, yC)
        glEnd()

if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = MyCanvas()
    widget.show()
    sys.exit(app.exec_())
