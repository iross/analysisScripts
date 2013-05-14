from ROOT import *
from plotHelpers import *
from combTrees import makeTree
from RecoLuminosity.LumiDB import argparse
from sys import exit
import numpy as np
gSystem.Load("RooUnfold-1.1.1/libRooUnfold");

ROOT.gROOT.SetBatch(True)

debug=True
#debug=False

def parseBins(string):
    """Parses a string and returns a list corresponding to bin boundaries for the target hist"""
    bins=[]
    if "range" in string: #
        bins=eval(string)
    elif "," in string: # if comma separated, make list out of 'em
        bins=[float(i) for i in string.split(',')]
    return bins

parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
parser.add_argument('--tree',type=str,required=True,default='',help='Tree name')
parser.add_argument('--nice',type=str,required=True,default='',help='Nice name (for legend label)')
parser.add_argument('--lumi',type=float,required=True,default=19.6,help='Nice name (for legend label)')
parser.add_argument('--vartrue',type=str,required=True,default='',help='var name (true tree)')
parser.add_argument('--varmeas',type=str,required=True,default='',help='var name (meas tree)')
parser.add_argument('--xTitle',type=str,required=True,default='',help='var name (meas tree)')
parser.add_argument('--legX',type=float,required=False,default=0.6,help='')
parser.add_argument('--legY',type=float,required=False,default=0.5,help='')
parser.add_argument('--plotname',type=str,required=False,default='plotplot',help='[plotname].png')
parser.add_argument('--testFile',type=str,required=False,default='sherpa_sm_selected.root',help='test file name')
parser.add_argument('--testGen',type=str,required=False,default='/scratch/iross/temp_sherpa.root',help='test gen file name (since I\'m stupidly not storing genEventTree in the cleaned ntuples right now)')
parser.add_argument('--bins',type=parseBins,required=False,default=[],help='bins')

args = parser.parse_args()

treename=args.tree
treeNiceName=args.nice
varTrue=args.vartrue
varMeas=args.varmeas
bins=args.bins
xTitle=args.xTitle
legX=args.legX
legY=args.legY
testFile = TFile(args.testFile)
testFileGen = TFile(args.testGen)
lumi=args.lumi

extra="z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120&&((z1l1Pt>20&&(z1l2Pt>10||z2l1Pt>10||z2l2Pt>10))||(z1l2Pt>20&&(z1l1Pt>10||z2l1Pt>10||z2l2Pt>10))||(z2l1Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l2Pt>10))||(z2l2Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l1Pt>10)))"

trainingFile = TFile("/scratch/iross/ZZ_wGen_proper_weights_selected.root")
trainingFileGen = TFile("/scratch/iross/ZZ_wGen_proper_weights.root")

#testFile = TFile("ZZJets4L_8TeV_final_wGen_selected.root")
#testFileGen = TFile("/scratch/iross/ZZJets4L_8TeV_final_wGen-MC.root")

#testFile=trainingFile
#testFileGen=trainingFileGen

idReq="1"
if "llll" in treename:
    idReq="&&(((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*13**2))||((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(13**2*13**2))||((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*11**2)))"
    idReq=idReq+"&&((abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4)||(abs(z1l1pdgId)==11&&abs(z1l1Eta)<2.5))"
    idReq=idReq+"&&((abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4)||(abs(z1l2pdgId)==11&&abs(z1l2Eta)<2.5))"
    idReq=idReq+"&&((abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4)||(abs(z2l1pdgId)==11&&abs(z2l1Eta)<2.5))"
    idReq=idReq+"&&((abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4)||(abs(z2l2pdgId)==11&&abs(z2l2Eta)<2.5))"
elif "eeee" in treename:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*11**2)"
    idReq=idReq+"&&(abs(z1l1pdgId)==11&&abs(z1l1Eta)<2.5)"
    idReq=idReq+"&&(abs(z1l2pdgId)==11&&abs(z1l2Eta)<2.5)"
    idReq=idReq+"&&(abs(z2l1pdgId)==11&&abs(z2l1Eta)<2.5)"
    idReq=idReq+"&&(abs(z2l2pdgId)==11&&abs(z2l2Eta)<2.5)"
    extra=extra+"&&z1l1Pt>7&&z1l2Pt>7&&z2l1Pt>7&&z2l2Pt>7"
    extra=extra+"&&abs(z1l1Eta)<2.5&&abs(z1l2Eta)<2.5&&abs(z2l1Eta)<2.5&&abs(z2l2Eta)<2.5"
