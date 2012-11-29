from ROOT import *
import sys
import getopt
from RecoLuminosity.LumiDB import argparse
from combTrees import *
from CommonSelectors import *
from Selector import *

class Skimmer(object):
    """Skimmer class. Accepts TTree, cuts, etc, and sorts through them, returning unique and arbitrated event sets"""
    def __init__(self, tree, cuts, arbMode, vars, outTree, allVars=False):
        super(Skimmer, self).__init__()
        self.tree = tree
        self.cuts = cuts
        self.arbMode = arbMode
        self.vars = vars
        self.outTree = outTree
        self.allVars = allVars
        self.events = {}
    def setEvents(self):
        """Get event list"""
        self.events=uniquify(self.tree,self.cuts,self.arbMode,self.vars,self.allVars)
    def makeTree(self):
        """Return TTree composed of events"""
        return makeTree(self.events,self.outTree)
    def clear(self):
        """Clear out event dict"""
        self.events={}

#f=TFile(file,"update")
#t=f.Get("eleEleEleEleEventTree/eventTree")
#cuts["eeee"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge==0")
