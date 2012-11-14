#!/usr/bin/env python
from ROOT import *
from array import *
from CommonSelectors import *

import logging,Colorer
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT.gROOT.ProcessLine(".X CMSStyle.C")

def makeHist(tree, var, cuts, nbin, xmin, xmax, overflow=False, customBinning=False, bins=[0,1]):
#	logging.debug("Making hist with %i bins, from %d to %d",nbin,xmin,xmax)
	h = TH1F("temp","temp",nbin,xmin,xmax)
#	h.Sumw2()
	if customBinning:
		h = TH1F("temp","temp",len(bins)-1,array('d',bins))
		h.Sumw2()
		nbin=len(bins)-1
	tree.Draw(var+">>temp",cuts,"")
	if overflow:
		logging.debug("Adding overflow bin.")
#		print "\twas",h.GetBinContent(nbin)
#		print "\twas",h.GetBinContent(nbin+1)
		h.SetBinContent(nbin,h.GetBinContent(nbin)+h.GetBinContent(nbin+1))
#		print "\tnow",h.GetBinContent(nbin)
	return h

def makeHist2D(tree, cuts, varx, nbinx, xmin, xmax, vary, nbiny, ymin, ymax, customBinning=False, bins=[0,1]):
#	logging.debug("Making hist with %i bins, from %d to %d",nbin,xmin,xmax)
	h = TH2F("h","h",nbinx,xmin,xmax,nbiny,ymin,ymax)
	h.Sumw2()
	if customBinning:
		#todo: 2d custom binning
		h = TH1F("temp","temp",len(bins)-1,array('d',bins))
		h.Sumw2()
		nbin=len(bins)-1
	tree.Draw(vary+":"+varx+">>h",cuts,"")
	return h

def addTree(file, treename, vars=["z1Mass","z1Pt","z2Mass","mass","RUN","EVENT","__WEIGHT__","__WEIGHT__noPU","__CORR__","__CORRnoHLT__","met"]):
	"""Add a tree. Quick and dirty implementation to add pseudodata"""
	import numpy as N
	f=TFile(file,"UPDATE")
	t=TTree(treename,treename)
	n={}
	for var in vars:
		n[var]=N.zeros(1,dtype=float)
		t.Branch(var,n[var],var+'/d')
		n[var][0]=-1.0
	n["mass"][0]=200.895
	n["z1Mass"][0]=91.191
	n["z2Mass"][0]=90.401
	n["RUN"][0]=191226
	n["EVENT"][0]=1820521419
	t.Fill()
	t.Write()
	f.Close()

def compTrees(trees,var,bins,cuts="1",names=[""],drawOptions="h"):
	"""Compare variables from some trees"""
	can=TCanvas("can","can",600,600)
	leg=TLegend(0.6,0.6,0.9,0.9)
	colors=[kBlack,kBlue,kRed,kGreen,kCyan,kRed-9]
	markers=[20,22,24,26,29,34]
	nbin=len(bins)
	xmin=min(bins)
	xmax=max(bins)
	h={}
	maxY=0
	i=0
	for tree in trees:
		h[tree.GetDirectory().GetName()+names[i]]=makeHist(tree, var, cuts, nbin, xmin, xmax, False, True, bins)
		maxY=max(maxY,h[tree.GetDirectory().GetName()+names[i]].GetMaximum()/h[tree.GetDirectory().GetName()+names[i]].Integral())
		i=i+1
	i=0
	for hist in h:
		h[hist].Scale(1/h[hist].Integral())
		h[hist].SetLineColor(colors[i])
		h[hist].SetMarkerStyle(markers[i])
		h[hist].SetMarkerColor(colors[i])
		h[hist].SetLineWidth(2)
		print i
		h[hist].SetName(names[i])
		h[hist].SetTitle(names[i])
		leg.AddEntry(h[hist])
		if i==0:
			h[hist].GetXaxis().SetTitle(var)
			h[hist].GetYaxis().SetRangeUser(0,maxY+0.05)
			if bins[0]-bins[1] == bins[len(bins)-2]-bins[len(bins)-1]: # if spaced evenly
				div=(float(bins[len(bins)-1])-float(bins[0]))/(len(bins)-1)
				h[hist].GetYaxis().SetTitle("Events / %.2f" %div)
				h[hist].GetYaxis().SetRange(0,15)
			else:
				h[hist].GetYaxis().SetTitle("Events")
				h[hist].GetYaxis().SetRange(0,15)
			h[hist].Draw(drawOptions)
		else:
			print "drrrrrawing"
			h[hist].Draw(drawOptions+"same")
		i+=1
		print h[hist].Integral()
	leg.SetFillColor(kWhite)
	leg.SetShadowColor(0)
	leg.Draw()
	raw_input("Make changes?")
	can.SaveAs("comp"+var+".png")
	return can

