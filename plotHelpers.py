#!/usr/bin/env python
from ROOT import *
from array import *
from CommonSelectors import *

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT.gROOT.ProcessLine(".X CMSStyle.C")
#ROOT.gROOT.SetBatch(True)

def makeHist(tree, var, cuts, nbin, xmin, xmax, overflow=False, customBinning=False, bins=[0,1], name="temp",binNorm=False):
    #	logging.debug("Making hist with %i bins, from %d to %d",nbin,xmin,xmax)
    h = TH1F(name,name,nbin,xmin,xmax)
    if customBinning:
        h = TH1F(name,name,len(bins)-1,array('d',bins))
    if overflow:
        h.SetBinContent(nbin,h.GetBinContent(nbin)+h.GetBinContent(nbin+1))
    h.Sumw2()
    tree.Draw(var+">>"+name,cuts,"goff")
    if binNorm:
        h.Scale(1.0,"width")
    return h

def makeHist2D(tree, cuts, varx, nbinx, xmin, xmax, vary, nbiny, ymin, ymax, customBinning=False, bins=[0,1]):
#       logging.debug("Making hist with %i bins, from %d to %d",nbin,xmin,xmax)
        h = TH2F("h","h",nbinx,xmin,xmax,nbiny,ymin,ymax)
        h.Sumw2()
        if customBinning:
                #todo: 2d custom binning
                h = TH1F("temp","temp",len(bins)-1,array('d',bins))
                h.Sumw2()
        tree.Draw(vary+":"+varx+">>h",cuts,"")
        return h

def compTrees(trees,var,bins,cuts="1",names=[""],drawOptions="h",prefix="",nice=""):
    """Compare variables from some trees"""
    can=TCanvas("can","can",600,600)
    leg=TLegend(0.6,0.7,0.9,0.9)
    colors=[kBlack,kBlue,kRed,kGreen,kCyan,kRed-9]
    markers=[20,22,24,26,29,34]
    nbin=len(bins)
    xmin=min(bins)
    xmax=max(bins)
    h={}
    name={}
    maxY=0
    i=0
    for tree in trees:
        h[tree.GetDirectory().GetName()+names[i]]=makeHist(tree, var, cuts[i], nbin, xmin, xmax, False, True, bins)
        name[tree.GetDirectory().GetName()+names[i]]=names[i]
        maxY=max(maxY,h[tree.GetDirectory().GetName()+names[i]].GetMaximum()/h[tree.GetDirectory().GetName()+names[i]].Integral())
        i=i+1
    i=0
    for hist in h:
        h[hist].Scale(1/h[hist].Integral())
        h[hist].SetLineColor(colors[i])
        h[hist].SetMarkerStyle(markers[i])
        h[hist].SetMarkerColor(colors[i])
        h[hist].SetLineWidth(2)
        h[hist].SetName(name[hist])
        h[hist].SetTitle(name[hist])
        leg.AddEntry(h[hist])
        if i==0:
            h[hist].GetXaxis().SetTitle(nice)
            h[hist].GetYaxis().SetRangeUser(0,maxY*1.15)
            if bins[0]-bins[1] == bins[len(bins)-2]-bins[len(bins)-1]: # if spaced evenly
                div=(float(bins[len(bins)-1])-float(bins[0]))/(len(bins)-1)
                h[hist].GetYaxis().SetTitle("a.u.")
                h[hist].GetYaxis().SetRange(0,15)
            else:
                h[hist].GetYaxis().SetTitle("Events")
                h[hist].GetYaxis().SetRange(0,15)
            h[hist].Draw(drawOptions)
        else:
            h[hist].Draw(drawOptions+"same")
        i+=1
    leg.SetFillColor(kWhite)
    leg.SetShadowColor(0)
    leg.Draw()
    can.SaveAs(prefix+"comp"+var+".png")
    can.SaveAs(prefix+"comp"+var+".pdf")
    return can

