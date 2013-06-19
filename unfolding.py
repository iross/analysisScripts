from __future__ import division
from ROOT import *
from plotHelpers import *
from combTrees import makeTree
from RecoLuminosity.LumiDB import argparse
from sys import exit
import numpy as np
import pdb
gSystem.Load("RooUnfold-1.1.1/libRooUnfold");
#
#ROOT.gROOT.SetBatch(True)

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

def purity(trueTree,measTree,trueVar,measVar,hist,accCuts,massReq):
    """measure purity of a bin, n_{reco+gen}/n_{rec}"""
    rec={}
    gen={}
    ftemp=TFile("temp.root","recreate")
    tTree=trueTree.CopyTree(accCuts+"&&"+massReq)
    mTree=measTree.CopyTree(massReq)
    for i in tTree:
        gen[i.EVENT] = {"evt":i.EVENT, "bin":hist.FindBin(i.GetLeaf(trueVar).GetValue()), "var":i.GetLeaf(trueVar).GetValue()}
    for i in mTree:
        rec[i.EVENT] = {"evt":i.EVENT, "bin":hist.FindBin(i.GetLeaf(measVar).GetValue()), "var":i.GetLeaf(measVar).GetValue()}

    genSet=set()
    recSet=set()
    for evt in gen.keys(): genSet.add(evt)
    for evt in rec.keys(): recSet.add(evt)
    nRec=[]
    nGen=[]
    nGenRec=[]
    for n in range(hist.GetNbinsX()+1):
        nRec.append(0)
        nGen.append(0)
        nGenRec.append(0)
    genRecSet = recSet.intersection(genSet)
    for evt in recSet:
        nRec[rec[evt]['bin']-1] += 1
        if evt in genRecSet:
            if gen[evt]['bin']==rec[evt]['bin']:
                nGenRec[rec[evt]['bin']-1] += 1
    for evt in genSet:
        nGen[gen[evt]['bin']-1] += 1
    return nGen,nRec,nGenRec

def errors(central, errStat, scaleUp, scaleDown, pdf):
    """Calculate new errors, calculated as stat+syst"""
    errUp = errStat
    errDown = errStat
#    print "*********Creating new error values!**********"
#    print "Old error is: ",errStat
#    print "Central value is: %s" % str(central)
#    print "Scale up value is: %s" % str(scaleUp)
#    print "Scale down value is: %s" % str(scaleDown)
#    print "PDF value is: %s" % str(pdf)
    return [errUp, errDown]

def getBinFactors(trueTree,measTree,varTrue,bins,accCuts,args,varMeas="dummy",massreq="(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)"):
    """Returns array of size nbins with bin-by-bin (truth:measured) ratios."""
    """No mathing done between truth events and reco events! Bulk corrections only!"""
    if varMeas is "dummy": #if I'm lazy and don't pass a varMeas, assume it's the same as the true
        varMeas=varTrue
