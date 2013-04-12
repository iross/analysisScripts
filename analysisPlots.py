from ROOT import *
from simplePlots import *
import math
import re
import os
from optparse import OptionParser

import numpy as np
import poisson as poisson

ROOT.gROOT.ProcessLine(".X CMSStyle.C")
ROOT.gROOT.SetBatch(True)

dataFile="DATA_2012_noMuEG2012v_8TeV_final_selected.root"

def getTrees(file,postfix):
    arr={}
    arr['eeee']=file.Get("eeeeFinal"+postfix)
    arr['eemm']=file.Get("mmeeFinal"+postfix)
    arr['mmmm']=file.Get("mmmmFinal"+postfix)
    #hack: if data, use FSR tree
#   if "DATA" in file.GetName():
#       arr['eemm']=file.Get("eleEleMuMuEventTreeFinalFSR")
    return arr

def getBGTrees(file,BGtype):
    arr={}
    arr['eeee']=file.Get("eeee"+BGtype+"Final")
    arr['eemm']=file.Get("eemm"+BGtype+"Final")
    arr['mmee']=file.Get("mmee"+BGtype+"Final")
    arr['mmmm']=file.Get("mmmm"+BGtype+"Final")
    return arr

def eventDump(tree,extra):
    """Dump some info about the contents of the passed tree"""
    print tree
    f=open("2012/"+tree.GetName().split("EventTree")[0]+".txt",'w')
    tree2=tree.CopyTree(extra)
    f.write('-------%s-------\n' % tree.GetName().split("EventTree")[0])
    for ev in tree2:
        f.write("RUN: %.0f\tEVENT: %.0f\n"%(ev.RUN,ev.EVENT))
        f.write("Z1m: %.2f\t Z2m: %.2f\t m_4l: %.2f"%(ev.z1Mass,ev.z2Mass,ev.mass))
        f.write('\n\n')
    f.write('%.0f total events\n' % tree2.GetEntries())
    f.close()

def makeScatter(fd,year,lumi):
    can = TCanvas("can","can",600,600)
    fd=TFile(fd)
    d={}
#these are 2012
#   d["eeee"]=fd.Get("eleEleEleEleEventTreeCleaned")
#   d["mmmm"]=fd.Get("muMuMuMuEventTreeCleaned")
    #use llll and eemm trees with FSR event
#   d["eemm"]=fd.Get("eleEleMuMuEventTreeFinalFSR")
    #these are 2011
    d["eeee"]=fd.Get("eeeeFinal")
    d["eemm"]=fd.Get("mmeeFinal")
    d["mmmm"]=fd.Get("mmmmFinal")
    d["4l"]=fd.Get("llllTree")


    h2={}
    for state in d:
        #HACK
        varx="z1Mass"
        texx=63
        varxNice="Z_{M}^{1} (GeV)"
        vary="z2Mass"
        varx="bestZmass"
        vary="subBestZmass"
        if state=="2l2t":
            varyNice="Z_{M}^{#tau#tau} (GeV)"
        else:
            varyNice="Z_{M}^{2} (GeV)"
        min=60
        max=120
        nbins=1200
        if state=="2l2t":
#           d[state].Scan(varx+":"+vary)
            h2[state]=makeHist2D(d[state],"1",varx,nbins,min,max,vary,nbins,30,90)
        else:
