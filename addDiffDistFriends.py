#!/usr/env/python

'''
File: addDiffDistFriends.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Embed new variables in a friendly branch in a TFile. The
             variables added are those to be used in the differential
             distributions.
'''

from RecoLuminosity.LumiDB import argparse
from ROOT import *
from addCorrections import parseLeps, ruinFriendships
from combTrees import dPhi
import pdb
import numpy as N

def main(args):
    fin = TFile(args.filein,"update")
    print args.trees
    stuff=[]
    if "all" in args.trees:
        for t in fin.GetListOfKeys():
            if t.ReadObj().Class().InheritsFrom(TTree.Class()) is True:
                stuff.append(t.GetName())
            else:
                continue
    else:
        stuff=[i for i in args.trees]
    for i in stuff:
        if "genEventTree" not in i and "mmee" not in i and "eemm" not in i and "eeee" not in i and "mmmm" not in i and "llll" not in i:
            stuff.remove(i)

    # vars needed as inputs: z1Eta, z2Eta, z1Pt, z2Pt, z1Phi, z2Phi, mass, pt, zilj[Eta, Phi, Pt], z1Mass, z2Mass
    ins=["zzMass", "zzPt", "zzEta", "z1Pt", "z2Pt", "z1Eta", "z2Eta", "z1Phi", "z2Phi"]
    for i in ["z1l1Pt", "z1l1Eta", "z1l1Phi", "z1Mass", "z1l2Pt", "z1l2Eta", "z1l2Phi", "z2Mass"]:
        ins.append(i)
    for i in ["z2l1Pt", "z2l1Eta", "z2l1Phi", "z2l2Pt", "z2l2Eta", "z2l2Phi"]:
        ins.append(i)
    inputVars={}
    fin = TFile(args.filein,"update")

    for t in stuff:
        fin = TFile(args.filein,"update")
        tree = fin.Get(t)
        newtree = TTree(tree.GetName()+"_moreVars",tree.GetName()+"_moreVars")

        n={}
        leplegs=["z1l1","z1l2","z2l1","z2l2"]

        for i in ins:
            inputVars[i] = -137.0


        # ouput vars : z_Eta (leading by Pt), z_Pt (leading by Pt), dR between Z, dPhi between Z, leading lepton Pt
        outs=["z1_eta_by_pt", "z2_eta_by_pt", "z1_pt_by_pt","z2_pt_by_pt", "dR_Zs", "dPhi_Zs", "leading_lep_pt"]
        for outvar in outs:
            # TODO do I need these genlevel for reco branch??
            n[outvar] = N.zeros(1,dtype=float)
            newtree.Branch(outvar, n[outvar],outvar+"/d")

        for i in tree:
            # get ins
            # these will have to be different if it's the truth/measured tree...
            for var in ["Mass" , "Pt", "Eta"]:
                if "gen" in tree.GetName():
                    inputVars["zz"+var] = i.GetLeaf("zz"+var).GetValue()
                else:
                    inputVars["zzMass"] = i.GetLeaf("mass").GetValue()
#                    inputVars["zzEta"] = i.GetLeaf("eta").GetValue()
                    inputVars["zzPt"] = i.GetLeaf("pt").GetValue()
            for  var in ["Mass", "Pt", "Eta", "Phi"]:
                inputVars["z1"+var] = i.GetLeaf("z1"+var).GetValue()
            for  var in ["Mass", "Pt", "Eta", "Phi"]:
                inputVars["z2"+var] = i.GetLeaf("z2"+var).GetValue()
            for l in range(len(leplegs)): # for each lepton, figure out type and get its weight.
                try:
                    inputVars[leplegs[l]+"Pt"] = i.GetLeaf(leplegs[l]+"Pt").GetValue()
                    inputVars[leplegs[l]+"Eta"] = i.GetLeaf(leplegs[l]+"Eta").GetValue()
                    inputVars[leplegs[l]+"Phi"] = i.GetLeaf(leplegs[l]+"Phi").GetValue()
                except ReferenceError: # this tree sucks and doesn't have the right vars
                    print "Trying to get",leplegs[l],"from tree",tree.GetName()
                    continue

            #set outs
            if inputVars["z1Pt"]>inputVars["z2Pt"]:
                n["z1_eta_by_pt"][0]=inputVars["z1Eta"]
                n["z1_pt_by_pt"][0]=inputVars["z1Pt"]
                n["z2_eta_by_pt"][0]=inputVars["z2Eta"]
                n["z2_pt_by_pt"][0]=inputVars["z2Pt"]
            else:
                n["z1_eta_by_pt"][0]=inputVars["z2Eta"]
                n["z1_pt_by_pt"][0]=inputVars["z2Pt"]
                n["z2_eta_by_pt"][0]=inputVars["z1Eta"]
                n["z2_pt_by_pt"][0]=inputVars["z1Pt"]
            n["leading_lep_pt"][0]=max(max(max(inputVars["z1l1Pt"],inputVars["z1l2Pt"]),inputVars["z2l1Pt"]),inputVars["z2l2Pt"])
            n["dR_Zs"][0]=sqrt( (inputVars["z1Eta"]-inputVars["z2Eta"])**2 + (inputVars["z1Phi"]-inputVars["z2Phi"])**2)
            n["dPhi_Zs"][0] = dPhi(inputVars["z1Phi"], inputVars["z2Phi"])
            newtree.Fill()
        print tree.GetName(),"has",tree.GetEntries(),"entries"
        print newtree.GetName(),"has",tree.GetEntries(),"entries"
        newtree.Write()
        tree.AddFriend(newtree.GetName())
        tree.Write("",TObject.kOverwrite)
        fin.Close()



if __name__ == "__main__":
    print "..."
    parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
    parser.add_argument('--filein',dest="filein",type=str,required=True,default='',help='Input file')
    parser.add_argument('--trees',dest="trees",type=str,nargs="+",required=True,default='',help='Input file')

    args = parser.parse_args()
    main(args)