def getYields(file, lumi, cuts=""):
    fin = TFile(file)
    if cuts != "":
        cuts="*"+cuts
    for t in fin.GetListOfKeys():
        tree = t.GetName()
        t=fin.Get(tree)
        #Note: use __CORR__ for 2l2t, __CORRnoHLT__ for 4l
        h=makeHist(t, "z1Mass", "(1)*__WEIGHT__noPU*__CORRnoHLT__*"+lumi+cuts, 60, 60, 120)
        h2 = TH1F("h2","h2",2,0,2)
        h2.Sumw2()
#		t.Draw("1>>h2","(1)*__WEIGHT__noPU*__CORRnoHLT__*"+lumi+cuts)
        t.Draw("1>>h2","(1)*__WEIGHT__noPU*__CORR__*"+lumi+cuts)
        h.Delete()
        h2.Delete()

def fit(hist):
    logging.debug("Fitting histogram %s",hist.GetTitle())
    gSystem.Load("libRooFit")
    mass = RooRealVar("mass","mass",100,600)
    mean = RooRealVar("mean","mean",50,0,600)
    sigma = RooRealVar("sigma","sigma",0,100)
    Yield = RooRealVar("yield","yield",50,0,10000)

    print hist.Integral(),"seen in data"
    land = RooLandau("land","land",mass,mean,sigma)
    data = RooDataHist("data","data",RooArgList(mass),hist)

    totalPdf = RooAddPdf("totalPdf","total",RooArgList(land),RooArgList(Yield))

    totalPdf.fitTo(data)
    c1=TCanvas("can","can",600,600)
    C = mass.frame()
    data.plotOn(C)
    totalPdf.plotOn(C)
    C.Draw()
    print mean.getVal(),"+-",mean.getErrorHi(),mean.getErrorLo()
    print sigma.getVal(),"+-",sigma.getErrorHi(),sigma.getErrorLo()
    mass.setRange("onshellReg",60,120)
    integral = totalPdf.createIntegral(RooArgSet(mass),RooArgSet(mass),"onshellReg")
    expected = integral.getVal()*Yield.getVal()
    print "Expected in on-shell region:",expected
    return c1

