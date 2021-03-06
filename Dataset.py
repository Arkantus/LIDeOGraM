import numpy as np


class Dataset:

    def __init__(self,datafile):
        datafileReader = open(datafile)
        line = datafileReader.readline()  # First line are the variables name
        self.varnames = []
        for i in line.split(','):
            self.varnames.append(i.strip())
        self.varnames=np.array(self.varnames)
        self.nbVar = len(self.varnames)
        line = datafileReader.readline()  # Second line is variables scale/step identifiers
        identvar = []
        for i in line.split(','):
            identvar.append(i.strip())
        self.variablesClass = {}
        for i in range(len(self.varnames)):
            self.variablesClass[self.varnames[i]] = identvar[i]

        self.data = []
        for line in datafileReader:
            linedata=[]
            for i in line.split(','):
                linedata.append(float(i.strip()))
            self.data.append(linedata)
        self.nbExp = len(self.data)
        self.data=np.array(self.data)




    def getAllExpsforVar(self,getvar):
        return self.data[:,self.varnames==getvar].flatten()

    def getAllVarsforExp(self,getexp):
        return dict(zip(self.varnames,self.data[getexp]))