#           d[state].Scan(varx+":"+vary)
            print state
            h2[state]=makeHist2D(d[state],"bestZmass>60&&bestZmass<120&&subBestZmass>60&&subBestZmass<120",varx,nbins,min,max,vary,nbins,60,max)
            if state=="eeee":
                h2[state].SetMarkerColor(kBlue)
            elif state=="mmmm":
                h2[state].SetMarkerColor(kRed)
            elif state=="eemm" or state=="mmee":
                h2[state].SetMarkerColor(kGreen)
        h2[state].GetXaxis().SetTitle(varxNice)
        h2[state].GetYaxis().SetTitle(varyNice)
        h2[state].Draw()
        ymax=120
        l1 = TLatex(texx,ymax*1.015,"CMS Preliminary "+year);
        l1.SetTextSize(0.04);
        if year=="2012":
            l="8"
        else:
            l="7"
        l2 = TLatex(texx+0.4,ymax*1.015,"L_{int} = "+lumi+" fb^{-1}, #sqrt{s} = "+l+" TeV");
        l2.SetTextSize(0.04);
        l1.Draw()
        l2.Draw()

        can.SaveAs(year+"/"+state+"/"+state+"_z1Mass_z2Mass.png")
        can.SaveAs(year+"/"+state+"/"+state+"_z1Mass_z2Mass.root")
        can.SaveAs(year+"/"+state+"/"+state+"_z1Mass_z2Mass.C")
    #temp draw them all, resave as 4l (for colors!)
    can.cd()
    h2['eeee'].Draw()
    h2['eemm'].Draw("psame")
    h2['mmmm'].Draw("psame")
    texx=60.5
    l1 = TLatex(texx,ymax*1.010,"CMS Preliminary "+year);
    l1.SetTextSize(0.04);
    if year=="2012":
        l="8"
    else:
        l="7"
    l2 = TLatex(texx+30,ymax*1.010,"L_{int} = "+lumi+" fb^{-1}, #sqrt{s} = "+l+" TeV");
    l2.SetTextSize(0.04);
    l1.Draw()
    l2.Draw()
    leg=TLegend(0.2,0.7,0.4,0.85)
    #legend
    leg.SetFillColor(kWhite)
    leg.AddEntry(h2['eeee'],"eeee","p")
    leg.AddEntry(h2['eemm'],"ee#mu#mu","p")
    leg.AddEntry(h2['mmmm'],"#mu#mu#mu#mu","p")
    leg.SetBorderSize(1)
    leg.Draw()
    can.SaveAs(year+"/4l/4l_z1Mass_z2Mass_colors.png")


def makeBGPlots(BGtype="AA",dir="2012",postfix="8TeV",lumi="2.95",extra="1",var="z1Mass",varNice="Z_{M}^{1}",bins=range(60,120,5),legx=0.2,legW=0.3,legy=0.3,legH=0.3,log=False,binNorm=False):
    year=dir
    if year=="2012":
        l="8"
    else:
        l="7"

    fd=TFile(dataFile)
    d=getBGTrees(fd,BGtype)
    print d

    fzz=TFile("qqZZ_8TeV_final_selected.root")
    zz=getBGTrees(fzz,BGtype)

    fzj=TFile("DYJets_8TeV_final_selected.root")
    zj=getBGTrees(fzj,BGtype)
    print zj

#    ftt=TFile("TTbar_HCPLoose_selected.root")
#    tt=getBGTrees(ftt,BGtype)


    dht=TH1F("dh","dh",len(bins)-1,array('d',bins))
    dh={}
    dhmax={} #store max values, since TGraphAsymmErrors don't play well with GetMaximum used for scaling..
#    fakerates=measureLeptonFakes(fd.GetName(),extra="&&z1Mass>81&&z1Mass<101") #todo: propagate 'extra' properly

    for tree in d:
        if "eeee" in tree or "mmee" in tree:
            fr=fakeRates[0]
        elif "eemm" in tree or "mmmm" in tree:
            fr=fakeRates[1]
        else:
            print("Can't figure out which fakerate to use!")
        if "AA" in BGtype:
            FR=str(fr*fr/(1-fr)/(1-fr))
        elif "AI" in BGtype or "IA" in BGtype:
            FR=str(fr/(1-fr))
        else:
            print("Can't figure out which pass-fail region!")
        t=d[tree]
        print tree,BGtype,t
        dh[tree]=makeHist(t,var,extra,50,100,600,False,True,bins,binNorm=binNorm)
        dht.Add(dh[tree])
        dhmax[tree]=dh[tree].GetMaximum()
        if not binNorm:
            temph=poisson.convert(dh[tree],False,-1000)
        dh[tree]=temph
    dhmax["4l"]=dht.GetMaximum()
    if not binNorm:
        dh["4l"]=poisson.convert(dht,False,-1000)

#    zzht=TH1F("zzh","zzh",len(bins)-1,array('d',bins))
#    zzh={}
#    for tree in zz:
#        t=zz[tree]
#        print tree,BGtype,t
#        zzh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__*1.0*"+lumi+"*1000)",50,100,600,False,True,bins)
#        zzht.Add(zzh[tree])
#        zzh[tree].SetFillColor(kAzure-9)
#        zzh[tree].SetMarkerSize(0.001)
#    zzh["4l"]=zzht