def measureLeptonFakes(file, var="z2l1Pt", extra="", customBinning=False, bins=[0,1], varNice="P_{T}"):
    logging.debug('Measuring fakes from file:%s',file)
    try:
        file = TFile(file)
        print "This will work a bit better if you pass an open TFile!"
    except TypeError:
        pass
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
    #todo: re-implement the nElectron/nMuon vetos
    enum.Add(makeHist(file.Get("eeeFinal"),var,defineCuts(common.cuts(),z1ee.cuts(),z1relIsoNoFSR.cuts(),eleNum.cuts())+extra,12,0,120,False,customBinning,bins))
    eden.Add(makeHist(file.Get("eeeFinal"),var,defineCuts(common.cuts(),z1ee.cuts(),z1relIsoNoFSR.cuts(),eleDen.cuts())+extra,12,0,120,False,customBinning,bins))
    enum.Add(makeHist(file.Get("mmeFinal"),var,defineCuts(common.cuts(),z1mm.cuts(),z1relIsoNoFSR.cuts(),eleNum.cuts())+extra,12,0,120,False,customBinning,bins))
    eden.Add(makeHist(file.Get("mmeFinal"),var,defineCuts(common.cuts(),z1mm.cuts(),z1relIsoNoFSR.cuts(),eleDen.cuts())+extra,12,0,120,False,customBinning,bins))

    mnum.Add(makeHist(file.Get("eemFinal"),var,defineCuts(common.cuts(),z1ee.cuts(),z1relIsoNoFSR.cuts(),muNum.cuts())+extra,12,0,120,False,customBinning,bins))
    mden.Add(makeHist(file.Get("eemFinal"),var,defineCuts(common.cuts(),z1ee.cuts(),z1relIsoNoFSR.cuts(),muDen.cuts())+extra,12,0,120,False,customBinning,bins))
    mnum.Add(makeHist(file.Get("mmmFinal"),var,defineCuts(common.cuts(),z1mm.cuts(),z1relIsoNoFSR.cuts(),muNum.cuts())+extra,12,0,120,False,customBinning,bins))
    mden.Add(makeHist(file.Get("mmmFinal"),var,defineCuts(common.cuts(),z1mm.cuts(),z1relIsoNoFSR.cuts(),muDen.cuts())+extra,12,0,120,False,customBinning,bins))

    c1=TCanvas("can","can",600,600)
    eleFr = TGraphAsymmErrors()
    eleFr.BayesDivide(enum,eden)
    eleFr.GetYaxis().SetRangeUser(0,0.5)
    eleFr.GetXaxis().SetTitle(varNice)
    eleFr.GetYaxis().SetTitle("e Fake Rate")
    eleFr.Draw("ap")
    c1.SaveAs("ele_FR_"+var+".C")
    c1.SaveAs("ele_FR_"+var+".png")
    enum.Draw()
    c1.SaveAs("ele_num_"+var+".C")
    c1.SaveAs("ele_num_"+var+".png")
    eden.Draw()
    c1.SaveAs("ele_den_"+var+".C")
    c1.SaveAs("ele_den_"+var+".png")
    muFr = TGraphAsymmErrors()
    muFr.BayesDivide(mnum,mden)
    muFr.GetYaxis().SetRangeUser(0,0.5)
    muFr.GetXaxis().SetTitle(var)
    muFr.GetYaxis().SetTitle("#mu Fake Rate")
    muFr.Draw("ap")
    c1.SaveAs("mu_FR_"+var+".C")
    c1.SaveAs("mu_FR_"+var+".png")
    mnum.Draw()
    c1.SaveAs("mu_num_"+var+".C")
    c1.SaveAs("mu_num_"+var+".png")
    mden.Draw()
    c1.SaveAs("mu_den_"+var+".C")
    c1.SaveAs("mu_den_"+var+".png")
    print "------Totals------"
    print "--Electrons--"
    print "\t",enum.Integral()/eden.Integral(),"=",enum.Integral(),"/",eden.Integral()
    print "--Muons--"
    print "\t",mnum.Integral()/mden.Integral(),"=",mnum.Integral(),"/",mden.Integral()
    return [enum.Integral()/eden.Integral(),mnum.Integral()/mden.Integral(),eleFr,muFr]

def applyFakes(file,extra="1",var="mass",lowZ1=True,customBinning=False,bins=[0,1],quiet=False,binNorm=False,fakeRates=[0,0]):
    """Apply fakerates to predefined control regions."""
    try:
        file=TFile(file)
        print "This will work a bit better if you pass an open TFile!"
    except TypeError:
        pass

    regions=["eeeeAAFinal","eeeeAIFinal","eeeeIAFinal","mmmmAAFinal","mmmmAIFinal","mmmmIAFinal","mmeeAAFinal","mmeeAIFinal","mmeeIAFinal","eemmAAFinal","eemmAIFinal","eemmIAFinal","eeeeAA_SSFinal","eeeeAI_SSFinal","eeeeIA_SSFinal","mmmmAA_SSFinal","mmmmAI_SSFinal","mmmmIA_SSFinal","mmeeAA_SSFinal","mmeeAI_SSFinal","mmeeIA_SSFinal","eemmAA_SSFinal","eemmAI_SSFinal","eemmIA_SSFinal"]

    BGs={}
    ns={}
    errs={}
    hists={}
    for reg in regions:
        if "eeee" in reg or "mmee" in reg:
            fr=fakeRates[0]
        elif "eemm" in reg or "mmmm" in reg:
            fr=fakeRates[1]
        else:
            sysexit("Can't figure out which fakerate to use!")
        t=file.Get(reg)
        if t.GetEntries()==0:
            BGs[reg]=0
            ns[reg]=0
            errs[reg]=0
            continue
        if lowZ1:
            t=t.CopyTree("mass>100&&mass<600&&((z1Mass>40&&z1Mass<120&&z2Mass>12&&z2Mass<120)||(z1Mass>12&&z1Mass<40&&z2Mass>40&&z2Mass<120))&&"+extra)
