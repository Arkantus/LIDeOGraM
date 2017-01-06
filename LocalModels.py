import numpy as np
import re
from ArrayConverter import ArrayConverter
from Equation import Equation
from AdjacenceMatrix import AdjacenceMatrix

class LocalModels:
    def __init__(self,modApp,file):
        self.modApp=modApp

        #Read equations from file
        stringTab = []
        eureqafile = open(file, 'r')
        for line in eureqafile:
            line = line.replace("\t", ",")
            line = line.replace("\"", "")
            line = line.replace(" = ", ",")
            line = line.replace(" ", "")
            line = line.replace("\n", "")
            line = line.split(',')
            stringTab.append(line)

        # Convert the table of String to a  list of Equations
        convertArr = []
        self.allEquations=[]
        for s in stringTab:
            fit=convertArr.append(np.float32(s[0]))
            cmplx=convertArr.append(np.float32(s[1]))
            var=convertArr.append(s[2])
            eq=convertArr.append(s[3])
            self.allEquations.append(Equation(fit,cmplx,var,eq))

        # Number of Equation for all variables taken together
        self.nbEqua = len(self.allEquations)

    def computeAdjMatrix(self):

        #Init
        nbVar=self.modApp.dataset.nbVar
        self.adj_simple=AdjacenceMatrix(self.modApp.dataset.varnames,0)
        self.adj_fit = AdjacenceMatrix(self.modApp.dataset.varnames,1)
        self.adj_cmplx = AdjacenceMatrix(self.modApp.dataset.varnames,1)
        self.nbEqForVar = np.zeros(nbVar)  # Number of equations for each variables

        self.equacolPO = []
        for e in self.allEquations: #For every equation
            for v in self.modApp.dataset.varnames :  # for every possible parents in this equation
                cont_h = len(re.findall(r'\b%s\b' % re.escape(v), e.eq))  # How many times the variable v is found in the equation e.eq
                if (cont_h > 0):  # If present, add infos in adjacence matrix
                    parentVar = v
                    offspringVar = list(self.modApp.dataset.varnames).index(e.var)
                    self.adj_simple.set(offspringVar, parentVar,self.adj_simple.get(offspringVar, parentVar+1))
                    self.adj_cmplx(offspringVar, parentVar,self.adj_cmplx.get(offspringVar, parentVar)*e.cmplx)# GEOMETRIC mean
                    self.adj_fit(offspringVar, parentVar,self.adj_fit.get(offspringVar, parentVar)*e.fit) # GEOMETRIC mean

                    self.equacolPO.append(
                        [self.allEquations[l, 0], self.allEquations[l, 1], self.allEquations[l, 2], v,
                         self.allEquations[l, 3]])
            self.nbEqForVar[list(self.modApp.dataset.varnames).index(
                self.allEquations[l, 2])] += 1  # Comptage du nombre d'équations pour chaque enfant

        self.equacolPO = ArrayConverter.convertPO(self.equacolPO)
        self.equacolPO = np.array(self.equacolPO, dtype=object)
        self.adj_cmplx = np.power(self.adj_cmplx, 1 / self.adj_simple)
        self.adj_cmplx[self.adj_simple == 0] = 0
        self.adj_fit = np.power(self.adj_fit, 1 / self.adj_simple)
        self.adj_fit[self.adj_simple == 0] = 0