#    ttht=TH1F("tth","tth",len(bins)-1,array('d',bins))
#    tth={}
#    for tree in tt:
#        t=tt[tree]
#        print tree,BGtype,t
#        tth[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__noPU*1.0*"+lumi+"*1000)",50,100,600,False,True,bins)
#        ttht.Add(tth[tree])
#        tth[tree].SetFillColor(kRed+1)
#        tth[tree].SetMarkerSize(0.001)
#    tth["4l"]=ttht

    zjht=TH1F("zjh","zjh",len(bins)-1,array('d',bins))
    zjh={}
    for tree in zj:
        print "------------",tree,"-------------"
        t=zj[tree]
        print t
        zjh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__*1.0*"+lumi+"*1000)",50,100,600,False,True,bins,binNorm=binNorm)
        print "**********", zjh[tree].Integral()
        zjht.Add(zjh[tree])
        zjh[tree].SetFillColor(kGreen-5)
        zjh[tree].SetMarkerSize(0.001)
    zjh['4l']=zjht

    #colors, etc.
#    zzht.SetMarkerSize(0.001)
#    zzht.SetFillColor(kAzure-9)
    zjht.SetMarkerSize(0.001)
    zjht.SetFillColor(kGreen-5)
#    ttht.SetMarkerSize(0.001)
#    ttht.SetFillColor(kRed+1)

    can = TCanvas("can","can",600,600)

    leg=TLegend(legx,legy,legx+legW,legy+legH)
    #legend
    leg.SetFillColor(kWhite)
    leg.AddEntry(dht,"Data","p")
#    leg.AddEntry(zzht,"ZZ","f")
    leg.AddEntry(zjht,"Z+X","f")
#    leg.AddEntry(ttht,"ttbar","f")
    leg.SetBorderSize(1)

    f=open(dir+"/yields.txt","w")
    for state in dh:
        leg.SetHeader(state+", "+BGtype+" Region")
        f.write("---"+state+"---\n")
        if state is "4l":
            f.write("Data: "+str(dht.Integral())+"\n")
        else:
            f.write("Data: "+str(dh[state].Integral())+"\n")
#        f.write("ZZ: "+str(zzh[state].Integral())+"\n")
#        f.write("ZJets:"+str(zjh[state].Integral())+"\n")
        if not os.path.exists(dir+"/"+state):
            os.makedirs(dir+"/"+state)
        hs=THStack("hs","stack bg")
#        hs.Add(zzh[state])
#        hs.Add(tth[state])
        hs.Add(zjh[state])
        hse=zjh[state].Clone()
        hse.SetMarkerStyle(1)
        hse.SetMarkerSize(0.0001)
        hse.SetFillColor(kGray+2)
        hse.SetFillStyle(3004)
        ymax=max(dhmax[state],hs.GetMaximum())
        if state is "4l":
            ymax=max(dht.GetMaximum(),hs.GetMaximum())

        ymax=ceil(1.02*(ROOT.Math.gamma_quantile_c(0.3173/2,ymax+1,1) )) #for 68% coverage
        print ymax,"is y max"
        ymax=int(ymax)
        dummy=TH1F("dummy","dummy",len(bins)-1,array('d',bins))
        dummy.GetYaxis().SetRangeUser(0.,ymax)
        if bins[0]-bins[1] == bins[len(bins)-2]-bins[len(bins)-1]: # if spaced evenly
            div=(float(bins[len(bins)-1])-float(bins[0]))/(len(bins)-1)
            dummy.GetYaxis().SetTitle("Events / %.0f GeV" %div)
            dummy.GetYaxis().SetRange(0,15)
        else:
            dummy.GetYaxis().SetTitle("Events")
            dummy.GetYaxis().SetRange(0,15)
        if binNorm:
            dummy.GetYaxis().SetTitle("dN/d"+varNice)

        dummy.GetXaxis().SetTitle(varNice)
        dummy.Draw()
        l1 = TLatex(bins[0]+(bins[len(bins)-1]-bins[0])/100.0,ymax*1.015,"CMS Preliminary "+year);
        l1.SetTextSize(0.04);
        l2 = TLatex(bins[0]+(bins[len(bins)-1]-bins[0])/2.0,ymax*1.015,"L_{int} ="+lumi+" fb^{-1}, #sqrt{s} = "+l+" TeV");
        l2.SetTextSize(0.04);
        if log:
            dh[state].GetYaxis().SetRangeUser(0.1,ymax)
        else:
            dh[state].GetYaxis().SetRangeUser(0.,ymax)


        dh[state].SetMarkerStyle(20)
        dh[state].SetMarkerSize(1)

        hs.Draw("HIST SAME")