#            t=t.CopyTree("mass>100&&mass<600&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120")
        else:
            t=t.CopyTree("mass>100&&z1Mass>40&&z1Mass<120&&z2Mass>12&&z2Mass<120&&mass<600&&"+extra)
#            t=t.CopyTree("mass>100&&z1Mass>40&&z1Mass<120&&z2Mass>12&&z2Mass<120&&mass<600&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120")
        n=t.GetEntries()
        if "AA" in reg:
            scale=fr*fr/(1-fr)/(1-fr)
            expected=n*scale
            err = n**0.5 * scale
        else:
            scale=fr/(1-fr)
            expected=n*scale
            err = n**0.5 * scale
        h=makeHist(t,var,extra,50,100,600,customBinning=customBinning,bins=bins,name="h_"+reg,binNorm=binNorm)
        h.Sumw2()
        BGs[reg]=expected
        ns[reg]=n
        errs[reg]=err
        h.Scale(scale)
        hists[reg]=h.Clone(reg)

    if not quiet:
        print(file.GetName()+" ('real' Z extended to 12-40: "+str(lowZ1)+")")
        for reg in sorted(BGs):
            if 'SS' not in reg:
                print reg,'--',BGs[reg],'+/-',errs[reg],' (',ns[reg],')'
        print "eeee:",BGs["eeeeAIFinal"]+BGs["eeeeIAFinal"]-BGs["eeeeAAFinal"],"+/-",(errs["eeeeAIFinal"]**2+errs["eeeeIAFinal"]**2+errs["eeeeAAFinal"]**2)**0.5
        print "mmmm:",BGs["mmmmAIFinal"]+BGs["mmmmIAFinal"]-BGs["mmmmAAFinal"],"+/-",(errs["mmmmAIFinal"]**2+errs["mmmmIAFinal"]**2+errs["mmmmAAFinal"]**2)**0.5
        print "mmee:",BGs["mmeeAIFinal"]+BGs["mmeeIAFinal"]-BGs["mmeeAAFinal"]+BGs["eemmAIFinal"]+BGs["eemmIAFinal"]-BGs["eemmAAFinal"],"+/-",(errs["mmeeAIFinal"]**2+errs["mmeeIAFinal"]**2+errs["mmeeAAFinal"]**2+errs["eemmAIFinal"]**2+errs["eemmIAFinal"]**2+errs["eemmAAFinal"]**2)**0.5
        print "eeee (SS):",BGs["eeeeAI_SSFinal"]+BGs["eeeeIA_SSFinal"]-BGs["eeeeAA_SSFinal"],"[observed:",file.Get("eeee_SSFinal").GetEntries("mass>100&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"),"]"
        print "mmmm (SS):",BGs["mmmmAI_SSFinal"]+BGs["mmmmIA_SSFinal"]-BGs["mmmmAA_SSFinal"],"[observed:",file.Get("mmmm_SSFinal").GetEntries("mass>100&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"),"]"
        print "mmee (SS):",BGs["mmeeAI_SSFinal"]+BGs["mmeeIA_SSFinal"]-BGs["mmeeAA_SSFinal"],"[observed:",file.Get("mmee_oSSFinal").GetEntries("z1Mass==bestZmass&&mass>100&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"),"]"
        print "eemm (SS):",BGs["eemmAI_SSFinal"]+BGs["eemmIA_SSFinal"]-BGs["eemmAA_SSFinal"],"[observed:",file.Get("eemm_oSSFinal").GetEntries("z1Mass==bestZmass&&mass>100&&z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"),"]"

    return hists

def addText(string,x1,y1,x2,y2):
    """ Return stylized string for stickin' on plots"""
    pav=TPaveText(x1,y1,x2,y2)
    pav.AddText(string)
    pav.SetFillColor(kWhite)
    pav.SetBorderSize(1)
    return pav