def getYields(file, lumi, cuts=""):
	fin = TFile(file)
	if cuts != "":
		cuts="*"+cuts
	for t in fin.GetListOfKeys():
		tree = t.GetName()
		t=fin.Get(tree)
		h=makeHist(t, "z1Mass", "(1)*__WEIGHT__noPU*"+lumi+cuts, 60, 60, 120)
		print tree,"--",h.Integral()
		h.Delete()

def mergeTrees(trees, treeName):
	"""Merge list of trees into a new tree, return it"""
	newChain=TChain(treeName)
	for tree in trees:
		#Add("file/tree")
		newChain.Add(tree)
	try:
		newChain.SetName(treeName)
		newChain.SetTitle(treeName)
	except ReferenceError:
		print "Created tree empty. :("
		return
	newTree=newChain.CloneTree()
	newTree.SetName(treeName)
	newTree.SetTitle(treeName)
	print newTree.ls()
	return newTree

def fit(hist):
	logging.debug("Fitting histogram %s",hist.GetTitle())	
	gSystem.Load("libRooFit")
	mass = RooRealVar("mass","mass",0,120)
	mean = RooRealVar("mean","mean",0,60)
	sigma = RooRealVar("sigma","sigma",0,10)
	Yield = RooRealVar("yield","yield",50,0,1000)
#	hist = TH1F("hist","hist",12,0,120)

#	tree.Draw("z2Mass>>hist",defineCuts(common.cuts(),stdIso("z1l1",0.275,"ele",True),stdIso("z1l2",0.275,"ele",True),"!"+stdIso("z2l1",0.275,"mu"),"!"+stdIso("z2l2",0.275,"mu"),z1Sip.cuts(),"z2Charge==0&&z2Mass>12&&z2Mass<120"))

	print hist.Integral(),"seen in data"
	land = RooLandau("land","land",mass,mean,sigma)
	data = RooDataHist("data","data",RooArgList(mass),hist)

	totalPdf = RooAddPdf("totalPdf","total",RooArgList(land),RooArgList(Yield))

	totalPdf.fitTo(data)
	C = mass.frame()
	data.plotOn(C)
	totalPdf.plotOn(C)
	C.Draw()
	raw_input("How's that fit look?")
	print mean.getVal(),"+-",mean.getErrorHi(),mean.getErrorLo()
	print sigma.getVal(),"+-",sigma.getErrorHi(),sigma.getErrorLo()
	mass.setRange("onshellReg",60,120)
	integral = totalPdf.createIntegral(RooArgSet(mass),RooArgSet(mass),"onshellReg")
	expected = integral.getVal()*Yield.getVal()
	print "Expected in on-shell region:",expected

def measureLeptonFakes(file, extra="", var="z2l1pt", customBinning=False, bins=[0,1]):
	logging.debug('Measuring fakes from file:%s',file)
	file = TFile(file)
	if customBinning:
		enum = TH1F("enum","enum",len(bins)-1,array('d',bins))
		eden = TH1F("eden","eden",len(bins)-1,array('d',bins))
		mnum = TH1F("mnum","mnum",len(bins)-1,array('d',bins))
		mden = TH1F("mden","mden",len(bins)-1,array('d',bins))
	else: 
		enum = TH1F("enum","enum",12,0,120)
		eden = TH1F("eden","eden",12,0,120)
		mnum = TH1F("mnum","mnum",12,0,120)
		mden = TH1F("mden","mden",12,0,120)
