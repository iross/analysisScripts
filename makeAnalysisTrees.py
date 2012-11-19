from combTrees import *
from ROOT import *
import sys
import getopt
from RecoLuminosity.LumiDB import argparse

parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
parser.add_argument('--file',type=str,required=True,default='',help='Input file')
parser.add_argument('--out',type=str,required=True,default='',help='Output file')

args = parser.parse_args()

file=args.file
outfile=args.out

if ".root" not in file:
    file=file+".root"

#vars to store
vars4l = ["mass","z1Mass","z2Mass","z1l1Pt","z1l2Pt","z2l1Pt","z2l2Pt","bestZmass","subBestZmass","RUN","LUMI","EVENT","met","z1l1pfCombIso2012","z1l2pfCombIso2012","z2l1pfCombIso2012","z2l2pfCombIso2012","__WEIGHT__","__WEIGHT__noPU","z1l1pfCombIso2012_noFSR","z1l2pfCombIso2012_noFSR","z2l1pfCombIso2012_noFSR","z2l2pfCombIso2012_noFSR","weight","weightnoPU","z1l1Eta","z1l2Eta","z2l1Eta","z2l2Eta","massNoFSR","z1l1Phi","z1l2Phi","z2l1Phi","z2l2Phi","z2Charge","z1l1pfPhotonIso","z1l1PhotonIso","z1l2pfPhotonIso","z1l2PhotonIso","z2l1pfPhotonIso","z2l1PhotonIso","z2l2pfPhotonIso","z2l2PhotonIso"]
for thing in ["z2l1isGlobal","z2l1isTracker","z2l1isPF","z2l1mvaNonTrigPass","z2l1MissHits","z2l1mvaNonTrigPass"]:
    vars4l.append(thing)
varsZ = ["mass","l1Pt","l2Pt","l1Eta","l2Eta","l1Phi","l2Phi","RUN","LUMI","EVENT","met","l1pfCombIso2012","l2pfCombIso2012","__WEIGHT__","__WEIGHT__noPU","l1SIP","l2SIP"]

#set selections
cuts={}