def makeBGhist(f,state,var,customBinning,bins,extra="1",binNorm=False,fakeRates=[0,0]):
    """Write the scaled background hists to the TFile on a common canvas"""
    """Also returns the final BG histogram"""

    hists=applyFakes(f,extra=extra,var=var,lowZ1=False,customBinning=customBinning,bins=bins,binNorm=binNorm,fakeRates=fakeRates)
    # if mmee, add eemm
    ROOT.gROOT.ProcessLine(".X CMSStyle.C")
    c1=TCanvas()
    c1.Divide(2,2)
    c1.SetTitle(state+"_canvas")
    c1.SetName(state+"_canvas")

    if state=="eemm" or state=="mmee": #add together Zee_real+Zmm_fake and Zmm_real+Zee_fake contributions
        stateBG=hists['mmeeAIFinal'].Clone()
        stateBG.Add(hists['mmeeIAFinal'])
        stateBG.Add(hists['eemmAIFinal'])
        stateBG.Add(hists['eemmIAFinal'])
        stateBG.Add(hists['mmeeAAFinal'],-1)
        stateBG.Add(hists['eemmAAFinal'],-1)
        c1.cd(1)
        hists['mmeeIAFinal'].Draw('e')
        temp2=addText('mmeeIAFinal',350,0.75*hists['mmeeIAFinal'].GetMaximum(),525,0.90*hists['mmeeIAFinal'].GetMaximum())
        temp2.Draw()
        c1.cd(2)
        hists['mmeeAIFinal'].Draw('e')
        temp3=addText('mmeeAIFinal',350,0.75*hists['mmeeAIFinal'].GetMaximum(),525,0.90*hists['mmeeAIFinal'].GetMaximum())
        temp3.Draw()
        c1.cd(3)
        hists['mmeeAAFinal'].Draw('e')
        temp4=addText('mmeeAAFinal',350,0.75*hists['mmeeAAFinal'].GetMaximum(),525,0.90*hists['mmeeAAFinal'].GetMaximum())
        temp4.Draw()
        c1.cd(4)
        stateBG.Draw('e')
        temp=addText('mmeeFinal',350,0.75*stateBG.GetMaximum(),525,0.90*stateBG.GetMaximum())
        temp.Draw()
        c1.Write()
    else:
        stateBG=hists[state+'AIFinal'].Clone()
        stateBG.Add(hists[state+'IAFinal'])
        stateBG.Add(hists[state+'AAFinal'],-1)
        c1.cd(1)
        hists[state+'IAFinal'].Draw('e')
        temp2=addText(state+'IAFinal',350,0.75*hists[state+'IAFinal'].GetMaximum(),525,0.90*hists[state+'IAFinal'].GetMaximum())
        temp2.Draw()
        c1.cd(2)
        hists[state+'AIFinal'].Draw('e')
        temp3=addText(state+'AIFinal',350,0.75*hists[state+'AIFinal'].GetMaximum(),525,0.90*hists[state+'AIFinal'].GetMaximum())
        temp3.Draw()
        c1.cd(3)
        hists[state+'AAFinal'].Draw('e')
        temp4=addText(state+'AAFinal',350,0.75*hists[state+'AAFinal'].GetMaximum(),525,0.90*hists[state+'AAFinal'].GetMaximum())
        temp4.Draw()
        c1.cd(4)
        stateBG.Draw('e')
        temp=addText(state+'Final',350,0.75*stateBG.GetMaximum(),525,0.90*stateBG.GetMaximum())
        temp.Draw()
        c1.Write()

    print hists[state+'AIFinal'].Integral(),"+",hists[state+'IAFinal'].Integral(),"-",hists[state+'AAFinal'].Integral()
    print stateBG.Integral()
    c2=TCanvas()
    stateBG.Draw()
    stateBG.SetTitle(state+"BG")
    stateBG.SetName(state+"BG")
    return stateBG

def main():
    print "...what are you doing here? This is just a bunch of helper functions."

if __name__=='__main__':main()