#	print defineCuts(common.cuts(),stdIso("z1l1",0.275,"ele"),stdIso("z1l2",0.275,"ele"),z1Sip.cuts(),eleNum.cuts(),"nElectrons<4","nMuons<4")
	#todo: pass extra cuts
	#temp
	extra="&&z1Mass>60&&z1Mass<120"
	enum.Add(makeHist(file.Get("eleEleEleEventTree/eventTree"),var,defineCuts(common.cuts(),z1ee.cuts(),z1RelPFIso.cuts(),eleNum.cuts()+extra,"1","1"),12,0,120,False,customBinning,bins))
	eden.Add(makeHist(file.Get("eleEleEleEventTree/eventTree"),var,defineCuts(common.cuts(),z1ee.cuts(),z1RelPFIso.cuts(),eleDen.cuts()+extra,"1","1"),12,0,120,False,customBinning,bins))
	enum.Add(makeHist(file.Get("muMuEleEventTree/eventTree"),var,defineCuts(common.cuts(),z1mm.cuts(),z1RelPFIso.cuts(),eleNum.cuts()+extra,"1","1"),12,0,120,False,customBinning,bins))
	eden.Add(makeHist(file.Get("muMuEleEventTree/eventTree"),var,defineCuts(common.cuts(),z1mm.cuts(),z1RelPFIso.cuts(),eleDen.cuts()+extra,"1","1"),12,0,120,False,customBinning,bins))

	mnum.Add(makeHist(file.Get("eleEleMuEventTree/eventTree"),var,defineCuts(common.cuts(),z1ee.cuts(),z1RelPFIso.cuts(),"1",muNum.cuts()+extra),12,0,120,False,customBinning,bins))
	mden.Add(makeHist(file.Get("eleEleMuEventTree/eventTree"),var,defineCuts(common.cuts(),z1ee.cuts(),z1RelPFIso.cuts(),"1",muDen.cuts()+extra),12,0,120,False,customBinning,bins))
	mnum.Add(makeHist(file.Get("muMuMuEventTree/eventTree"),var,defineCuts(common.cuts(),z1mm.cuts(),z1RelPFIso.cuts(),"1",muNum.cuts()+extra),12,0,120,False,customBinning,bins))
	mden.Add(makeHist(file.Get("muMuMuEventTree/eventTree"),var,defineCuts(common.cuts(),z1mm.cuts(),z1RelPFIso.cuts(),"1",muDen.cuts()+extra),12,0,120,False,customBinning,bins))
	eleFr = TGraphAsymmErrors()
	eleFr.BayesDivide(enum,eden)
	eleFr.SetTitle("Electron fake rate")
	eleFr.GetYaxis().SetRangeUser(0,1.0)
	eleFr.GetXaxis().SetTitle(var)
	eleFr.GetYaxis().SetTitle("Fake Rate")
	eleFr.Draw("ap")
	raw_input("Press any key to look at muons")
	muFr = TGraphAsymmErrors()
	muFr.BayesDivide(mnum,mden)
	muFr.SetTitle("Mu fake rate")
	muFr.GetYaxis().SetRangeUser(0,1.0)
	muFr.GetXaxis().SetTitle(var)
	muFr.GetYaxis().SetTitle("Fake Rate")
	muFr.Draw("ap")
	raw_input("Press any key to move on")
	print "------Totals------"
	print "--Electrons--"
	print "\t",enum.Integral()/eden.Integral(),"=",enum.Integral(),"/",eden.Integral()
	print "--Muons--"
	print "\t",mnum.Integral()/mden.Integral(),"=",mnum.Integral(),"/",mden.Integral()
	return [enum.Integral()/eden.Integral(),mnum.Integral()/mden.Integral()]