#NOTE: don't apply mass cuts until AFTER best Z1 selection
cuts["eeee"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge==0")
cuts["mmmm"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge==0")
cuts["mmee"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge==0") #...this tree should have full selection applied right now
cuts["eeee_SS"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge!=0")
cuts["mmmm_SS"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge!=0")
cuts["mmee_SS"]=defineCuts(pt20_10.cuts(),z2ee.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge!=0") #...this tree should have full selection applied right now
cuts["eemm_SS"]=defineCuts(pt20_10.cuts(),z2mm.cuts(),z2RelPFIso.cuts(),"fourFour","z2Charge!=0") #...this tree should have full selection applied right now
cuts["mm"]=defineCuts("l1Pt>20&&l2Pt>10") #all cuts applied before trees filled
cuts["ee"]=defineCuts("l1Pt>20&&l2Pt>10") #all cuts applied before trees filled

cuts["eee"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eleDen.cuts())
cuts["eem"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),muDen.cuts())
cuts["mme"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eleDen.cuts())
cuts["mmm"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),muDen.cuts())

cuts["eeeeAA"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge==0")
cuts["eeeeAI"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge==0")
cuts["eeeeIA"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge==0")

cuts["mmeeAA"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge==0")
cuts["mmeeAI"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge==0")
cuts["mmeeIA"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge==0")

cuts["eemmAA"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge==0")
cuts["eemmAI"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge==0")
cuts["eemmIA"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge==0")

cuts["mmmmAA"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge==0")
cuts["mmmmAI"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge==0")
cuts["mmmmIA"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge==0")

cuts["eeeeAA_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge!=0")
cuts["eeeeAI_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge!=0")
cuts["eeeeIA_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge!=0")

cuts["mmeeAA_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeAA.cuts(),"z2Charge!=0")
cuts["mmeeAI_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeAI.cuts(),"z2Charge!=0")
cuts["mmeeIA_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),eeIA.cuts(),"z2Charge!=0")

cuts["eemmAA_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge!=0")
cuts["eemmAI_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge!=0")
cuts["eemmIA_SS"]=defineCuts(common.cuts(),z1ee.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge!=0")

cuts["mmmmAA_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmAA.cuts(),"z2Charge!=0")
cuts["mmmmAI_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmAI.cuts(),"z2Charge!=0")
cuts["mmmmIA_SS"]=defineCuts(common.cuts(),z1mm.cuts(),z1relIso.cuts(),mmIA.cuts(),"z2Charge!=0")

f=TFile(file,"update")
t=f.Get("eleEleEleEleEventTree/eventTree")

fout=TFile(outfile,"recreate")

#uniquify
eeeeEvents=uniquify(t,cuts["eeee"],"bestZmass",vars4l)
eeee_SSEvents=uniquify(t,cuts["eeee_SS"],"bestZmass",vars4l)
eeeeAAEvents=uniquify(t,cuts["eeeeAA"],"BG",vars4l)
eeeeAIEvents=uniquify(t,cuts["eeeeAI"],"BG",vars4l)
eeeeIAEvents=uniquify(t,cuts["eeeeIA"],"BG",vars4l)
eeeeTree=makeTree(eeeeEvents,"eeeeFinal")
eeee_SSTree=makeTree(eeee_SSEvents,"eeee_SSFinal")
eeeeAATree=makeTree(eeeeAAEvents,"eeeeAAFinal")
eeeeAITree=makeTree(eeeeAIEvents,"eeeeAIFinal")
eeeeIATree=makeTree(eeeeIAEvents,"eeeeIAFinal")
eeeeAA_SSEvents=uniquify(t,cuts["eeeeAA_SS"],"BG",vars4l)
eeeeAI_SSEvents=uniquify(t,cuts["eeeeAI_SS"],"BG",vars4l)
eeeeIA_SSEvents=uniquify(t,cuts["eeeeIA_SS"],"BG",vars4l)
eeeeAA_SSTree=makeTree(eeeeAA_SSEvents,"eeeeAA_SSFinal")
eeeeAI_SSTree=makeTree(eeeeAI_SSEvents,"eeeeAI_SSFinal")
eeeeIA_SSTree=makeTree(eeeeIA_SSEvents,"eeeeIA_SSFinal")

t=f.Get("muMuMuMuEventTree/eventTree")
mmmmEvents=uniquify(t,cuts["mmmm"],"bestZmass",vars4l)
mmmm_SSEvents=uniquify(t,cuts["mmmm_SS"],"bestZmass",vars4l)
mmmmAAEvents=uniquify(t,cuts["mmmmAA"],"BG",vars4l)
mmmmAIEvents=uniquify(t,cuts["mmmmAI"],"BG",vars4l)
mmmmIAEvents=uniquify(t,cuts["mmmmIA"],"BG",vars4l)
mmmmTree=makeTree(mmmmEvents,"mmmmFinal")
mmmm_SSTree=makeTree(mmmm_SSEvents,"mmmm_SSFinal")
mmmmAATree=makeTree(mmmmAAEvents,"mmmmAAFinal")
mmmmAITree=makeTree(mmmmAIEvents,"mmmmAIFinal")
mmmmIATree=makeTree(mmmmIAEvents,"mmmmIAFinal")
mmmmAA_SSEvents=uniquify(t,cuts["mmmmAA_SS"],"BG",vars4l)
mmmmAI_SSEvents=uniquify(t,cuts["mmmmAI_SS"],"BG",vars4l)
mmmmIA_SSEvents=uniquify(t,cuts["mmmmIA_SS"],"BG",vars4l)
mmmmAA_SSTree=makeTree(mmmmAA_SSEvents,"mmmmAA_SSFinal")
mmmmAI_SSTree=makeTree(mmmmAI_SSEvents,"mmmmAI_SSFinal")
mmmmIA_SSTree=makeTree(mmmmIA_SSEvents,"mmmmIA_SSFinal")

t=f.Get("muMuEleEleEventTree/eventTree")
mmeeEvents=uniquify(t,cuts["mmee"],"bestZmass",vars4l)
mmeeTree=makeTree(mmeeEvents,"mmeeFinal")

#mmee and eemm come from "ONLY" branch
t=f.Get("muMuEleEleonlyEventTree/eventTree")
mmee_SSEvents=uniquify(t,cuts["mmee_SS"],"bestZmass",vars4l)
mmee_SSTree=makeTree(mmee_SSEvents,"mmee_SSFinal")
mmeeAAEvents=uniquify(t,cuts["mmeeAA"],"BG",vars4l)
mmeeAIEvents=uniquify(t,cuts["mmeeAI"],"BG",vars4l)
mmeeIAEvents=uniquify(t,cuts["mmeeIA"],"BG",vars4l)
mmeeAATree=makeTree(mmeeAAEvents,"mmeeAAFinal")
mmeeAITree=makeTree(mmeeAIEvents,"mmeeAIFinal")
mmeeIATree=makeTree(mmeeIAEvents,"mmeeIAFinal")
mmeeAA_SSEvents=uniquify(t,cuts["mmeeAA_SS"],"BG",vars4l)
mmeeAI_SSEvents=uniquify(t,cuts["mmeeAI_SS"],"BG",vars4l)
mmeeIA_SSEvents=uniquify(t,cuts["mmeeIA_SS"],"BG",vars4l)
mmeeAA_SSTree=makeTree(mmeeAA_SSEvents,"mmeeAA_SSFinal")
mmeeAI_SSTree=makeTree(mmeeAI_SSEvents,"mmeeAI_SSFinal")
mmeeIA_SSTree=makeTree(mmeeIA_SSEvents,"mmeeIA_SSFinal")

t=f.Get("eleEleMuMuEventTree/eventTree")
eemm_SSEvents=uniquify(t,cuts["eemm_SS"],"bestZmass",vars4l)
eemm_SSTree=makeTree(eemm_SSEvents,"eemm_SSFinal")
eemmAAEvents=uniquify(t,cuts["eemmAA"],"BG",vars4l)
eemmAIEvents=uniquify(t,cuts["eemmAI"],"BG",vars4l)
eemmIAEvents=uniquify(t,cuts["eemmIA"],"BG",vars4l)
eemmAATree=makeTree(eemmAAEvents,"eemmAAFinal")
eemmAITree=makeTree(eemmAIEvents,"eemmAIFinal")
eemmIATree=makeTree(eemmIAEvents,"eemmIAFinal")
eemmAA_SSEvents=uniquify(t,cuts["eemmAA_SS"],"BG",vars4l)
eemmAI_SSEvents=uniquify(t,cuts["eemmAI_SS"],"BG",vars4l)
eemmIA_SSEvents=uniquify(t,cuts["eemmIA_SS"],"BG",vars4l)
eemmAA_SSTree=makeTree(eemmAA_SSEvents,"eemmAA_SSFinal")
eemmAI_SSTree=makeTree(eemmAI_SSEvents,"eemmAI_SSFinal")
eemmIA_SSTree=makeTree(eemmIA_SSEvents,"eemmIA_SSFinal")

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
mmeEvents=uniquify(t,cuts["mme"],"dummy",vars4l,True) #use 4l vars for now
mmeTree=makeTree(mmeEvents,"mmeFinal")
mmeTree.Write()
mmeEvents.clear()

t=f.Get("muMuMuEventTree/eventTree")
mmmEvents=uniquify(t,cuts["mmm"],"dummy",vars4l,True) #use 4l vars for now
mmmTree=makeTree(mmmEvents,"mmmFinal")
mmmTree.Write()
mmmEvents.clear()

t=f.Get("eleEleEleEventTree/eventTree")
eeeEvents=uniquify(t,cuts["eee"],"dummy",vars4l,True) #use 4l vars for now
eeeTree=makeTree(eeeEvents,"eeeFinal")
eeeTree.Write()
eeeEvents.clear()

t=f.Get("eleEleMuEventTree/eventTree")
eemEvents=uniquify(t,cuts["eem"],"dummy",vars4l,True) #use 4l vars for now
eemTree=makeTree(eemEvents,"eemFinal")
eemTree.Write()
eemEvents.clear()

#write trees
eeeeTree.Write()
eeee_SSTree.Write()
eeeeAATree.Write()
eeeeAITree.Write()
eeeeIATree.Write()
eeeeAA_SSTree.Write()
eeeeAI_SSTree.Write()
eeeeIA_SSTree.Write()
mmmmTree.Write()
mmmm_SSTree.Write()
mmmmAATree.Write()
mmmmAITree.Write()
mmmmIATree.Write()
mmmmAA_SSTree.Write()
mmmmAI_SSTree.Write()
mmmmIA_SSTree.Write()
mmeeTree.Write()
mmee_SSTree.Write()
mmeeAATree.Write()
mmeeAITree.Write()
mmeeIATree.Write()
eemm_SSTree.Write()
eemmAA_SSTree.Write()
eemmAI_SSTree.Write()
eemmIA_SSTree.Write()
mmeeAATree.Write()
mmeeAITree.Write()
mmeeIATree.Write()
eemmAA_SSTree.Write()
eemmAI_SSTree.Write()
eemmIA_SSTree.Write()


f.Close()
fout.Close()

#make total 4l tree
fout2=TFile(outfile,"UPDATE")
llllTree=TChain("llllTree")
llllTree.Add(outfile+"/eeeeFinal")
llllTree.Add(outfile+"/mmeeFinal")
llllTree.Add(outfile+"/mmmmFinal")
print llllTree.GetEntries()
llllTreeFinal=llllTree.CloneTree()
llllTreeFinal.SetName("llllTree")
llllTreeFinal.Write()
fout2.Close()

#dump them for quick event checks.
import pickle
pout=open('myEvents.pck','w')
finalEvents={}
finalEvents['eeee']=eeeeEvents
finalEvents['mmmm']=mmmmEvents
finalEvents['mmee']=mmeeEvents
pickle.dump(finalEvents,pout)
pout.close()


t