elif "mmmm" in treename:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(13**2*13**2)"
    idReq=idReq+"&&(abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4)"
    idReq=idReq+"&&(abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4)"
    idReq=idReq+"&&(abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4)"
    idReq=idReq+"&&(abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4)"
#    extra=extra+"&&z1l1Pt>5&&z1l2Pt>5&&z2l1Pt>5&&z2l2Pt>5"
#    extra=extra+"&&abs(z1l1Eta)<2.4&&abs(z1l2Eta)<2.4&&abs(z2l1Eta)<2.4&&abs(z2l2Eta)<2.4"
else:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*13**2)"
    idReq=idReq+"&&((abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4)||(abs(z1l1pdgId)==11&&abs(z1l1Eta)<2.5))"
    idReq=idReq+"&&((abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4)||(abs(z1l2pdgId)==11&&abs(z1l2Eta)<2.5))"
    idReq=idReq+"&&((abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4)||(abs(z2l1pdgId)==11&&abs(z2l1Eta)<2.5))"
    idReq=idReq+"&&((abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4)||(abs(z2l2pdgId)==11&&abs(z2l2Eta)<2.5))"

print bins
nbins=len(bins)
xlo=bins[0]
xhigh=bins[nbins-1]

fout=TFile("out.root","update")
tMeas=trainingFile.Get(treename)
tTrue=trainingFileGen.Get("genlevel/genEventTree")

dataTreeTrue = testFileGen.Get("genlevel/genEventTree")
dataTree = testFile.Get(treename)

def getBinFactors(trueTree,measTree,varTrue,bins,varMeas="dummy"):
    """Returns array of size nbins with bin-by-bin (truth:measured) ratios."""
    """No mathing done between truth events and reco events! Bulk corrections only!"""
    if varMeas is "dummy": #if I'm lazy and don't pass a varMeas, assume it's the same as the true
        varMeas=varTrue