#        hsa.Draw("hsame")
        hse.Draw("e2same")
        dh[state].Draw("pesame")
        leg.Draw()
        l1.Draw();
        l2.Draw();
        if log:
            can.SetLogy(1)

        print can
        if str(bins[0]-bins[1]) == str(bins[len(bins)-2]-bins[len(bins)-1]): # if spaced evenly
            can.SaveAs(dir+"/BG/"+state+"_"+BGtype+"_"+state+"_"+var+""+postfix+".png")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".pdf")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".root")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".C")
        else:
            binStr=""
            print
            for i in range(len(bins)-1):
                binStr+="_"+str(bins[i])
            can.SaveAs(dir+"/BG/"+state+"_"+BGtype+"_"+state+"_"+var+"_varbinning"+postfix+binStr+".png")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".pdf")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".root")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".C")
    f.close()

def makePlots(dir="2012",postfix="8TeV",lumi="2.95",extra="1",var="z1Mass",varNice="Z_{M}^{1}",bins=range(60,120,5),legx=0.2,legW=0.3,legy=0.3,legH=0.3,log=False,binNorm=False):
    fd=TFile(dataFile)
    d=getTrees(fd,"")

    eventDump(d["eeee"],extra)
    eventDump(d["eemm"],extra)
    eventDump(d["mmmm"],extra)

    if binNorm:
        postfix = postfix + "_binNorm"
        print "HOT DAMN! IT'S BIN NORMED!"

    year=dir
    if year=="2012":
        l="8"
    else:
        l="7"

    fzz=TFile("qqZZ_8TeV_final_selected.root")

    zz=getTrees(fzz,"")

    fzj=TFile(dataFile)
    zj=getTrees(fzj,"")


#    fh=TFile("ggH125_lite_2.root")
#    ht=getTrees(fh,"")


    dht=TH1F("dh","dh",len(bins)-1,array('d',bins))
    dh={}
    for tree in d:
        t=d[tree]
        dh[tree]=makeHist(t,var,extra,50,100,600,False,True,bins,"temp"+tree,binNorm=binNorm)
        dht.Add(dh[tree])
        if not binNorm:
            dh[tree]=poisson.convert(dh[tree],False,-1000)
    dh["4l"]=dht
    if not binNorm:
        dh["4l"]=poisson.convert(dh["4l"],False,-1000)

    zzht=TH1F("zzh","zzh",len(bins)-1,array('d',bins))
    zzh={}
    for tree in zz:
        t=zz[tree]
#        zzh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__noPU*__CORRnoHLT__*149/139*"+lumi+"*1000)",50,100,600,False,True,bins)
#        zzh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__noPU*149/139*1.06*"+lumi+"*1000)",50,100,600,False,True,bins)
        zzh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__*1.06*1.10*"+lumi+"*1000)",50,100,600,False,True,bins,name="temp_zz_"+tree,binNorm=binNorm)
    #   zzh[tree]=makeHist(t,var,"1*"+lumi+"*1000",50,100,600,False,True,bins)
        print "Trying to add: ",zzh[tree]
        zzht.Add(zzh[tree])
        zzh[tree].SetFillColor(kAzure-9)
        zzh[tree].SetMarkerSize(0.001)
    zzh["4l"]=zzht

#    zzaht=TH1F("zzh","zzh",len(bins)-1,array('d',bins))
#    zzah={}
#    for tree in zza:
#        t=zza[tree]
#        zzah[tree]=makeHist(t,var,"("+extra+")*(weightnoPU*"+lumi+"*1000*149/139*1.06)",50,100,600,False,True,bins) #do I need this?
#    #   zzah[tree]=makeHist(t,var,"1*"+lumi+"*1000",50,100,600,False,True,bins)
#        zzaht.Add(zzah[tree])
#        zzah[tree].SetFillColor(kWhite-9)
#        zzah[tree].SetMarkerSize(0.001)
#    zzah["4l"]=zzaht
#    print '---------'
#    print zzah["4l"].Integral()
#    print zzh["4l"].Integral()
#    print '---------'