def applyFakes(filename,extra="",var="z2l1Pt", customBinning=False, bins=[0,1]):
	#4m
	AI={}
	IA={}
	AA={}
	nAI={}
	nIA={}
	nAA={}
	file=TFile(filename)
	FRs=measureLeptonFakes(filename,extra,var,customBinning,bins)

	ai=file.Get("muMuMuMuEventTree_antiIso1/eventTree")
	ia=file.Get("muMuMuMuEventTree_antiIso2/eventTree")
	aa=file.Get("muMuMuMuEventTree_antiIso/eventTree")
	nAI["mmmm"]=ai.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmAI.cuts()))
	AI["mmmm"]=FRs[1]/(1-FRs[1])*ai.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmAI.cuts())+extra)
	nIA["mmmm"]=ia.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmIA.cuts())+extra)
	IA["mmmm"]=FRs[1]/(1-FRs[1])*ia.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmIA.cuts())+extra)
	nAA["mmmm"]=aa.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmAA.cuts())+extra)
	AA["mmmm"]=FRs[1]*FRs[1]/(1-FRs[1])/(1-FRs[1])*aa.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),mmAA.cuts())+extra)

	ai=file.Get("eleEleEleEleEventTree_antiIso1/eventTree")
	ia=file.Get("eleEleEleEleEventTree_antiIso2/eventTree")
	aa=file.Get("eleEleEleEleEventTree_antiIso/eventTree")
	nAI["eeee"]=ai.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeAI.cuts())+extra)
	AI["eeee"]=FRs[0]/(1-FRs[0])*ai.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeAI.cuts())+extra)
	nIA["eeee"]=ia.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeIA.cuts())+extra)
	IA["eeee"]=FRs[0]/(1-FRs[0])*ia.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeIA.cuts())+extra)
	nAA["eeee"]=aa.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeAA.cuts())+extra)
	AA["eeee"]=FRs[0]*FRs[0]/(1-FRs[0])/(1-FRs[0])*aa.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),eeAA.cuts())+extra)

	ai=file.Get("muMuEleEleEventTree_antiIso1/eventTree")
	ia=file.Get("muMuEleEleEventTree_antiIso2/eventTree")
	aa=file.Get("muMuEleEleEventTree_antiIso/eventTree")
	nAI["mmee"]=ai.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAI.cuts())+extra)
	AI["mmee"]=FRs[0]/(1-FRs[0])*ai.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAI.cuts())+extra)
	nIA["mmee"]=ia.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeIA.cuts())+extra)
	IA["mmee"]=FRs[0]/(1-FRs[0])*ia.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeIA.cuts())+extra)
	nAA["mmee"]=aa.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAA.cuts())+extra)
	AA["mmee"]=FRs[0]*FRs[0]/(1-FRs[0])/(1-FRs[0])*aa.GetEntries(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAA.cuts())+extra)

	#get event numbers for each region
	mmeeEvents={}
	mmeeEvents["ai"]=[]
	mmeeEvents["ia"]=[]
	mmeeEvents["aa"]=[]
	aicopy=ai.CopyTree(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAI.cuts()))
	iacopy=ia.CopyTree(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeIA.cuts()))
	aacopy=aa.CopyTree(defineCuts(common.cuts(),z1mm.cuts(),z1StdIsomm.cuts(),eeAA.cuts()))
	for event in aicopy:
		mmeeEvents["ai"].append(event.EVENT)
	for event in iacopy:
		mmeeEvents["ia"].append(event.EVENT)
	for event in aacopy:
		mmeeEvents["aa"].append(event.EVENT)

	ai=file.Get("eleEleMuMuEventTree_antiIso1/eventTree")
	ia=file.Get("eleEleMuMuEventTree_antiIso2/eventTree")
	aa=file.Get("eleEleMuMuEventTree_antiIso/eventTree")
	nAI["eemm"]=ai.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAI.cuts())+extra)
	AI["eemm"]=FRs[1]/(1-FRs[1])*ai.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAI.cuts())+extra)
	nIA["eemm"]=ia.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmIA.cuts())+extra)
	IA["eemm"]=FRs[1]/(1-FRs[1])*ia.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmIA.cuts())+extra)
	nAA["eemm"]=aa.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAA.cuts())+extra)
	AA["eemm"]=FRs[1]*FRs[1]/(1-FRs[1])/(1-FRs[1])*aa.GetEntries(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAA.cuts())+extra)

	#get event numbers for each region
	eemmEvents={}
	eemmEvents["ai"]=[]
	eemmEvents["ia"]=[]
	eemmEvents["aa"]=[]
	aicopy=ai.CopyTree(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAI.cuts()))
	iacopy=ia.CopyTree(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmIA.cuts()))
	aacopy=aa.CopyTree(defineCuts(common.cuts(),z1ee.cuts(),z1StdIsoee.cuts(),mmAA.cuts()))
	for event in aicopy:
		eemmEvents["ai"].append(event.EVENT)
	for event in iacopy:
		eemmEvents["ia"].append(event.EVENT)
	for event in aacopy:
		eemmEvents["aa"].append(event.EVENT)