#    measHist=makeHist(measTree,varMeas,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weightnoPU)",25,100,600,False,True,bins,binNorm=False)
#    trueHist=makeHist(trueTree,varTrue,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(weightnoPU)",25,100,600,False,True,bins,binNorm=False)
    measHist=makeHist(measTree,varMeas,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(1)",25,100,600,False,True,bins,binNorm=False)
    trueHist=makeHist(trueTree,varTrue,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(1)",25,100,600,False,True,bins,binNorm=False)
    efficiency=measHist.Integral()/trueHist.Integral()
    print "Efficiency:",efficiency,"=",measHist.Integral(),"/",trueHist.Integral()
    corrs=[]
    for i in range(len(bins)):
        rat=0.0
        try:
            rat=trueHist.GetBinContent(i)/measHist.GetBinContent(i)
            corrs.append(rat)
        except ZeroDivisionError:
            corrs.append(rat)
    return corrs,efficiency

def applyCorrs(corrs,hist):
    """Apply the true:reco corrections, return the 'unfolded' histogram"""
    temp=hist.Clone()
    for i in range(len(corrs)):
        temp.SetBinContent(i,temp.GetBinContent(i)*corrs[i])
    return temp

corrs,eff=getBinFactors(tTrue,tMeas,varTrue,bins,varMeas=varMeas)
print "Corrections:",corrs
print "Efficiency:",eff
print "Acceptance:",trainingFileGen.Get("genlevel/genEventTree").GetEntries(extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")")/trainingFileGen.Get("MMMM/results").GetBinContent(1),"=",trainingFileGen.Get("genlevel/genEventTree").GetEntries(extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")"),"/",trainingFileGen.Get("MMMM/results").GetBinContent(1)


if "DATA" in args.testFile: #don't need to apply weights
    dataHist=makeHist(dataTree,varMeas,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))",25,100,600,False,True,bins,binNorm=True)
    dataHistTrue=makeHist(dataTree,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*0",25,100,600,False,True,bins,binNorm=True)
else:
    dataHist=makeHist(dataTree,varMeas,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*(weightnoPU*1000*19.3*1.10)",25,100,600,False,True,bins,binNorm=True)
    dataHistTrue=makeHist(dataTreeTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weightnoPU*1000*19.3*1.10)",25,100,600,False,True,bins,binNorm=True)

unfoldedHist=applyCorrs(corrs,dataHist)

# remove integrated lumi
unfoldedHist.Scale(1/unfoldedHist.Integral())
dataHist.Scale(1/dataHist.Integral())
#dataHistTrue.Scale(1/dataHistTrue.Integral())

ymax=max(unfoldedHist.GetMaximum(),unfoldedHist.GetMaximum())
#ymax=ymax*1.05*(1+1/ymax**0.5)
ymax=ymax*1.05*(1+ymax**0.5)

can=TCanvas("can","can",600,600)
pad1 = TPad("pad1","pad1",0,0.2,1,1);
pad1.SetBottomMargin(0.125);
pad1.SetTopMargin(0.1);
pad1.SetRightMargin(0.07);
pad1.SetLeftMargin(0.18)
pad1.Draw()
pad1.cd()
unfoldedHist.GetYaxis().SetRangeUser(0,ymax)
unfoldedHist.GetYaxis().SetTitle("1/#sigma_{fid} d #sigma_{fid}/d("+xTitle+")")
unfoldedHist.GetXaxis().SetTitle(xTitle)
unfoldedHist.Draw('p')

dataHist.SetLineColor(kRed)
dataHist.SetLineWidth(2)
dataHist.SetMarkerSize(0.00001)
#dataHist.Draw("h same")
dataHistTrue.SetLineColor(kBlue)
dataHistTrue.SetLineWidth(2)
dataHistTrue.SetMarkerSize(0.00001)
#dataHistTrue.Draw("h same")

leg=TLegend(legX,legY,legX+0.3,legY+0.25)

#leg.SetHeader(treeNiceName)
#legend
leg.SetFillColor(kWhite)
#leg.AddEntry(dataHistTrue,"Truth","l")
#leg.AddEntry(dataHist,"Measured","l")
leg.AddEntry(unfoldedHist,"Unfolded","p")

print "--------"+args.nice+"-----------"
print "Data:",dataHist.Integral()
print "True:",dataHistTrue.Integral()
if "DATA" not in args.testFile: print "Efficiency:",dataHist.Integral()/dataHistTrue.Integral()
print "Unfolded:",unfoldedHist.Integral()
print "-------------------"

if debug:
    trainingMeas=makeHist(tMeas,varMeas,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*(weightnoPU*19.3*1000)",25,100,600,False,True,bins,binNorm=True)
    trainingTrue=makeHist(tTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weightnoPU*19.3*1000)",25,100,600,False,True,bins,binNorm=True)
    trainingTrue.SetLineColor(kAzure-4)
    trainingTrue.SetFillColor(kAzure-9)
    trainingMeas.SetLineColor(kBlack)
    leg.AddEntry(trainingTrue,"POWHEG+gg","f")
#    leg.AddEntry(trainingMeas,"training measured","l")
    trainingTrue.SetLineWidth(2)
    trainingTrue.SetMarkerSize(0.00001)
    trainingTrue.Scale(1/trainingTrue.Integral())
    trainingTrue.Draw("h same")
    trainingMeas.Scale(1/trainingMeas.Integral())
    trainingMeas.SetLineWidth(2)
    trainingMeas.SetMarkerSize(0.00001)
#    trainingMeas.Draw("h same")
#redraw data hists
#dataHist.Draw("h same")
unfoldedHist.Draw("p same")
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.Draw()
binrange=bins[len(bins)-1]-bins[0]
tex = TLatex(bins[0]+0.02*binrange,ymax*1.05,"CMS Preliminary 2012");
tex2 = TLatex(bins[0]+0.62*binrange,ymax*1.05,str(lumi)+"fb^{-1}, \sqrt{s}=8 TeV");
tex.Draw()
tex2.Draw()
pad1.RedrawAxis()
can.cd()
pad2 = TPad("pad2","pad2",0,0,1,0.2);
pad2.SetBottomMargin(0.125);
pad2.SetTopMargin(0.05);
pad2.SetRightMargin(0.07);
pad2.SetLeftMargin(0.18)
pad2.Draw()
pad2.cd()
temp=unfoldedHist.Clone()
temp.SetMarkerSize(1.0)
temp.SetLineColor(kBlack)
temp.Divide(trainingTrue)
temp.GetYaxis().SetRangeUser(0.0,2.0)
temp.GetYaxis().SetTitle("Data/MC")
temp.GetYaxis().SetTitleSize(0.20)
temp.GetXaxis().SetTitleSize(0.00)
temp.GetYaxis().SetTitleOffset(0.25)
temp.GetYaxis().SetNdivisions(4)
temp.SetLabelSize(0.0,"X")
temp.SetLabelSize(0.13,"Y")

#temp.SetLabelOffset(0.25,"Y")
temp.Draw()
can.cd()
can.SaveAs(args.plotname+".png")

