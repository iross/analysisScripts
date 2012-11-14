from simplePlots import *

class Plotter():
    """Class for handling 1D plots"""
    def __init__(self, data, treesToStack):
        self.data = data
        self.treesToStack = treesToStack
    def comp(self,var,bins):
        compTrees([self.data,self.treesToStack[0]],var,bins,names=["data","test"])
    def checkEntries(self):
        print "Data:",self.data.GetEntries()
        for i in self.treesToStack:
            print i,i.GetEntries()

