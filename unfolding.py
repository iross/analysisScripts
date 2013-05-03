from ROOT import *
from plotHelpers import makeHist
from combTrees import makeTree
from RecoLuminosity.LumiDB import argparse
gSystem.Load("RooUnfold-1.1.1/libRooUnfold");

parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
parser.add_argument('--tree',type=str,required=True,default='',help='Input file')
parser.add_argument('--nice',type=str,required=True,default='',help='Output file')

args = parser.parse_args()

treename=args.tree
treeNiceName=args.nice

# apply mass/pt requirements. todo: eta cuts based on pdgId

extra="z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120&&((z1l1Pt>20&&(z1l2Pt>10||z2l1Pt>10||z2l2Pt>10))||(z1l2Pt>20&&(z1l1Pt>10||z2l1Pt>10||z2l2Pt>10))||(z2l1Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l2Pt>10))||(z2l2Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l1Pt>10)))"

#weights screwy (ran eventweightsiterative on the unmerged root files)
trainingFile = TFile("/scratch/iross/ZZ_8TeV_wGen_selected.root")
trainingFileGen = TFile("/scratch/iross/ZZ_8TeV_wGen.root")

#weights are ok...maybe?
trainingFile = TFile("/scratch/iross/ZZ_wGen_proper_weights_selected.root")
trainingFileGen = TFile("/scratch/iross/ZZ_wGen_proper_weights.root")

testFile = TFile("sherpa_sm_selected.root")
testFileGen = TFile("/scratch/iross/temp_sherpa.root")
#testFile = TFile("ZZJets4L_8TeV_final_wGen_selected.root")
#testFileGen = TFile("/scratch/iross/ZZJets4L_8TeV_final_wGen-MC.root")

#testFile=trainingFile
#testFileGen=trainingFileGen

idReq="1"
if "llll" in treename:
    idReq="&&(((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*13**2))||((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(13**2*13**2))||((z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*11**2)))"
    multFactor=1
elif "eeee" in treename:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*11**2)"
    multFactor=1
    extra=extra+"&&z1l1Pt>7&&z1l2Pt>7&&z2l1Pt>7&&z2l2Pt>7"
    extra=extra+"&&abs(z1l1Eta)<2.5&&abs(z1l2Eta)<2.5&&abs(z2l1Eta)<2.5&&abs(z2l2Eta)<2.5"
elif "mmmm" in treename:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(13**2*13**2)"
    multFactor=1
#    extra=extra+"&&z1l1Pt>5&&z1l2Pt>5&&z2l1Pt>5&&z2l2Pt>5"
#    extra=extra+"&&abs(z1l1Eta)<2.4&&abs(z1l2Eta)<2.4&&abs(z2l1Eta)<2.4&&abs(z2l2Eta)<2.4"
else:
    idReq="&&(z1l1pdgId*z1l2pdgId*z2l1pdgId*z2l2pdgId)==(11**2*13**2)"
    multFactor=1

nbins=40
xlo=0
xhigh=1000

fout=TFile("out.root","update")
temp=trainingFile.Get(treename)
temp2=trainingFileGen.Get("genlevel/genEventTree")
tMeas=temp.CopyTree(extra)
tTrue=temp2.CopyTree(extra)

dataTreeTrue = testFileGen.Get("genlevel/genEventTree")
dataTree = testFile.Get(treename)


bins=range(xlo,xhigh+(xhigh-xlo)/nbins,(xhigh-xlo)/nbins)

def getBinFactors(trueTree,measTree,varTrue,bins,varMeas="dummy"):
    """Returns array of size nbins with bin-by-bin (truth:measured) ratios."""
    """No mathing done between truth events and reco events! Bulk corrections only!"""
    if varMeas is "dummy": #if I'm lazy and don't pass a varMeas, assume it's the same as the true
        varMeas=varTrue