#    measHist=makeHist(measTree,varMeas,accCuts+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weightnoPU)",25,100,600,False,True,bins,binNorm=False)
#    trueHist=makeHist(trueTree,varTrue,accCuts+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(weightnoPU)",25,100,600,False,True,bins,binNorm=False)
#    measHist=makeHist(measTree,varMeas,accCuts+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weight)",25,100,600,True,True,bins,binNorm=False)
#    measHist=makeHist(measTree,varMeas,massreq+"&&((dR_z1_gz1<0.5&&dR_z2_gz2<0.5)||(dR_z1_gz2<0.5&&dR_z2_gz1<0.5))",25,100,600,True,True,bins,binNorm=False) #no acceptance cuts--they're implied in the measured trees already
    measHist=makeHist(measTree,varMeas,massreq,25,100,600,True,True,bins,binNorm=False) #no acceptance cuts--they're implied in the measured trees already, no matching Z with gen
    trueHist=makeHist(trueTree,varTrue,accCuts+"&&"+massreq,25,100,600,True,True,bins,binNorm=False)

    ngen,nrec,ngenrec=purity(trueTree,measTree,varTrue,varMeas,measHist,accCuts,massreq)
    effMethod2 = [float(ngen[i])/nrec[i] for i in range(len(ngen))]

    efficiency=measHist.Integral()/trueHist.Integral()
    print "Efficiency (%s):" % args.nice,efficiency,"=",measHist.Integral(),"/",trueHist.Integral()
    print "Efficiency (%s):" % args.nice,measTree.GetEntries(massreq)/trueTree.GetEntries(accCuts+"&&"+massreq)
    print "Efficiency (%s):" % args.nice,measTree.GetEntries(massreq),"/",trueTree.GetEntries(accCuts+"&&"+massreq)

    trueHist.Draw()
    measHist.SetLineColor(kGreen)
    measHist.Draw("hsame")
    corrs=[]
    # todo: make a histogram with the correction factors.
    corrH = TH1F("corr_H","corr_H",len(bins)-1,array('d',bins))
    corrH.GetXaxis().SetTitle(args.xTitle)
    corrH.GetYaxis().SetTitle("Truth/Reco")
    purityH = TH1F("purityH","purityH",len(bins)-1,array('d',bins))
    purityH.SetLineColor(kBlue)
    purityH.SetLineWidth(2)
    effH = TH1F("effH","effH",len(bins)-1,array('d',bins))
    effH.SetLineColor(kRed)
    effH.SetLineWidth(2)
    corrH2 = TH1F("corrH2","corrH2",len(bins)-1,array('d',bins))
    corrH2.SetLineColor(kBlack)
    corrH2.SetLineWidth(2)
    corrH.Sumw2()
    for i in range(len(bins)+1):
        rat=0.0
        try:
            rat=trueHist.GetBinContent(i)/measHist.GetBinContent(i)
            corrs.append(rat)
            corrH.SetBinContent(i,rat)
            purityH.SetBinContent(i,ngenrec[i-1]/nrec[i-1])
            effH.SetBinContent(i,ngenrec[i-1]/ngen[i-1])
            corrH2.SetBinContent(i,ngen[i-1]/nrec[i-1])
        except ZeroDivisionError:
            corrs.append(rat)
            corrH.SetBinContent(i,rat)
    can=TCanvas("can","can",600,600)
    corrH.GetYaxis().SetRangeUser(0,max(corrs)*1.10)
    print corrs
    print "new method:",effMethod2
    can.cd()
    corrH.Draw("ep")
    effH.Draw("lsame")
    purityH.Draw("lsame")
    corrH2.Draw("lsame")
    leg=TLegend(0.20,0.15,0.9,0.4)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(2)
    leg.AddEntry(corrH,"Correction","p")
    leg.AddEntry(corrH2,"Correction, method 2","l")
    leg.AddEntry(purityH,"Purity","l")
    leg.AddEntry(effH,"Efficiency","l")
    leg.Draw()
    can.SaveAs("diffDists/"+args.plotname+"_binCorrs.png")
    can.SaveAs("diffDists/"+args.plotname+"_binCorrs.pdf")
    can.SaveAs("diffDists/"+args.plotname+"_binCorrs.C")
    can.SaveAs("diffDists/"+args.plotname+"_binCorrs.root")
    pdb.set_trace()
    corrH.Delete()
    can.Delete()
    return corrs,efficiency

def applyCorrs(corrs,hist):
    """Apply the true:reco corrections, return the 'unfolded' histogram"""
    temp=hist.Clone()
    for i in range(len(corrs)):
        temp.SetBinContent(i,temp.GetBinContent(i)*corrs[i])
    return temp

def unfold():
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
    parser.add_argument('--wt',type=str,required=False,default="weight",help="weight factor (e.g. __WEIGHT__*tnp_corr)")

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
    wt=args.wt
    lumi=args.lumi

    extra="z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120&&((z1l1Pt>20&&(z1l2Pt>10||z2l1Pt>10||z2l2Pt>10))||(z1l2Pt>20&&(z1l1Pt>10||z2l1Pt>10||z2l2Pt>10))||(z2l1Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l2Pt>10))||(z2l2Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l1Pt>10)))"

    # default
    trainingFile = TFile("/scratch/iross/ZZ_wGen_proper_weights_selected.root")