#    hht=TH1F("hh","hh",len(bins)-1,array('d',bins))
#    hh={}
#    for tree in ht:
#        t=ht[tree]
#        hh[tree]=makeHist(t,var,"("+extra+")*(weight*"+lumi+"*1000)",50,100,600,False,True,bins)
#    #   zzh[tree]=makeHist(t,var,"1*"+lumi+"*1000",50,100,600,False,True,bins)
#        hht.Add(hh[tree])
#        hh[tree].SetFillColor(kWhite)
#        hh[tree].SetLineColor(kRed)
#        hh[tree].SetLineWidth(2)
#        hh[tree].SetMarkerSize(0.001)
#    hh["4l"]=hht

    zjht=TH1F("zjh","zjh",len(bins)-1,array('d',bins))
    zjh={}
    for tree in zj:
        zjh[tree]=makeBGhist(fd,tree,var,True,bins,extra,binNorm=binNorm,fakeRates=fakeRates)
        ##temp use AA for shape
#        t=fd.Get("eeeeAAFinal")
#        zjh[tree]=makeHist(t,var,"("+extra+")",50,100,600,False,True,bins)
#        if tree is "eeee":
#            zjh[tree].Scale(0.000781733566027)
#        elif tree is "eemm":
#            zjh[tree].Scale(0.00182164048866)
#        elif tree is "mmmm":
#            zjh[tree].Scale(0.000998080279232)
        ##temp
#        zjh[tree]=makeHist(t,var,"("+extra+")*(__WEIGHT__noPU*"+lumi+"*1000)",50,100,600,False,True,bins)
        zjh[tree].SetFillColor(kGreen-5)
        zjh[tree].SetMarkerSize(0.001)
#    zjh['mmmm'].Scale(0.52/zjh['mmmm'].Integral())
#    zjh['eemm'].Scale(0.58/zjh['eemm'].Integral())
#    zjh['eeee'].Scale(0.25/zjh['eeee'].Integral())
    for hist in zjh:
        zjht.Add(zjh[hist])
    zjh['4l']=zjht

    #colors, etc.
    zzht.SetMarkerSize(0.001)
    zzht.SetFillColor(kAzure-9)
#    hht.SetMarkerSize(0.001)
#    hht.SetFillColor(kWhite)
#    hht.SetLineColor(kRed)
#    hht.SetLineWidth(2)
    zjht.SetMarkerSize(0.001)
    zjht.SetFillColor(kGreen-5)
#    zzaht.SetMarkerSize(0.001)

    f=open(dir+"/yields.txt","w")
    fd.cd()
    fd.ls()
    can = TCanvas("can","can",600,600)

    leg=TLegend(legx,legy,legx+legW,legy+legH)

    #legend
    leg.SetFillColor(kWhite)
    leg.AddEntry(dht,"Data","p")
    leg.AddEntry(zzht,"ZZ","f")
    leg.AddEntry(zjht,"Z+X","f")
#    leg.AddEntry(hht,"h125","f")
#    leg.AddEntry(zzaht,"f_{4}^{Z}=0.015","l")
#    leg.AddEntry(zzaht,"SHERPA","l")
    leg.SetBorderSize(1)


    for state in dh:
        f.write("---"+state+"---\n")
        if state is "4l":
            f.write("Data: "+str(dht.Integral())+"\n")
        else:
            f.write("Data: "+str(dh[state].Integral())+"\n")
        f.write("ZZ: "+str(zzh[state].Integral())+"\n")
#        f.write("ZJets:"+str(zjh[state].Integral())+"\n")
        if not os.path.exists(dir+"/"+state):
            os.makedirs(dir+"/"+state)
        hs=THStack("hs","stack bg")
        hs.Add(zjh[state])
        hs.Add(zzh[state])
        hse=zzh[state].Clone()
        hse.Add(zjh[state])
        hse.SetMarkerStyle(1)
        hse.SetMarkerSize(0.0001)
        hse.SetFillColor(kGray+2)
        hse.SetFillStyle(3004)