#	print "ai"
#	print "mmee\teemm\toverlap"
#	print len(mmeeEvents["ai"]),len(eemmEvents["ai"]),len(set(mmeeEvents["ai"]).intersection(set(eemmEvents["ai"])))
#	print "ia"
#	print "mmee\teemm\toverlap"
#	print len(mmeeEvents["ia"]),len(eemmEvents["ia"]),len(set(mmeeEvents["ia"]).intersection(set(eemmEvents["ia"])))
#	print "aa"
#	print "mmee\teemm\toverlap"
#	print len(mmeeEvents["aa"]),len(eemmEvents["aa"]),len(set(mmeeEvents["aa"]).intersection(set(eemmEvents["aa"])))

	#printout
	for state in ["eeee","mmmm","mmee","eemm"]:
		print "----"+state+"----"
		print "AI:",AI[state],"(",nAI[state],")"
		print "IA:",IA[state],"(",nIA[state],")"
		print "AA:",AA[state],"(",nAA[state],")"
		print AI[state]+IA[state]-AA[state]," = ",AI[state],"+",IA[state],"-",AA[state]

def main():
	f1 = TFile("BG_StdIso.root")
	f2 = TFile("Z2Jets_BGStdIso.root")
	c = TCanvas()
#	files=[f1,f2]
	files = [f1]
	hs = THStack("hs","stacked")
	for f in files:
		t = f.Get("eleEleMuMuEventTree_antiIso/eventTree")
		histEEMM = makeHist(t,"z2Mass",defineCuts(common.cuts(),stdIso("z1l1",0.275,"ele",True),stdIso("z1l2",0.275,"ele",True),"!"+stdIso("z2l1",0.275,"mu"),"!"+stdIso("z2l2",0.275,"mu"),z1Sip.cuts(),"z2Charge==0&&z2Mass>12&&z2Mass<120"),12,0,120)
		fit(histEEMM)
		t = f.Get("muMuEleEleEventTree_antiIso/eventTree")
		histMMEE = makeHist(t,"z2Mass",defineCuts(common.cuts(),stdIso("z1l1",0.275,"mu",True),stdIso("z1l2",0.275,"mu",True),"!"+stdIso("z2l1",0.275,"ele"),"!"+stdIso("z2l2",0.275,"ele"),z1Sip.cuts(),"z2Charge==0&&z2Mass>12&&z2Mass<120"),12,0,120)
		fit(histMMEE)
		t = f.Get("muMuMuMuEventTree_antiIso/eventTree")
		histMMMM = makeHist(t,"z2Mass",defineCuts(common.cuts(),stdIso("z1l1",0.275,"mu",True),stdIso("z1l2",0.275,"mu",True),"!"+stdIso("z2l1",0.275,"mu"),"!"+stdIso("z2l2",0.275,"mu"),z1Sip.cuts(),"z2Charge==0&&z2Mass>12&&z2Mass<120"),12,0,120)
		fit(histMMMM)
		t = f.Get("eleEleEleEleEventTree_antiIso/eventTree")
		histEEEE = makeHist(t,"z2Mass",defineCuts(common.cuts(),stdIso("z1l1",0.275,"ele",True),stdIso("z1l2",0.275,"ele",True),"!"+stdIso("z2l1",0.275,"ele"),"!"+stdIso("z2l2",0.275,"ele"),z1Sip.cuts(),"z2Charge==0&&z2Mass>12&&z2Mass<120"),12,0,120)
		fit(histEEEE)
		print f.GetName()
		if "Z2" in f.GetName():
			print "Z2j"
			hist.SetFillColor(kRed)
#		hist.Draw()
#		print hist.Integral()
#		hs.Add(hist)
#	hs.Draw()
	histEEMM.Add(histMMEE)
	histEEMM.Add(histMMMM)
	histEEMM.Add(histEEEE)
	print "Total total total:",histEEMM.Integral()
	fit(histEEMM)
	c.Update()
	raw_input("Press Enter")

if __name__=='__main__':main()