#    trainingFileGen = TFile("/hdfs/store/user/iross/ZZ_wGen_proper_weights.root")
    trainingFileGen = TFile("/scratch/iross/ZZ_wGen_proper_weights.root")

    trainingSherpa = TFile("/scratch/iross/aTGC_f4_0p000_0p000_8TeV_sel_forAcc-MC_selected.root")
    trainingSherpaGen = TFile("/scratch/iross/aTGC_f4_0p000_0p000_8TeV_sel_forAcc-MC.root")

    #trainingFile = TFile("/scratch/iross/qqZZ_dev_v2.root")
    #trainingFileGen = TFile("/hdfs/store/user/iross/qqZZ_dev_v2_selected.root")

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
        extra=extra+"&&(abs(z1l1pdgId)==13&&z1l1Pt>5 || abs(z1l1pdgId)==11&& z1l1Pt>7)"
        extra=extra+"&&(abs(z1l2pdgId)==13&&z1l2Pt>5 || abs(z1l2pdgId)==11&& z1l2Pt>7)"
        extra=extra+"&&(abs(z2l1pdgId)==13&&z2l1Pt>5 || abs(z2l1pdgId)==11&& z2l1Pt>7)"
        extra=extra+"&&(abs(z2l2pdgId)==13&&z2l2Pt>5 || abs(z2l2pdgId)==11&& z2l2Pt>7)"
        extra=extra+"&&(abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4 || abs(z1l1pdgId)==11&& abs(z1l1Eta)<2.5)"
        extra=extra+"&&(abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4 || abs(z1l2pdgId)==11&& abs(z1l2Eta)<2.5)"
        extra=extra+"&&(abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4 || abs(z2l1pdgId)==11&& abs(z2l1Eta)<2.5)"
        extra=extra+"&&(abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4 || abs(z2l2pdgId)==11&& abs(z2l2Eta)<2.5)"
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
        extra=extra+"&&z1l1Pt>5&&z1l2Pt>5&&z2l1Pt>5&&z2l2Pt>5"
        extra=extra+"&&abs(z1l1Eta)<2.4&&abs(z1l2Eta)<2.4&&abs(z2l1Eta)<2.4&&abs(z2l2Eta)<2.4"
    else:
        idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*13**2)"
        idReq=idReq+"&&((abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4)||(abs(z1l1pdgId)==11&&abs(z1l1Eta)<2.5))"
        idReq=idReq+"&&((abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4)||(abs(z1l2pdgId)==11&&abs(z1l2Eta)<2.5))"
        idReq=idReq+"&&((abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4)||(abs(z2l1pdgId)==11&&abs(z2l1Eta)<2.5))"
        idReq=idReq+"&&((abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4)||(abs(z2l2pdgId)==11&&abs(z2l2Eta)<2.5))"
        extra=extra+"&&(abs(z1l1pdgId)==13&&z1l1Pt>5 || abs(z1l1pdgId)==11&& z1l1Pt>7)"
        extra=extra+"&&(abs(z1l2pdgId)==13&&z1l2Pt>5 || abs(z1l2pdgId)==11&& z1l2Pt>7)"
        extra=extra+"&&(abs(z2l1pdgId)==13&&z2l1Pt>5 || abs(z2l1pdgId)==11&& z2l1Pt>7)"
        extra=extra+"&&(abs(z2l2pdgId)==13&&z2l2Pt>5 || abs(z2l2pdgId)==11&& z2l2Pt>7)"
        extra=extra+"&&(abs(z1l1pdgId)==13&&abs(z1l1Eta)<2.4 || abs(z1l1pdgId)==11&& abs(z1l1Eta)<2.5)"
        extra=extra+"&&(abs(z1l2pdgId)==13&&abs(z1l2Eta)<2.4 || abs(z1l2pdgId)==11&& abs(z1l2Eta)<2.5)"
        extra=extra+"&&(abs(z2l1pdgId)==13&&abs(z2l1Eta)<2.4 || abs(z2l1pdgId)==11&& abs(z2l1Eta)<2.5)"
        extra=extra+"&&(abs(z2l2pdgId)==13&&abs(z2l2Eta)<2.4 || abs(z2l2pdgId)==11&& abs(z2l2Eta)<2.5)"
    print idReq
    print extra
    acceptanceCuts = extra+idReq

    print bins
    nbins=len(bins)
    xlo=bins[0]
    xhigh=bins[nbins-1]

    fout=TFile("out.root","recreate")
    tMeas=trainingFile.Get(treename)
    tTrue=trainingFileGen.Get("genlevel/genEventTree")
    tMeasSherpa=trainingSherpa.Get(treename)
    tTrueSherpa=trainingSherpaGen.Get("genlevel/genEventTree")

    dataTreeTrue = testFileGen.Get("genlevel/genEventTree")
    dataTree = testFile.Get(treename)

    # sherpa stuff for systematics
    corrsS,effS=getBinFactors(tTrueSherpa,tMeasSherpa,varTrue,bins,acceptanceCuts,args,varMeas=varMeas)
    corrs,eff=getBinFactors(tTrue,tMeas,varTrue,bins,acceptanceCuts,args,varMeas=varMeas)
    print tTrueSherpa
    print tMeasSherpa

    corrDiffs = [abs(corrsS[i]-corrs[i]) for i in range(len(corrs))]

    print "Corrections:",corrs
    print "Efficiency:",eff
    print "Corrections (Sherpa):",corrsS
    print "Efficiency: (Sherpa)",effS
    print "Correction diffs: ",corrDiffs
    print "----------------"
    print "Acceptance:",trainingFileGen.Get("genlevel/genEventTree").GetEntries(extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")")/trainingFileGen.Get("MMMM/results").GetBinContent(1),"=",trainingFileGen.Get("genlevel/genEventTree").GetEntries(extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")"),"/",trainingFileGen.Get("MMMM/results").GetBinContent(1)


    if "DATA" in args.testFile: #don't need to apply weights