#        hs.Add(hh[state])
        ymax=max(dh[state].GetMaximum(),hs.GetMaximum())
        if state is "4l":
            ymax=max(dht.GetMaximum(),hs.GetMaximum())

        ymax=ceil(1.02*(ROOT.Math.gamma_quantile_c(0.3173/2,ymax+1,1) )) #for 68% coverage
        print ymax,"is y max"
        ymax=int(ymax)
        dummy=TH1F("dummy","dummy",len(bins)-1,array('d',bins))
        dummy.GetYaxis().SetRangeUser(0.,ymax)
        if bins[0]-bins[1] == bins[len(bins)-2]-bins[len(bins)-1]: # if spaced evenly
            div=(float(bins[len(bins)-1])-float(bins[0]))/(len(bins)-1)
            dummy.GetYaxis().SetTitle("Events / %.0f GeV" %div)
            dummy.GetYaxis().SetRange(0,15)
        else:
            dummy.GetYaxis().SetTitle("Events")
            dummy.GetYaxis().SetRange(0,15)
        if binNorm:
            varNiceNoUnits=re.sub('\([^)]*\)','',varNice)
            print varNiceNoUnits
            dummy.GetYaxis().SetTitle("dN/d"+varNice)

        dummy.GetXaxis().SetTitle(varNice)
        dummy.Draw()
        l1 = TLatex(bins[0]+(bins[len(bins)-1]-bins[0])/100.0,ymax*1.015,"CMS Preliminary "+year);
        l1.SetTextSize(0.04);
        l2 = TLatex(bins[0]+(bins[len(bins)-1]-bins[0])/2.0,ymax*1.015,"L_{int} ="+lumi+" fb^{-1}, #sqrt{s} = "+l+" TeV");
        l2.SetTextSize(0.04);
        if log:
            dh[state].GetYaxis().SetRangeUser(0.1,ymax)
        else:
            dh[state].GetYaxis().SetRangeUser(0.,ymax)

#        hsa=THStack("hsa","stack bg")
#        zzah[state].SetLineStyle(7)
#        zzah[state].SetLineWidth(2)
#        zzah[state].SetMarkerSize(0.0002)
#        hsa.Add(zjh[state])
#        hsa.Add(zzah[state])

        dh[state].SetMarkerStyle(20)
        dh[state].SetMarkerSize(1)

        hs.Draw("HIST E SAME")
#        hsa.Draw("hsame")
        hse.Draw("e2same")
        dh[state].Draw("pesame")
        leg.Draw()
        l1.Draw();
        l2.Draw();
        if log:
            can.SetLogy(1)

        # strip special chars out of variable name for easier saving
        var=re.sub('[/,.\{\}()+><\* =]','',var)

        if str(bins[0]-bins[1]) == str(bins[len(bins)-2]-bins[len(bins)-1]): # if spaced evenly
            if len(var)>20 and "Phi" in var:
                var="deltaPhi_l1_l2"
            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".png")
            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".pdf")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".root")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+""+postfix+".C")
        else:
            if len(var)>20 and "Phi" in var:
                var="deltaPhi_l1_l2"
            binStr=""
            print
            for i in range(len(bins)-1):
                binStr+="_"+str(bins[i])
            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".png")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".pdf")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".root")
#            can.SaveAs(dir+"/"+state+"/"+state+"_"+var+"_varbinning"+postfix+binStr+".C")
    f.close()

if __name__ == '__main__':
    parser=OptionParser(description="%prog -- dump some analysis-level plots and yields",usage="%prog --extra='extra cuts to apply'")
    parser.add_option("--extra",dest="extra",type="string",default="1")
    parser.add_option("--measExtra",dest="measExtra",type="string",default="&&z1Mass>81&&z1Mass<101")
    parser.add_option("--lumi",dest="lumi",type="string",default="19.3")
    (options,args)=parser.parse_args()
    extra=options.extra
    measExtra=options.measExtra
    lumi=options.lumi

    global fakeRates
    fakeRates=measureLeptonFakes("DATA_2012_noMuEG2012v_8TeV_final_selected.root",extra=measExtra)

#    makeBGPlots("AI",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,610,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1Mass",varNice="M_{real} (GeV)",bins=range(60,125,5),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1Mass",varNice="M_{real} (GeV)",bins=range(60,125,5),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1Mass",varNice="M_{real} (GeV)",bins=range(60,122,2),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(60,125,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(60,125,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(60,122,2),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)

#    makeBGPlots("AI",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="bestZmass",varNice="M_{Z1} (GeV)",bins=range(60,125,5),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="bestZmass",varNice="M_{Z1} (GeV)",bins=range(60,125,5),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="bestZmass",varNice="M_{Z1} (GeV)",bins=range(60,122,2),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="subBestZmass",varNice="M_{Z2} (GeV)",bins=range(60,125,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="subBestZmass",varNice="M_{Z2} (GeV)",bins=range(60,125,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="subBestZmass",varNice="M_{Z2} (GeV)",bins=range(60,122,2),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)