#    measHist=makeHist(measTree,varMeas,"(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weight*1000*19.3)",25,100,600,False,True,bins,binNorm=False)
#    trueHist=makeHist(trueTree,varTrue,"(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(weight*1000*19.3)",25,100,600,False,True,bins,binNorm=False)
    measHist=makeHist(measTree,varMeas,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weight)",25,100,600,False,True,bins,binNorm=False)
    trueHist=makeHist(trueTree,varTrue,extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(weight)",25,100,600,False,True,bins,binNorm=False)
    trueHist.Scale(multFactor)
    print "measured integral:",measHist.Integral()
    print "truth integral:",trueHist.Integral()
    corrs=[]
    for i in range(len(bins)-1):
        rat=0.0
        try:
            rat=trueHist.GetBinContent(i)/measHist.GetBinContent(i)
            corrs.append(rat)
        except ZeroDivisionError:
            corrs.append(rat)
    return corrs

def applyCorrs(corrs,hist):
    """Apply the true:reco corrections, return the 'unfolded' histogram"""
    temp=hist.Clone()
    for i in range(len(corrs)):
        temp.SetBinContent(i,temp.GetBinContent(i)*corrs[i])
        # todo:errors
    return temp

def makeResponse(nbins,xlo,xhigh,trueTree,measTree):
    response = RooUnfoldResponse(nbins,xlo,xhigh)
    # fill using response.Fill(measured, true) (or response.Miss(true)
    print "Here we go!"
    recEvents={}
    nr=0
    for event in measTree:
        id=event.EVENT/event.gMass
    #    if str('%.4f' %id) in recEvents.keys():
    #        print "Repeat found!"
    #        nr=nr+1
    #        print recEvents[str('%.4f' %id)]['gz1Mass'],recEvents[str('%.4f' %id)]['gz2Mass']
    #        print event.gz1Mass,event.gz2Mass

        recEvents[str('%.4f' %id)]={'mass':event.mass,
                'gMass':event.gMass,
                'gz1Mass':event.gz1Mass,
                'gz2Mass':event.gz2Mass,
                'dR_z1_gz1':event.dR_z1_gz1,
                'dR_z2_gz2':event.dR_z2_gz2,
                'dR_z1_gz2':event.dR_z1_gz2,
                'dR_z2_gz1':event.dR_z2_gz1}
    recSet=set(recEvents.keys())

    tTrueEvents={}
    for event in trueTree: #loop over truth events
        id=event.EVENT/event.zzMass
        tTrueEvents[str('%.4f' %id)]={'zzMass':event.zzMass}
    trueSet=set(tTrueEvents.keys())

    hit=0
    miss=0
    agree=0
    # Training
    measEvents={}
    for event in trueSet:
        if event in recSet:
            agree=agree+1
            #hack hack hack to make sure I can still close
            if (recEvents[event]['dR_z1_gz1'] < 0.5 and recEvents[event]['dR_z2_gz2'] < 0.5) or (recEvents[event]['dR_z1_gz2']<0.5 and recEvents[event]['dR_z2_gz1']<0.5):
               measEvents[event]=recEvents[event]
               response.Fill(recEvents[event]['mass'],tTrueEvents[event]['zzMass'])
               hit=hit+1
            else:
                response.Miss(tTrueEvents[event]['zzMass'])
                miss=miss+1
        else:
            response.Miss(tTrueEvents[event]['zzMass'])
            miss=miss+1
    print len(trueSet),"true events used in training"
    print len(recSet),"measured events used for training"
    print len(recSet-trueSet),"measured not in true"
    print "hit:",hit
    print "miss:",miss
    print "in both true and rec:",agree
    return response

corrs=getBinFactors(tTrue,tMeas,"zzMass",bins,varMeas="mass")

dataHist=makeHist(dataTree,"mass",extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(weight*1000*19.3)",25,100,600,False,True,bins,binNorm=False)
dataHistTrue=makeHist(dataTreeTrue,"zzMass",extra+"&&(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(weight*1000*19.3)",25,100,600,False,True,bins,binNorm=False)
#dataHist=makeHist(dataTree,"mass","(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120)*(1)",25,100,600,False,True,bins,binNorm=False)
#dataHistTrue=makeHist(dataTreeTrue,"zzMass","(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(1)",25,100,600,False,True,bins,binNorm=False)
trainingTrue=makeHist(tTrue,"zzMass","(z1Mass>60&&z1Mass<120&&z2Mass>60&&z2Mass<120"+idReq+")*(1)",25,100,600,False,True,bins,binNorm=False)
trainingTrue.Scale(dataHistTrue.Integral()/trainingTrue.Integral())
trainingTrue.SetLineColor(kGreen)

unfoldedHist=applyCorrs(corrs,dataHist)

#response=makeResponse(nbins,xlo,xhigh,t2,t)

# unfold
#print "Unfolding..."
#print response
#unfold = RooUnfoldBinByBin(response, measured)
#print "unfolded"
## check results
#unfold.PrintTable(cout,true)

ymax=max(dataHist.GetMaximum(),dataHistTrue.GetMaximum(), unfoldedHist.GetMaximum())
ymax=ymax*1.05*(1+1/ymax**0.5)

can=TCanvas("can","can",600,600)
pad1 = TPad("pad1","pad1",0,0.3,1,1);
pad1.SetBottomMargin(0);
pad1.Draw()
pad1.cd()
unfoldedHist.GetYaxis().SetRangeUser(0,ymax)
unfoldedHist.Draw('p')


dataHist.SetLineColor(kRed)
dataHist.SetLineWidth(2)
dataHist.SetMarkerSize(0.00001)
dataHist.Draw("h same")
dataHistTrue.SetLineColor(kBlue)
dataHistTrue.SetLineWidth(2)
dataHistTrue.SetMarkerSize(0.00001)
dataHistTrue.Scale(multFactor)
dataHistTrue.Draw("h same")


leg=TLegend(0.6,0.5,0.9,0.85)
leg.SetHeader(treeNiceName)
#legend
leg.SetFillColor(kWhite)
leg.AddEntry(dataHistTrue,"Truth","l")
leg.AddEntry(dataHist,"Measured","l")
leg.AddEntry(unfoldedHist,"Unfolded","p")

print "-------------------"
print "Data:",dataHist.Integral()
print "True:",dataHistTrue.Integral()
print "Unfolded:",unfoldedHist.Integral()
print "-------------------"

#trainingTrue.SetLineWidth(2)
#trainingTrue.SetMarkerSize(0.00001)
#trainingTrue.Draw("h same")
#leg.AddEntry(trainingTrue,"POWHEG (normed to true)","l")

leg.SetBorderSize(1)
leg.Draw()
can.cd()
pad2 = TPad("pad2","pad2",0,0,1,0.3);
pad2.SetTopMargin(0.1)
pad2.Draw()
pad2.cd()
temp=dataHistTrue.Clone()
temp.SetLineColor(kBlack)
temp.Divide(unfoldedHist)
temp.GetYaxis().SetRangeUser(0.75,1.25)
temp.Draw()
can.cd()
can.SaveAs("test.png")