#        dataHist=makeHist(dataTree,varMeas,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))",25,100,600,False,True,bins,binNorm=True)
#        dataHistTrue=makeHist(dataTree,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*0",25,100,600,False,True,bins,binNorm=True)
        dataHist=makeHist(dataTree,varMeas,"((z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))",25,100,600,False,True,bins,binNorm=True)
        dataHistTrue=makeHist(dataTree,varTrue,"((z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*0",25,100,600,False,True,bins,binNorm=True)
    else:
        dataHist=makeHist(dataTree,varMeas,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*("+wt+"*1000*"+lumi+"*1.10)",25,100,600,False,True,bins,binNorm=True)
        dataHistTrue=makeHist(dataTreeTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*("+wt+"*1000*"+lumi+"*1.10)",25,100,600,False,True,bins,binNorm=True)

    unfoldedHist=applyCorrs(corrs,dataHist)
    unfoldedHistSherpa=applyCorrs(corrsS,dataHist)

    # remove integrated lumi
    sig_fid = unfoldedHist.Integral()
    unfoldedHist.Scale(1/sig_fid)
    unfoldedHistWSyst = unfoldedHist.Clone()
    dataHist.Scale(1/dataHist.Integral())
    sig_fidS = unfoldedHistSherpa.Integral()
    unfoldedHistSherpa.Scale(1/sig_fidS)
    #dataHistTrue.Scale(1/dataHistTrue.Integral())

    # add systematics for unfolding
    for i in range(unfoldedHistWSyst.GetNbinsX()+1):
#        print "Bin %s! Nominal value is: %s" % (str(i),str(unfoldedHistWSyst.GetBinContent(i)))
#        print "Diff is %s" % str(abs(unfoldedHist.GetBinContent(i)-unfoldedHistSherpa.GetBinContent(i)))
#        print "Error was: %s" % str(unfoldedHistWSyst.GetBinError(i))
        newErrorSq = unfoldedHistWSyst.GetBinError(i)**2 + (unfoldedHistSherpa.GetBinContent(i)-unfoldedHist.GetBinContent(i))**2 # compared to sherpa unfolded
        newErrorSq = unfoldedHistWSyst.GetBinError(i)**2 + (unfoldedHist.GetBinContent(i)*0.05)**2 # flat 5%
#        print "Error now: %s" % str(newErrorSq**0.5)
        unfoldedHistWSyst.SetBinError(i,newErrorSq**0.5)


    ymax=max(unfoldedHist.GetMaximum(),unfoldedHist.GetMaximum())
    #ymax=ymax*1.05*(1+1/ymax**0.5)
    ymax=ymax*1.05*(1+ymax**0.5)

    # draw options
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
#    unfoldedHistSherpa.SetLineColor(kPink+10)

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
#    leg.AddEntry(dataHist,"Measured","l")
    leg.AddEntry(unfoldedHist,"Unfolded Data","pe")
    leg.AddEntry(unfoldedHistWSyst,"Total Error","f")
#    leg.AddEntry(unfoldedHistSherpa,"Unfolded via Sherpa","l")

    print "--------"+args.nice+"-----------"
    print "Data:",dataHist.Integral()
    print "True:",dataHistTrue.Integral()
    if "DATA" not in args.testFile: print "Efficiency:",dataHist.Integral()/dataHistTrue.Integral()
    print "Unfolded:",unfoldedHist.Integral()
    print "-------------------"

    if debug:
        trainingMeas=makeHist(tMeas,varMeas,"((z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*("+wt+"*"+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
        trainingTrue=makeHist(tTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weight*"+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
        trainingTrueScaleUp=makeHist(tTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weight*scale_up*"+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
        trainingTrueScaleDown=makeHist(tTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weight*scale_down*"+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
        trainingTruePDF=makeHist(tTrue,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*(weight*mstw8_ct10*"+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)

        #todo: set errors in each bin to be stat+syst(scale up, PDF)
        for i in range(trainingTrue.GetNbinsX()+1):
            errors(trainingTrue.GetBinContent(i), trainingTrue.GetBinError(i), trainingTrueScaleUp.GetBinContent(i), trainingTrueScaleDown.GetBinContent(i), trainingTruePDF.GetBinContent(i))


        trainingTrue.SetLineColor(kAzure-4)
        trainingTrue.SetFillColor(kAzure-9)
        trainingMeas.SetLineColor(kBlack)
        leg.AddEntry(trainingTrue,"POWHEG+gg","f")
#        leg.AddEntry(trainingMeas,"training measured","l")
        trainingTrue.SetLineWidth(2)
        trainingTrue.SetMarkerSize(0.00001)
        trainingTrue.Scale(1/trainingTrue.Integral())
        trainingTrue.Draw("h same")

        # true/meas SHERPA
#        trainingTrueSherpa=makeHist(tTrueSherpa,varTrue,"("+extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+"))*("+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
#        trainingTrueSherpa.SetLineColor(kGreen+3)
#        trainingTrueSherpa.SetLineWidth(3)
#        trainingTrueSherpa.SetMarkerSize(0.00001)
#        trainingTrueSherpa.Scale(1/trainingTrueSherpa.Integral())
#        trainingMeasSherpa=makeHist(tMeasSherpa,varMeas,"((z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120))*("+str(lumi)+"*1000)",25,100,600,False,True,bins,binNorm=True)
#        trainingMeasSherpa.SetLineColor(kGreen-7)
#        trainingMeasSherpa.SetLineWidth(3)
#        trainingMeasSherpa.SetMarkerSize(0.00001)
#        trainingMeasSherpa.Scale(1/trainingMeasSherpa.Integral())

#        trainingTrueSherpa.Draw("h same")
#        trainingMeasSherpa.Draw("h same")
#        leg.AddEntry(trainingTrueSherpa,"SHERPA true","l")
#        leg.AddEntry(trainingMeasSherpa,"SHERPA measured","l")

        trainingMeas.Scale(1/trainingMeas.Integral())
        trainingMeas.SetLineWidth(2)
        trainingMeas.SetMarkerSize(0.00001)
#        trainingMeas.Draw("h same")
    unfoldedHistWSyst.SetFillColor(kGray+2)
    unfoldedHistWSyst.SetFillStyle(3004)
    unfoldedHistWSyst.Draw("e2same") #draw errors as rectangle
    #redraw data hists
#    dataHist.Draw("h same")
    unfoldedHist.Draw("p same")
#    unfoldedHistSherpa.Draw("h same")
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
    tempWSyst=unfoldedHistWSyst.Clone()
    tempWSyst.SetMarkerSize(1.0)
    tempWSyst.SetFillColor(kGray+2)
    tempWSyst.SetFillStyle(3004)
    temp.SetLineColor(kBlack)
    temp.Divide(trainingTrue)
    tempWSyst.Divide(trainingTrue)
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
    tempWSyst.Draw("e2same")
    temp.Draw("psame")
    can.cd()
    can.SaveAs("diffDists/"+args.plotname+".png")
    can.SaveAs("diffDists/"+args.plotname+".root")
    can.SaveAs("diffDists/"+args.plotname+".C")
    can.Delete()
    pass

    SetOwnership(pad1,False)
    SetOwnership(pad2,False)

    trainingFile.Close()
    trainingFileGen.Close()
    testFile.Close()
    testFileGen.Close()
    fout.Close()

def main():
    """docstring for main"""
    unfold()

if __name__ == "__main__":
    main()
