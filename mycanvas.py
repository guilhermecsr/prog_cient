from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from OpenGL.GL import *
from hetool import *
from tkinter import *
import numpy as np
from tkinter import messagebox as mb


class MyCanvas(QtOpenGL.QGLWidget):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_model = None
        self.m_w = 0  # width: GL canvas horizontal size
        self.m_h = 0  # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.retangular = False
        self.list = None
        self.m_buttonPressed = False
        self.leftMouse = False
        self.m_pt0 = QtCore.QPointF(0.0, 0.0)
        self.m_pt1 = QtCore.QPointF(0.0, 0.0)

        # self.m_buttonPressed = False
        self.m_pt0_f = QtCore.QPointF(0.0, 0.0)
        self.m_pt1_f = QtCore.QPointF(0.0, 0.0)
        self.fencedPoints = []
        self.bconditions = []

        self.grid = False
        self.pontos = []
        self.alt = 60
        self.lar = 60
        self.coordenadas = []
        self.indices = []

        self.tol = 10e-2
        self.hemodel = HeModel()
        self.heview = HeView(self.hemodel)
        self.hecontroller = HeController(self.hemodel)

        # self.hemodel_fence = HeModel()
        # self.heview_fence = HeView(self.hemodel_fence)
        # self.hecontroller_fence = HeController(self.hemodel_fence)

    def initializeGL(self):
        # glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height
        if (self.m_model is None) or (self.m_model.isEmpty()):
            self.scaleWorldWindow(1.0)
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

        pt0f_U = self.convertPtCoordsToUniverse(self.m_pt0_f)
        pt1f_U = self.convertPtCoordsToUniverse(self.m_pt1_f)
        # print("param", self.m_pt0, "retorno:", pt0_U)

        if not ((self.m_model == None) and (self.m_model.isEmpty())):
            # verts = self.m_model.getVerts()
            # glColor3f(0.0, 1.0, 0.0)  # green
            curves = self.m_model.getFences()
            glColor3f(0.0, 0.0, 1.0)  # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()

        if not (self.heview.isEmpty()):
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

        if self.leftMouse:
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_LINE_STRIP)
            glVertex2f(pt0_U.x(), pt0_U.y())
            glVertex2f(pt1_U.x(), pt1_U.y())

            glEnd()
            # self.exportJson()

        else:
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_LINE_STRIP)
            # x1, y1, x2, y2 = int(pt0f_U.x()), int(pt0f_U.y()), int(pt1f_U.x()), int(pt1f_U.y())
            # QtCore.QRect.getCoords(x1, y1, x2, y2)
            # r1 = QtCore.QRect(x1, y1, x2, y2)

            # QRect não funcionou, fiz linha por linha
            glVertex2f(pt0f_U.x(), pt0f_U.y())
            glVertex2f(pt1f_U.x(), pt0f_U.y())
            glVertex2f(pt0f_U.x(), pt0f_U.y())
            glVertex2f(pt0f_U.x(), pt1f_U.y())
            glVertex2f(pt1f_U.x(), pt1f_U.y())
            glVertex2f(pt1f_U.x(), pt0f_U.y())
            glEnd()

        # pega o boundbox, cria um grid de pontos e verifica quais estão dentro do patch para mostrar
        self.grid_de_pontos()
        self.exportJson()
        glEndList()

    def grid_de_pontos(self):
        if not (self.heview.isEmpty()):
            patches = self.heview.getPatches()
            if self.grid:
                m_L, m_R, m_B, m_T = self.heview.getBoundBox()
                glPointSize(3)
                glBegin(GL_POINTS)
                eterno = 0
                x = 0
                y = 0
                pontos = []
                indices = []
                for i in range(int(m_L)+1, int(m_R)-1, int(self.lar)):
                    x += 1
                    for j in range(int(m_B)+1, int(m_T)-1, int(self.alt)):
                        p = Point(i, j)
                        y += 1
                        for pat in patches:
                            if pat.isPointInside(p):
                                eterno += 1
                                p.attributes.append([eterno, x, y])
                                indices.append([eterno, x, y])
                                pontos.append(p)
                            else:
                                p.attributes.append([0, x, y])
                                indices.append([0, x, y])
                                pontos.append(p)
                        for pt in pontos:
                            if pt.selected:
                                glColor3f(1.0, 0.0, 0.0)
                                print('select')
                            else:
                                glColor3f(1.0, 1.0, 1.0)
                            # if pt.attributes[0][0] != 0:
                            glVertex2f(pt.getX(), pt.getY())
                    y = 0
                # print(len(pontos), "pontos presentes.")
                glEnd()
                self.pontos = pontos
                self.indices = self.faz_matriz(self.pontos)  # (indices)

    def faz_matriz(self, pontos):
        aux = []
        saida = []

        if len(pontos) > 0:
            x = pontos[0].attributes[0][1]
            for i in range(len(pontos)):
                if pontos[i].attributes[0][1] == x:
                    aux.append(pontos[i].attributes[0])
                else:
                    saida.append(aux)
                    aux = []
                x = pontos[i].attributes[0][1]
            return saida
        else:
            return saida

    def faz_condicoes(self, pontos):
        saida = []

        if len(pontos) > 0 and len(pontos[0].attributes) > 0:
            for i in range(len(pontos)):
                saida.append(pontos[i].attributes[1]["temperatura"])
            print(saida)
            return saida
        else:
            return saida

    def exportJson(self):
        inds = {}
        inds["indices"] = self.indices
        inds["bc"] = self.bconditions
        jsonFile = open("coordenadas_dos_pontos_do_grid.json", "w")
        json.dump(inds, jsonFile)
        jsonFile.close()

    def criaDialogBox(self, grid=False, condicao=False):
        def submit():
            if grid:
                x = int(caixa_1.get())
                y = int(caixa_2.get())

                self.criaGrid(x, y)
                janela.destroy()
            if condicao:
                bc = int(caixa_1.get())
                self.condicoes_contorno(bc)
                janela.destroy()

        janela = Tk()
        if grid:
            label_1 = Label(janela, text="distância em pixels entre os pontos", font="Arial 12")
            label_1.place(x=1, y=2)

            botao_1 = Button(janela, width=10, text="botao", command=submit, background="dark grey")
            botao_1.place(x=85, y=120)

            caixa_1 = Entry(janela, background="white", width=10, font="Arial 12")
            caixa_1.place(x=80, y=45)

            caixa_2 = Entry(janela, background="white", width=10, font="Arial 12")
            caixa_2.place(x=80, y=80)

            janela.geometry("250x160+0+0")
            janela.mainloop()

        if condicao:
            label_1 = Label(janela, text="temperatura dos pontos selecionados", font="Arial 12")
            label_1.place(x=1, y=2)

            botao_1 = Button(janela, width=10, text="botao", command=submit, background="dark grey")
            botao_1.place(x=85, y=120)

            caixa_1 = Entry(janela, background="white", width=10, font="Arial 12")
            caixa_1.place(x=80, y=45)

            janela.geometry("250x160+0+0")
            janela.mainloop()

    def criaGrid(self, x, y):
        self.lar = x
        self.alt = y
        self.grid = True
        self.update()
        self.paintGL()
        print("Cria Grid")

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    def mousePressEvent(self, event):
        if event.button() == 1:  # botão esquerdo = 1
            self.leftMouse = True
            # print("botão esquerdo")
            self.m_buttonPressed = True
            self.m_pt0 = event.pos()
        elif event.button() == 2:  # botão direito = 2
            self.leftMouse = False
            self.m_buttonPressed = True
            self.m_pt0_f = event.pos()
            # print("botão direito")

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.pos()
            self.m_pt1_f = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
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

            if self.retangular:
                self.m_model.setCurve(pt0_U.x(), pt0_U.y(), pt1_U.x(), pt0_U.y())
                self.m_model.setCurve(pt0_U.x(), pt0_U.y(), pt0_U.x(), pt1_U.y())
                self.m_model.setCurve(pt1_U.x(), pt1_U.y(), pt0_U.x(), pt1_U.y())
                self.m_model.setCurve(pt1_U.x(), pt1_U.y(), pt1_U.x(), pt0_U.y())

                self.hecontroller.insertSegment([pt0_U.x(), pt0_U.y(), pt1_U.x(), pt0_U.y()], self.tol)
                self.hecontroller.insertSegment([pt0_U.x(), pt0_U.y(), pt0_U.x(), pt1_U.y()], self.tol)
                self.hecontroller.insertSegment([pt1_U.x(), pt1_U.y(), pt0_U.x(), pt1_U.y()], self.tol)
                self.hecontroller.insertSegment([pt1_U.x(), pt1_U.y(), pt1_U.x(), pt0_U.y()], self.tol)
                self.retangular = False
            else:
                self.m_model.setCurve(pt0_Ux, pt0_Uy, pt1_Ux, pt1_Uy)
                self.hecontroller.insertSegment([pt0_Ux, pt0_Uy, pt1_Ux, pt1_Uy], self.tol)

            self.m_buttonPressed = False
            self.m_pt0.setX(0.0)
            self.m_pt0.setY(0.0)
            self.m_pt1.setX(0.0)
            self.m_pt1.setY(0.0)
            self.update()
            self.paintGL()
        elif event.button() == 2:
            pt0f_U = self.convertPtCoordsToUniverse(self.m_pt0_f)
            pt1f_U = self.convertPtCoordsToUniverse(self.m_pt1_f)

            array = []
            for i in range(len(self.pontos)):

                # verifica a cerca sendo formada por todas as direções
                if ((pt0f_U.x() <= self.pontos[i].getX() <= pt1f_U.x()
                     and pt0f_U.y() <= self.pontos[i].getY() <= pt1f_U.y())
                        or (pt1f_U.x() <= self.pontos[i].getX() <= pt0f_U.x()
                            and pt1f_U.y() <= self.pontos[i].getY() <= pt0f_U.y())
                        or (pt1f_U.x() <= self.pontos[i].getX() <= pt0f_U.x()
                            and pt0f_U.y() <= self.pontos[i].getY() <= pt1f_U.y())
                        or (pt0f_U.x() <= self.pontos[i].getX() <= pt1f_U.x()
                            and pt1f_U.y() <= self.pontos[i].getY() <= pt0f_U.y())):
                    self.pontos[i].selected = True
                    array.append(self.pontos[i])
            print(len(self.pontos), "pontos, ", len(array), "selecionados")

            # glPointSize(3)
            # glBegin(GL_POINTS)
            # glColor3f(1.0, 0.0, 0.0)
            # for pt in array:
            #     glVertex2f(pt.getX(), pt.getY())
            # glEnd()

            self.fencedPoints = array
            self.criaDialogBox(condicao=True)

            self.m_buttonPressed = False
            self.m_pt0_f.setX(0.0)
            self.m_pt0_f.setY(0.0)
            self.m_pt1_f.setX(0.0)
            self.m_pt1_f.setY(0.0)
            self.update()
            self.paintGL()

    def condicoes_contorno(self, t):
        for point in self.pontos:
            if point in self.fencedPoints and point.attributes[0][0] != 0:
                point.attributes.append({'temperatura': t})
            else:
                point.attributes.append({'temperatura': 0})
        self.bconditions = self.faz_condicoes(self.pontos)

    def setModel(self, _model):
        self.m_model = _model

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
