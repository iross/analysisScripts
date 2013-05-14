#!/usr/bin/python

'''
File: addCorrections.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Embed TnP-based corrections in each event. Requires muon+electron
             files that hold TH2 with correction factors
'''

from RecoLuminosity.LumiDB import argparse
from ROOT import *
import numpy as N

def lepW(hist,lPt,lEta):
    """Return weight for lepton, given histogram."""
    weight=1.0
    bin=hist.FindBin(lPt,lEta)
    weight*=hist.GetBinContent(bin)
    return weight

def parseLeps(outTree):
    """Parse the leptons in the event into a sorted list of lepton types"""
    leplist=[]
    lepaccess=[]
    if "eeee" in outTree:
        leplist=['e','e','e','e']
        lepaccess=['z1l1','z1l2','z2l1','z2l2']
    elif "eemm" in outTree:
        leplist=['e','e','m','m']
        lepaccess=['z1l1','z1l2','z2l1','z2l2']
    elif "mmmm" in outTree:
        leplist=['m','m','m','m']
        lepaccess=['z1l1','z1l2','z2l1','z2l2']
    elif "eee" in outTree:
        leplist=['e','e','e']
        lepaccess=['z1l1','z1l2','z2l1']
    elif "mmm" in outTree:
        leplist=['m','m','m']
        lepaccess=['z1l1','z1l2','z2l1']
    elif "emm" in outTree:
        leplist=['e','m','m']
        lepaccess=['z1l1','z1l2','z2l1']
    elif "mmm" in outTree:
        leplist=['m','e','e']
        lepaccess=['z1l1','z1l2','z2l1']
    elif "ee" in outTree:
        leplist=['e','e']
        lepaccess=['l1','l2']
    elif "mm" in outTree:
        leplist=['m','m']
        lepaccess=['l1','l2']
    return leplist,lepaccess



def main(args):
    fe = TFile("Electron_scale_factors_IDISOSIP_combined.root")
    fm = TFile("muonid_hcp-05.10.2012-with-tk-v2.root")

    he=fe.Get("h_electron_scale_factor_RECO_ID_ISO_SIP")
    hm=fm.Get("TH2D_ALL_2012")

    fin = TFile(args.filein,"update")

    # loop over trees in a file
    stuff=[]
    for t in fin.GetListOfKeys():
        stuff.append(t)

    for t in stuff:
        weight=1.0
        print t.GetName()
        if "corr" in t.GetName() : continue

        if t.ReadObj().Class().InheritsFrom(TTree.Class()) is False:
            print t.GetName(),"is not a TTree.. skipping"
            continue
        tree = fin.Get(t.GetName())
        newtree = TTree(t.GetName()+"_corr",t.GetName()+"_corr")

        print "Working on",t.GetName(),":",tree.GetEntries(),"events found"

        leps,leplegs=parseLeps(t.GetName())
        n={args.branch: N.zeros(1,dtype=float)}
        pt=0.0
        eta=0.0

        newtree.Branch(args.branch,n[args.branch],args.branch+'/d')

        for i in tree:
            weight=1.0
            for l in range(len(leps)): # for each lepton, figure out type and get its weight.
                try:
                    pt = i.GetLeaf(leplegs[l]+"Pt").GetValue()
                    eta = i.GetLeaf(leplegs[l]+"Eta").GetValue()
                except ReferenceError: # this tree sucks and doesn't have the right vars
                    continue
                if leps[l] is "e":
                    weight*=lepW(he,pt,eta)
                elif leps[l] is "m":
                    weight*=lepW(hm,pt,eta)

            n[args.branch][0]=weight
            newtree.Fill()
        newtree.Write()
        tree.AddFriend(newtree.GetName())
        tree.Write("",TObject.kOverwrite)

    fin.Close()
#    combineTrees
    #make total 4l tree
    fout2=TFile(args.filein,"UPDATE")
    fout2.Delete("llllTree*;*")
    llllTree=TChain("llllTree")
    llllTree.Add(args.filein+"/eeeeFinal")
    llllTree.Add(args.filein+"/mmeeFinal")
    llllTree.Add(args.filein+"/mmmmFinal")
    llllTreeFinal=llllTree.CloneTree()
    try:
        llllTreeFinal.SetName("llllTree")
        llllTreeFinal.Write()
    except ReferenceError:
        print "No events in llllTree!"

    fm.Close()
    fe.Close()

if __name__ == "__main__":
    print "..."
    parser = argparse.ArgumentParser(description='Make cleaned up trees (one entry per event, smaller set of vars, etc...)')
    parser.add_argument('--filein',type=str,required=True,default='',help='Input file')

    parser.add_argument('--branch',type=str,required=False,default='tnp_weight',help='Input file')

    args = parser.parse_args()
    main(args)