#    makeBGPlots("AI",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="mass",varNice="M_{llll} (GeV)",bins=range(80,610,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="mass",varNice="M_{llll} (GeV)",bins=range(80,610,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="mass",varNice="M_{llll} (GeV)",bins=range(80,610,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z1Mass",varNice="M_{real} (GeV)",bins=range(0,130,5),legx=0.3,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z1Mass",varNice="M_{real} (GeV)",bins=range(0,130,5),legx=0.3,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z1Mass",varNice="M_{real} (GeV)",bins=range(0,130,5),legx=0.3,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA",dir="2012",postfix="8TeV_nohighMassReq",lumi=lumi,extra="bestZmass>40&&bestZmass<120&&subBestZmass>12&&subBestZmass<120",var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AI_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("IA_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makeBGPlots("AA_SS",dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Mass",varNice="M_{fake} (GeV)",bins=range(0,130,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)

#    makePlots(dir="2012",postfix="_low_8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(100,184,3),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="_low_fine_8TeV",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=np.arange(100,151,1.5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="bestZmass",varNice="M_{Z1}",bins=range(60,122,2),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="subBestZmass",varNice="M_{Z2}",bins=range(60,122,2),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="pt/(z1Pt+z2Pt)",varNice="ZZ_{P_{T}}/(Z^{1}_{P_{T}}+Z^{2}_{P_{T}})",bins=np.arange(0,1,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1Pt",varNice="Z_{1} P_{T}",bins=np.arange(0,210,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1Pt",varNice="Z_{1} P_{T}",bins=np.arange(0,210,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#mp    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Pt",varNice="Z_{2} P_{T}",bins=np.arange(0,210,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2Pt",varNice="Z_{2} P_{T}",bins=np.arange(0,210,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="pt",varNice="P_{T}^{ZZ}",bins=range(0,100,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="pt",varNice="P_{T}^{ZZ}",bins=range(0,100,5),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="pt",varNice="P_{T}^{ZZ}",bins=[0,5,10,15,20,30,40,50,80,100],legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="met",varNice="ME_{T}",bins=range(0,100,2),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)

#    makePlots(dir="2012",postfix="8TeV_10wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_10wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV_10wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=False)
#    makePlots(dir="2012",postfix="8TeV_20wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1020,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV_20wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1020,20),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=False)
#    makePlots(dir="2012",postfix="8TeV_10wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=[0,240,300,400,800],legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)

#    deltaPhiZ1="(z1l1Phi-z1l2Phi+2*3.1416)*((z1l1Phi-z1l2Phi)<-3.1416) + (z1l1Phi-z1l2Phi-2*3.1416)*((z1l1Phi-z1l2Phi)>3.1416) + (z1l1Phi-z1l2Phi)*((z1l1Phi-z1l2Phi)>-3.1416&&((z1l1Phi-z1l2Phi)<3.1416))"
#    deltaPhiZ2="(z2l1Phi-z2l2Phi+2*3.1416)*((z2l1Phi-z2l2Phi)<-3.1416) + (z2l1Phi-z2l2Phi-2*3.1416)*((z2l1Phi-z2l2Phi)>3.1416) + (z2l1Phi-z2l2Phi)*((z2l1Phi-z2l2Phi)>-3.1416&&((z2l1Phi-z2l2Phi)<3.1416))"
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="((z1Mass==bestZmass)*abs("+deltaPhiZ1+")) + ((z2Mass==bestZmass)*abs("+deltaPhiZ2+"))",varNice="#Delta#phi (l^{1}_{Z_{1}}, l^{2}_{Z_{1}})",bins=np.arange(0,3.2,0.2),legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="((z1Mass==bestZmass)*abs("+deltaPhiZ1+")) + ((z2Mass==bestZmass)*abs("+deltaPhiZ2+"))",varNice="#Delta#phi (l^{1}_{Z_{1}}, l^{2}_{Z_{1}})",bins=[0,0.5,1.0,1.7,3.2],legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="((z1Mass==bestZmass)*abs("+deltaPhiZ1+")) + ((z2Mass==bestZmass)*abs("+deltaPhiZ2+"))",varNice="#Delta#phi (l^{1}_{Z_{1}}, l^{2}_{Z_{1}})",bins=[0,0.5,1.0,1.7,3.2],legx=0.2,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=False)






