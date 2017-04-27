#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QCoreApplication
from classes.CanvGraph import CanvGraph
from classes.FramAction import FramAction
from classes.ClassGraph import ClassGraph
from classes.MenuBar import MenuBar
import copy
from classes.ToolMenu import ToolMenu
from functools import reduce

class Window(QtGui.QMainWindow):

    def __init__(self, graph: ClassGraph,fctToCall):
        self.fctToCall=fctToCall
        self.graphReady = False

        QtGui.QMainWindow.__init__(self)
        self.mainWid = QtGui.QWidget(self)
        self.setWindowTitle("Class management")
        self.gridLayout = QtGui.QGridLayout(self.mainWid)
        self.mainWid.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setCentralWidget(self.mainWid)

        self.graph = copy.copy(graph)
        self.initialGraph = graph

        self.canv = CanvGraph(graph)
        self.canv.addObserver(self)
        self.frame = FramAction(graph.unboundNode)

        self.frame.button1.addObserver(self)
        self.frame.button2.addObserver(self)

        self.gridLayout.setSpacing(5)
        self.canv.setMinimumSize(200, 200)

        self.saveButton = QtGui.QPushButton("Validate")

        self.saveButton.clicked.connect(lambda: self.setReady(self.canv.graph))


        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(lambda: self.setReady(self.initialGraph))

        self.gridLayout.addWidget(self.canv, 0, 0, 2, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.saveButton, 1, 2, 1, 1)


        self.selectedNode = None
        MenuBar(self)

        self.show()
        #self.exec()

    def notify(self, selectedNode=None, keepSelected = False):
        if keepSelected:
            selectedNode = self.selectedNode
        else:
            self.selectedNode = selectedNode
        self.canv.paint(selectedNode)
        self.frame.setListsValues(self.graph.unboundNode, selectedNode)
        QCoreApplication.processEvents()

    def setReady(self, graph):
        self.graph = graph
        self.graphReady = True
        print("pret !")
        self.fctToCall(self.graph)
        self.close()