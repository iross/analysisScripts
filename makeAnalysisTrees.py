from combTrees import *
from ROOT import *
import sys
import getopt
from RecoLuminosity.LumiDB import argparse
from SkimmerClass import Skimmer
from simplePlots import *

#todo: threading?

def cmssw_major_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[1])

parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
parser.add_argument('--file',type=str,required=True,default='',help='Input file')
parser.add_argument('--out',type=str,required=True,default='',help='Output file')

args = parser.parse_args()

file=args.file
outfile=args.out

if ".root" not in file:
    file=file+".root"

if cmssw_major_version==4: #2011, use the pfCombIso with the 2011 rho values
    iso="pfCombIso"
else:
    iso="pfCombIso2012"

#vars to store
vars4l = ["mass","z1Mass","z2Mass","z1l1Pt","z1l2Pt","z2l1Pt","z2l2Pt","bestZmass","subBestZmass","RUN","LUMI","EVENT","met","z1l1"+iso,"z1l2"+iso,"z2l1"+iso,"z2l2"+iso,"__WEIGHT__","__WEIGHT__noPU","z1l1"+iso,"z1l2"+iso,"z2l1"+iso,"z2l2"+iso,"weight","weightnoPU","z1l1Eta","z1l2Eta","z2l1Eta","z2l2Eta","massNoFSR","z1l1Phi","z1l2Phi","z2l1Phi","z2l2Phi","z2Charge","z1l1pfPhotonIso","z1l1PhotonIso","z1l2pfPhotonIso","z1l2PhotonIso","z2l1pfPhotonIso","z2l1PhotonIso","z2l2pfPhotonIso","z2l2PhotonIso","pt","z1Pt","z2Pt","nElectrons","nMuons"]
for thing in ["z2l1isGlobal","z2l1isTracker","z2l1isPF","z2l1mvaNonTrigPass","z2l1MissHits","z2l1mvaNonTrigPass","kd"]:
    vars4l.append(thing)
varsZ = ["mass","l1Pt","l2Pt","l1Eta","l2Eta","l1Phi","l2Phi","RUN","LUMI","EVENT","met","l1"+iso,"l2"+iso,"__WEIGHT__","__WEIGHT__noPU","l1SIP","l2SIP"]

#set selections
cuts={}
skimmers={}

#NOTE: don't apply mass cuts until AFTER best Z1 selection
cuts["eeee"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2relIso.cuts(),"fourFour","z2Charge==0")
cuts["mmmm"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2relIso.cuts(),"fourFour","z2Charge==0")
cuts["mmee"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2relIso.cuts(),"fourFour","z2Charge==0") #...this tree should have full selection applied right now
cuts["eemm"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2relIso.cuts(),"fourFour","z2Charge==0")
cuts["eeee_SS"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2relIso.cuts(),"z2Charge!=0") #don't use fourFour, since SS criteria forces failure
cuts["mmmm_SS"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2relIso.cuts(),"z2Charge!=0")
cuts["mmee_SS"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2relIso.cuts(),"z2Charge!=0")
cuts["eemm_SS"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2relIso.cuts(),"z2Charge!=0")
cuts["mm"]=defineCuts("l1Pt>20&&l2Pt>10") #all cuts applied before trees filled
cuts["ee"]=defineCuts("l1Pt>20&&l2Pt>10") #all cuts applied before trees filled

cuts["eee"]=defineCuts(common.cuts(),z1ee.cuts(),"z1l1"+iso+"<0.40&&z1l2"+iso+"<0.40",eleDen.cuts())
cuts["eem"]=defineCuts(common.cuts(),z1ee.cuts(),"z1l1"+iso+"<0.40&&z1l2"+iso+"<0.40",muDen.cuts())
cuts["mme"]=defineCuts(common.cuts(),z1mm.cuts(),"z1l1"+iso+"<0.40&&z1l2"+iso+"<0.40",eleDen.cuts())
cuts["mmm"]=defineCuts(common.cuts(),z1mm.cuts(),"z1l1"+iso+"<0.40&&z1l2"+iso+"<0.40",muDen.cuts())

