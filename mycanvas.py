from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from OpenGL.GL import *
from hetool import *
import tkinter as tk
from tkinter import messagebox as mb


class MyCanvas(QtOpenGL.QGLWidget):

    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_w = 0  # width: GL canvas horizontal size
        self.m_h = 0  # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPointF(0.0, 0.0)
        self.m_pt1 = QtCore.QPointF(0.0, 0.0)
        self.grid = False
        self.alt = 60
        self.lar = 60
        self.root = tk.Tk()
        self.coordenadas = []

        self.tol = 10e-2
        self.hemodel = HeModel()
        self.heview = HeView(self.hemodel)
        self.hecontroller = HeController(self.hemodel)

    def initializeGL(self):
        # glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height
        if(self.m_model is None) or (self.m_model.isEmpty()): self.scaleWorldWindow(1.0)
        else:
            self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
            self.scaleWorldWindow(1.1)
        glViewport(0, 0, self.m_w, self.m_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        # glClear(GL_COLOR_BUFFER_BIT)
        # if (self.m_model == None) or (self.m_model.isEmpty()): return
        # glCallList(self.list)
        # glDeleteLists(self.list, 1)
        # self.list = glGenLists(1)
        # glNewList(self.list, GL_COMPILE)
        # verts = self.m_model.getVerts()
        # glColor3f(0.0, 1.0, 0.0)  # green
        # glBegin(GL_TRIANGLES)
        # for vtx in verts:
        #     glVertex2f(vtx.getX(), vtx.getY())
        # glEnd()

        # clear the buffer with the current clear color
        glClear(GL_COLOR_BUFFER_BIT)
        # draw a triangle with RGB color at the 3 vertices
        # interpolating smoothly the color in the interior
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        # Display model polygon RGB color at its vertices
        # interpolating smoothly the color in the interior
        # glShadeModel(GL_SMOOTH)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        # print("param", self.m_pt0, "retorno:", pt0_U)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(pt0_U.x(), pt0_U.y())
        glVertex2f(pt1_U.x(), pt1_U.y())
        glEnd()

        if not ((self.m_model == None) and (self.m_model.isEmpty())):
            verts = self.m_model.getVerts()
            glColor3f(0.0, 1.0, 0.0)  # green
            curves = self.m_model.getCurves()
            glColor3f(0.0, 0.0, 1.0)  # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()

        if not(self.heview.isEmpty()):
            # print("teste")
            patches = self.heview.getPatches()
            glColor3f(1.0, 0.0, 1.0)
            for pat in patches:
                triangs = Tesselation.tessellate(pat.getPoints())
                for triang in triangs:
                    glBegin(GL_TRIANGLES)
                    for pt in triang:
                        glVertex2d(pt.getX(), pt.getY())
                    glEnd()

            segments = self.heview.getSegments()
            glColor3f(0.0, 1.0, 1.0)
            for curv in segments:
                ptc = curv.getPointsToDraw()
                glBegin(GL_LINES)
                glVertex2f(ptc[0].getX(), ptc[0].getY())
                glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()

            verts = self.heview.getPoints()
            glColor3f(1.0, 0.0, 0.0)
            glPointSize(3)
            glBegin(GL_POINTS)
            for vert in verts:
                glVertex2f(vert.getX(), vert.getY())
            glEnd()

            # pega o boundbox, cria um grid de pontos e verifica quais estão dentro do patch para mostrar
            if self.grid:
                m_L, m_R, m_B, m_T = self.heview.getBoundBox()
                glColor3f(1.0, 1.0, 1.0)
                glPointSize(3)
                glBegin(GL_POINTS)
                pontos = []
                coordenadas = []
                for i in range(int(m_L), int(m_R), int(self.lar)):
                    for j in range(int(m_B), int(m_T), int(self.alt)):
                        p = Point(i, j)
                        for pat in patches:
                            if pat.isPointInside(p):
                                pontos.append(p)
                                coordenadas.append([p.getX(), p.getY()])
                                print(len(pontos), "pontos presentes.")
                        for pt in pontos:
                            glVertex2f(pt.getX(), pt.getY())
                glEnd()
                self.coordenadas = coordenadas
        self.exportJson()
        glEndList()

    def exportJson(self):
        print(self.coordenadas)
        print(len(self.coordenadas))
        jsonString = json.dumps(self.coordenadas)
        jsonFile = open("coordenadas_dos_pontos_do_grid.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    def criaDialogBox(self):
        # root = tk.Tk()
        self.root.geometry("200x120")

        def getTextInput():
            x = horizontal.get("1.0", "end")
            y = vertical.get("1.0", "end")

            # cria o grid conforme o x e y informados
            self.criaGrid(x, y)

        horizontal = tk.Text(self.root, height=1)
        vertical = tk.Text(self.root, height=1)
        esp_lateral = tk.Label(self.root, text="Espaçamento lateral (50px+)")
        esp_vertical = tk.Label(self.root, text="Espaçamento lateral (50px+)")

        esp_lateral.pack()
        horizontal.pack()
        esp_vertical.pack()
        vertical.pack()

        btnRead = tk.Button(self.root, height=1, width=5, text="Read",
                            command=getTextInput)

        btnRead.pack()

        self.root.mainloop()

    def criaGrid(self, x, y):
        self.lar = x
        self.alt = y
        self.grid = True
        self.update()
        self.paintGL()
        print("Cria Grid")
        self.root.destroy()


    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.pos()

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)

        # aqui o programa reposiciona o inicio e o final da reta para os pontos mais proximos!
        tol = 100
        snaped1, xs1, ys1 = self.heview.snapToPoint(pt0_U.x(), pt0_U.y(), tol)
        snaped2, xs2, ys2 = self.heview.snapToPoint(pt1_U.x(), pt1_U.y(), tol)

        if snaped1:
            pt0_Ux, pt0_Uy = xs1, ys1
        else:
            pt0_Ux, pt0_Uy = pt0_U.x(), pt0_U.y()

        if snaped2:
            pt1_Ux, pt1_Uy = xs2, ys2
        else:
            pt1_Ux, pt1_Uy = pt1_U.x(), pt1_U.y()

        self.m_model.setCurve(pt0_Ux, pt0_Uy, pt1_Ux, pt1_Uy)
        self.hecontroller.insertSegment([pt0_Ux, pt0_Uy, pt1_Ux, pt1_Uy], self.tol)
        # self.m_model.setCurve(self.m_pt0.x(), self.m_pt0.y(), self.m_pt1.x(), self.m_pt1.y())
        self.m_buttonPressed = False
        self.m_pt0.setX(0.0)
        self.m_pt0.setY(0.0)
        self.m_pt1.setX(0.0)
        self.m_pt1.setY(0.0)
        self.update()
        self.paintGL()

    def setModel(self, _model):
        self.m_model = _model

    # def fitWorldToViewport(self):
    #     # if (self.m_model == None) or (self.m_model.isEmpty()): return
    #     self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
    #     self.scaleWorldWindow(1.10)
    #     self.update()

    def fitWorldToViewport(self):
        print("fitWorldToViewport")

        # mudar para heview
        if self.m_model is None:
            return
        self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()

    def scaleWorldWindow(self, _scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.m_h / self.m_w
        # Get current window center.
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        # Set new window sizes based on scaling factor.
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        # Adjust window to keep the same aspect ratio of the viewport.
        if sizey > (vpr * sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):

        # Compute pan distances in horizontal and vertical directions.
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        # Shift current window.
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
