'''
File: embedBGPlots.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Calculate the BG histograms and embed them in a root file. Use after running through makeAnalysisTrees.
'''

from RecoLuminosity.LumiDB import argparse
from ROOT import *
from plotHelpers import applyFakes, makeBGhist, measureLeptonFakes

parser = argparse.ArgumentParser(description='Shove the final BG histograms into the data root file.')
parser.add_argument('--file',type=str,required=True,default='',help='Input file')

args = parser.parse_args()

file=args.file
f=TFile(file,"UPDATE")

frs=measureLeptonFakes("DATA_2012_noMuEG2012v_8TeV_final_selected.root",extra="&&z1Mass>81&&z1Mass<101")

#binning=[100,200,300,400,600,800]
#binning=[100,200,300,400,600,800,810]
#binning=range(100,600,10)
binning=[100,200,300,400,500,600,700,800,900,1000,1100]
eeeeBG=makeBGhist(f,"eeee","mass",True,binning,extra="bestZmass>60&&bestZmass<120&&subBestZmass>60&&subBestZmass<120",binNorm=False,fakeRates=frs)
f.cd()
eeeeBG.Write()
mmeeBG=makeBGhist(f,"mmee","mass",True,binning,extra="bestZmass>60&&bestZmass<120&&subBestZmass>60&&subBestZmass<120",binNorm=False,fakeRates=frs)
f.cd()
mmeeBG.Write()
mmmmBG=makeBGhist(f,"mmmm","mass",True,binning,extra="bestZmass>60&&bestZmass<120&&subBestZmass>60&&subBestZmass<120",binNorm=False,fakeRates=frs)
f.cd()
mmmmBG.Write()

f.Close()