cuts["eeeeAA"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge==0","fourFour")
cuts["eeeeAI"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge==0","fourFour")
cuts["eeeeIA"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge==0","fourFour")

cuts["mmeeAA"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge==0","fourFour")
cuts["mmeeAI"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge==0","fourFour")
cuts["mmeeIA"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge==0","fourFour")

cuts["eemmAA"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge==0","fourFour")
cuts["eemmAI"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge==0","fourFour")
cuts["eemmIA"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge==0","fourFour")

cuts["mmmmAA"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge==0","fourFour")
cuts["mmmmAI"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge==0","fourFour")
cuts["mmmmIA"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge==0","fourFour")

cuts["eeeeAA_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge!=0")
cuts["eeeeAI_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge!=0")
cuts["eeeeIA_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge!=0")

cuts["mmeeAA_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge!=0")
cuts["mmeeAI_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge!=0")
cuts["mmeeIA_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge!=0")

cuts["eemmAA_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge!=0")
cuts["eemmAI_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge!=0")
cuts["eemmIA_SS"]=defineCuts(z1ee.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge!=0")

cuts["mmmmAA_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge!=0")
cuts["mmmmAI_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge!=0")
cuts["mmmmIA_SS"]=defineCuts(z1mm.cuts(),pt20_10.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge!=0")

f=TFile(file,"read")

fout=TFile(outfile,"recreate")
fout.Close() #temp

t=f.Get("eleEleEleEleEventTree/eventTree")
print t
#uniquify
skimmers["eeee"]=Skimmer(t,cuts["eeee"],"bestZmass",vars4l,"eeeeFinal")
skimmers["eeee_SS"]=Skimmer(t,cuts["eeee_SS"],"bestZmass",vars4l,"eeee_SSFinal")
skimmers["eeeeAA"]=Skimmer(t,cuts["eeeeAA"],"BG",vars4l,"eeeeAAFinal",True)
skimmers["eeeeAI"]=Skimmer(t,cuts["eeeeAI"],"BG",vars4l,"eeeeAIFinal",True)
skimmers["eeeeIA"]=Skimmer(t,cuts["eeeeIA"],"BG",vars4l,"eeeeIAFinal",True)
skimmers["eeeeAA_SS"]=Skimmer(t,cuts["eeeeAA_SS"],"BG",vars4l,"eeeeAA_SSFinal")
skimmers["eeeeAI_SS"]=Skimmer(t,cuts["eeeeAI_SS"],"BG",vars4l,"eeeeAI_SSFinal")
skimmers["eeeeIA_SS"]=Skimmer(t,cuts["eeeeIA_SS"],"BG",vars4l,"eeeeIA_SSFinal")

t=f.Get("muMuMuMuEventTree/eventTree")
skimmers["mmmm"]=Skimmer(t,cuts["mmmm"],"bestZmass",vars4l,"mmmmFinal")
skimmers["mmmm_SS"]=Skimmer(t,cuts["mmmm_SS"],"bestZmass",vars4l,"mmmm_SSFinal")
skimmers["mmmmAA"]=Skimmer(t,cuts["mmmmAA"],"BG",vars4l,"mmmmAAFinal",True)
skimmers["mmmmAI"]=Skimmer(t,cuts["mmmmAI"],"BG",vars4l,"mmmmAIFinal",True)
skimmers["mmmmIA"]=Skimmer(t,cuts["mmmmIA"],"BG",vars4l,"mmmmIAFinal",True)
skimmers["mmmmAA_SS"]=Skimmer(t,cuts["mmmmAA_SS"],"BG",vars4l,"mmmmAA_SSFinal")
skimmers["mmmmAI_SS"]=Skimmer(t,cuts["mmmmAI_SS"],"BG",vars4l,"mmmmAI_SSFinal")
skimmers["mmmmIA_SS"]=Skimmer(t,cuts["mmmmIA_SS"],"BG",vars4l,"mmmmIA_SSFinal")

t=f.Get("muMuEleEleEventTree/eventTree")
skimmers["mmee"]=Skimmer(t,cuts["mmee"],"bestZmass",vars4l,"mmeeFinal")

#mmee and eemm come from "ONLY" branch
t=f.Get("muMuEleEleonlyEventTree/eventTree")
skimmers["mmee_o"]=Skimmer(t,cuts["mmee"],"bestZmass",vars4l,"mmee_oFinal")
skimmers["mmee_o_SS"]=Skimmer(t,cuts["mmee_SS"],"bestZmass",vars4l,"mmee_oSSFinal")
skimmers["mmee_oAA"]=Skimmer(t,cuts["mmeeAA"],"BG",vars4l,"mmeeAAFinal")
skimmers["mmee_oAI"]=Skimmer(t,cuts["mmeeAI"],"BG",vars4l,"mmeeAIFinal")
skimmers["mmee_oIA"]=Skimmer(t,cuts["mmeeIA"],"BG",vars4l,"mmeeIAFinal")
skimmers["mmee_oAA_SS"]=Skimmer(t,cuts["mmeeAA_SS"],"BG",vars4l,"mmeeAA_SSFinal")
skimmers["mmee_oAI_SS"]=Skimmer(t,cuts["mmeeAI_SS"],"BG",vars4l,"mmeeAI_SSFinal")
skimmers["mmee_oIA_SS"]=Skimmer(t,cuts["mmeeIA_SS"],"BG",vars4l,"mmeeIA_SSFinal")


t=f.Get("eleEleMuMuEventTree/eventTree")
skimmers["eemm_o"]=Skimmer(t,cuts["eemm"],"bestZmass",vars4l,"eemm_oFinal")
skimmers["eemm_o_SS"]=Skimmer(t,cuts["eemm_SS"],"bestZmass",vars4l,"eemm_oSSFinal")
skimmers["eemm_oAA"]=Skimmer(t,cuts["eemmAA"],"BG",vars4l,"eemmAAFinal")
skimmers["eemm_oAI"]=Skimmer(t,cuts["eemmAI"],"BG",vars4l,"eemmAIFinal")
skimmers["eemm_oIA"]=Skimmer(t,cuts["eemmIA"],"BG",vars4l,"eemmIAFinal")
skimmers["eemm_oAA_SS"]=Skimmer(t,cuts["eemmAA_SS"],"BG",vars4l,"eemmAA_SSFinal")
skimmers["eemm_oAI_SS"]=Skimmer(t,cuts["eemmAI_SS"],"BG",vars4l,"eemmAI_SSFinal")
skimmers["eemm_oIA_SS"]=Skimmer(t,cuts["eemmIA_SS"],"BG",vars4l,"eemmIA_SSFinal")

#temp.. don't do these because they take so damn long
#t=f.Get("muMuEventTree/eventTree")
#mmEvents=uniquify(t,cuts["mm"],"dummy",varsZ)
#mmTree=makeTree(mmEvents,"mmFinal")
#mmTree.Write()
#mmEvents.clear()
#t=f.Get("eleEleEventTree/eventTree")
#eeEvents=uniquify(t,cuts["ee"],"dummy",varsZ)
#eeTree=makeTree(eeEvents,"eeFinal")
#eeTree.Write()
#eeEvents.clear()

t=f.Get("muMuEleEventTree/eventTree")
skimmers["mme"]=Skimmer(t,cuts["mme"],"dummy",vars4l,"mmeFinal",True)

t=f.Get("muMuMuEventTree/eventTree")
skimmers["mmm"]=Skimmer(t,cuts["mmm"],"dummy",vars4l,"mmmFinal",True)

t=f.Get("eleEleEleEventTree/eventTree")
skimmers["eee"]=Skimmer(t,cuts["eee"],"dummy",vars4l,"eeeFinal",True)

t=f.Get("eleEleMuEventTree/eventTree")
skimmers["eem"]=Skimmer(t,cuts["eem"],"dummy",vars4l,"eemFinal",True)

for i in skimmers:
    fout=TFile(outfile,"update") #open/close this every time for memory relief?
    skimmers[i].setEvents()
    skimmers[i].makeTree().Write()
    skimmers[i].clear()
    fout.Close()

f.Close()

#make total 4l tree
fout2=TFile(outfile,"UPDATE")
llllTree=TChain("llllTree")
llllTree.Add(outfile+"/eeeeFinal")
llllTree.Add(outfile+"/mmeeFinal")
llllTree.Add(outfile+"/mmmmFinal")
llllTreeFinal=llllTree.CloneTree()
try:
    llllTreeFinal.SetName("llllTree")
    llllTreeFinal.Write()
except ReferenceError:
    print "No events in llllTree!"

#make mmee+eemm tree
for type in ["AAFinal","AIFinal","IAFinal","AA_SSFinal","AI_SSFinal","IA_SSFinal"]:
    mmeeSumTree=TChain("mmeeSumTree"+type)
    mmeeSumTree.Add(outfile+"/mmee"+type)
    mmeeSumTree.Add(outfile+"/eemm"+type)
    mmeeSumTreeFinal = mmeeSumTree.CloneTree()
    try:
        mmeeSumTreeFinal.SetName("mmeeSum"+type)
        mmeeSumTreeFinal.Write()
    except ReferenceError:
        print "No events in the combined eemm+mmee tree!"
fout2.Close()

#dump events for quick checks.
#import pickle
#pout=open('myEvents.pck','w')
#finalEvents={}
#finalEvents['eeee']=eeeeEvents
#finalEvents['mmmm']=mmmmEvents
#finalEvents['mmee']=mmeeEvents
#pickle.dump(finalEvents,pout)
#pout.close()
