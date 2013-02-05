'''
File: embedBGPlots.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Calculate the BG histograms and embed them in a root file. Use after running through makeAnalysisTrees
'''

from RecoLuminosity.LumiDB import argparse
from ROOT import TFile
from simplePlots import applyFakes

def writeBGhist(f,state,customBinning,bins):
    """Write the final background hist to the TFile"""
    hists=applyFakes(f,extra="&&z1Mass>81&&z1Mass<101",lowZ1=True,customBinning=customBinning,bins=bins)
    # if mmee, add eemm
    if state=="eemm" or state=="mmee": #add together Zee_real+Zmm_fake and Zmm_real+Zee_fake contributions
        stateBG=hists['mmeeAIFinal'].Clone()
        stateBG.Add(hists['mmeeIAFinal'])
        stateBG.Add(hists['eemmAIFinal'])
        stateBG.Add(hists['eemmIAFinal'])
        stateBG.Add(hists['mmeeAAFinal'],-1)
        stateBG.Add(hists['eemmAAFinal'],-1)
    else:
        stateBG=hists[state+'AIFinal'].Clone()
        stateBG.Add(hists[state+'IAFinal'])
        stateBG.Add(hists[state+'AAFinal'],-1)

    print hists[state+'AIFinal'].Integral(),"+",hists[state+'IAFinal'].Integral(),"-",hists[state+'AAFinal'].Integral()
    print stateBG.Integral()
    #todo: fix errors
    stateBG.SetTitle(state+"BG")
    stateBG.SetName(state+"BG")
    stateBG.Write()
    pass

parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
parser.add_argument('--file',type=str,required=True,default='',help='Input file')

args = parser.parse_args()

file=args.file
f=TFile(file,"UPDATE")

binning=[100,200,300,400,600,800]
writeBGhist(f,"eeee",True,binning)
writeBGhist(f,"mmee",True,binning)
writeBGhist(f,"mmmm",True,binning)

f.Close()