#    makePlots(dir="2012",postfix="8TeV_signal",lumi=lumi,extra=extra+"&&mass>121.5&&mass<131.5",var="z1Mass*(abs(z1Mass-91.2)>abs(z2Mass-91.2))+z2Mass*(abs(z2Mass-91.2)>abs(z1Mass-91.2))",varNice="M_{Z2}",bins=range(0,84,4),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1Pt",varNice="Z_{1}l_{1} P_{T}",bins=range(0,105,5),legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1Pt",varNice="z1l1Pt",bins=[0,60,100,200,600],legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False,binNorm=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1Pt",varNice="z1l1Pt",bins=[0,60,100,200,600],legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l2Pt",varNice="z_{1}l_2} P_{T}",bins=range(0,105,5),legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l1Pt",varNice="z2l1Pt",bins=range(0,105,5),legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l2Pt",varNice="z2l2Pt",bins=range(0,105,5),legx=0.7,legW=0.2,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1Eta",varNice="z1l1 #eta",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l2Eta",varNice="z1l2 #eta",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l1Eta",varNice="z2l1 #eta",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l2Eta",varNice="z2l2 #eta",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1Phi",varNice="z1l1 #phi",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l2Phi",varNice="z1l2 #phi",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l1Phi",varNice="z2l1 #phi",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l2Phi",varNice="z2l2 #phi",bins=np.arange(-2.5,2.5,0.1),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_10wide",lumi=lumi,extra=extra,var="mass",varNice="M_{llll} (GeV)",bins=range(80,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False,binNorm=True)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l1pfCombIso2012",varNice="z1l1Iso",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z1l2pfCombIso2012",varNice="z1l2Iso",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l1pfCombIso2012",varNice="z2l1Iso",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV",lumi=lumi,extra=extra,var="z2l2pfCombIso2012",varNice="z2l2Iso",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_barrel",lumi=lumi,extra=extra+"&&abs(z1l1Eta)<1.54",var="z1l1pfCombIso2012",varNice="z1l1Iso (barrel)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_barrel",lumi=lumi,extra=extra+"&&abs(z1l2Eta)<1.54",var="z1l2pfCombIso2012",varNice="z1l2Iso (barrel)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_barrel",lumi=lumi,extra=extra+"&&abs(z2l1Eta)<1.54",var="z2l1pfCombIso2012",varNice="z2l1Iso (barrel)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_barrel",lumi=lumi,extra=extra+"&&abs(z2l2Eta)<1.54",var="z2l2pfCombIso2012",varNice="z2l2Iso (barrel)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_endcap",lumi=lumi,extra=extra+"&&abs(z1l1Eta)>1.54",var="z1l1pfCombIso2012",varNice="z1l1Iso (endcap)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_endcap",lumi=lumi,extra=extra+"&&abs(z1l2Eta)>1.54",var="z1l2pfCombIso2012",varNice="z1l2Iso (endcap)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_endcap",lumi=lumi,extra=extra+"&&abs(z2l1Eta)>1.54",var="z2l1pfCombIso2012",varNice="z2l1Iso (endcap)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_endcap",lumi=lumi,extra=extra+"&&abs(z2l2Eta)>1.54",var="z2l2pfCombIso2012",varNice="z2l2Iso (endcap)",bins=np.arange(0,0.42,0.02),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#
#    makePlots(dir="2012",postfix="8TeV_10wide_massgt100",lumi=lumi,extra=extra+"&&mass>100",var="mass",varNice="M_{llll} (GeV)",bins=range(100,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
#    makePlots(dir="2012",postfix="8TeV_10wide_massgt100",lumi=lumi,extra=extra+"&&mass>100",var="mass",varNice="M_{llll} (GeV)",bins=range(100,1010,10),legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)
    makePlots(dir="2012",postfix="dumbCounting",lumi=lumi,extra=extra+"&&mass>100",var="mass",varNice="M_{llll} (GeV)",bins=[0,1000],legx=0.6,legW=0.3,legy=0.7,legH=0.2,log=False)

    makeScatter(dataFile,"2012","19.3")
    f=open("2012/yields.txt")
    print "****----"+extra+"----"
    for line in f:
        print line.rstrip("\n\r")
    f.close()
