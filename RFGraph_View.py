#-*- coding: utf-8
from PyQt4 import QtGui, QtCore

from NetworkCanvas import NetworkCanvas
from EqTableCanvas import EqTableCanvas
from FitCanvas import FitCanvas

# TODO Crée tout les boutons (or graphes + équations)
class RFGraph_View(QtGui.QMainWindow):

    def __init__(self,modApp):

        self.modApp=modApp

        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("LSN")
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)
        self.networkGUI = NetworkCanvas(self.modApp, self)
        self.gridLayout.addWidget(self.networkGUI, 1, 0, 8, 60)

        self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtGui.QLabel('Edges importance : ')
        self.gridLayout.addWidget(self.adjThreshold_lab, 8, 0, 1, 2)
        self.gridLayout.addWidget(self.adjThreshold_slider, 8, 2, 1, 57)

        self.comprFitCmplx_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.comprFitCmplx_slider.setValue(self.modApp.comprFitCmplxVal * 100)
        self.comprFitCmplx_lab = QtGui.QLabel('Compromise : ')
        self.gridLayout.addWidget(self.comprFitCmplx_lab, 9, 0)
        self.comprFitCmplx_lab_cmplx = QtGui.QLabel('Complexity')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_cmplx, 9, 1)
        self.gridLayout.addWidget(self.comprFitCmplx_slider, 9, 2, 1, 57)
        self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 9, 59, 1, 1)
        self.selectContrTxt = QtGui.QLabel('')
        self.gridLayout.addWidget(self.selectContrTxt, 0, 25, 2, 12)

        self.eqTableGUI = EqTableCanvas(self.modApp)

        self.gridLayout.addWidget(self.eqTableGUI, 1, 60, 6, 60)

        self.fitGUI = FitCanvas(self.modApp)
        self.gridLayout.addWidget(self.fitGUI, 7, 60, 6, 60)

        self.buttonCompromis = QtGui.QPushButton('Compromise', self)
        self.buttonFitness = QtGui.QPushButton('Fitness', self)
        self.buttonComplexite = QtGui.QPushButton('Complexity', self)
        self.buttonOptUgp3 = QtGui.QPushButton('µGP Optimisation', self)
        self.buttonShowModGlobal = QtGui.QPushButton('Show Global Model', self)
        self.buttonHideModGlobal = QtGui.QPushButton('Hide Global Model', self)
        self.buttonChangerEq = QtGui.QPushButton('Change equation', self)
        self.buttonRemoveLink = QtGui.QPushButton('Remove Link', self)
        self.buttonReinstateLink = QtGui.QPushButton('Reinstate', self)
        self.buttonHelp = QtGui.QPushButton('Help', self)

        self.gridLayout.addWidget(self.buttonCompromis, 10, 0, 1, 15)
        self.gridLayout.addWidget(self.buttonFitness, 10, 15, 1, 15)
        self.gridLayout.addWidget(self.buttonComplexite, 10, 30, 1, 15)
        self.gridLayout.addWidget(self.buttonOptUgp3, 10, 45, 1, 15)
        self.gridLayout.addWidget(self.buttonShowModGlobal, 11, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonHideModGlobal, 11, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonChangerEq, 12, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonRemoveLink, 12, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonReinstateLink, 0, 12, 1, 8)
        self.gridLayout.addWidget(self.buttonHelp, 0, 120, 1, 12)

        self.scrolledList = QtGui.QComboBox(self)
        self.gridLayout.addWidget(self.scrolledList, 0, 0, 1, 12 )
        self.scrolledList.addItem("Select link to reinstate")

        self.font = QtGui.QFont('Liberation Sans Narrow')
        self.font.setPointSize(12)
        self.setFont(self.font)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.show()
        self.updateView()


    def updateView(self):
        self.networkGUI.updateView()
        self.fitGUI.updateView()
        self.eqTableGUI.updateView()