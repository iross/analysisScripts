#!/usr/env/python

'''
File: addCorrections.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Embed TnP-based corrections in each event. Requires muon+electron
             files that hold TH2 with correction factors. Adds the corrections
             in a new tree, then friends the base tree with the new one.
'''

from RecoLuminosity.LumiDB import argparse
from ROOT import *
import numpy as N

def lepW(hist,lPt,lEta):
    """Return weight for lepton, given histogram."""
    weight=1.0
    bin=hist.FindBin(lPt,lEta)
    weight*=hist.GetBinContent(bin)
    if weight == 0.0:
        # ...assuming these TnP bins include pT above their boundaries..
        while weight == 0.0:
            weight=lepW(hist,99.9,lEta-lEta/20)

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
    elif "mmee" in outTree:
        leplist=['m','m','e','e']
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
    fe = TFile("/afs/hep.wisc.edu/cms/iross/analysis/zz535/src/UWAnalysis/analysisScripts/Electron_scale_factors_IDISOSIP_combined.root")
    fm = TFile("/afs/hep.wisc.edu/cms/iross/analysis/zz535/src/UWAnalysis/analysisScripts/muonid_hcp-05.10.2012-with-tk-v2.root")

    he=fe.Get("h_electron_scale_factor_RECO_ID_ISO_SIP")
    hm=fm.Get("TH2D_ALL_2012")

    fin = TFile(args.filein,"update")

    # loop over trees in a file
    stuff=[]
    for t in fin.GetListOfKeys():
        stuff.append(t)

    for t in stuff:
        weight=1.0
        up=1.0
        down=1.0
        print t.GetName()
        if "corr" in t.GetName() : continue

        if t.ReadObj().Class().InheritsFrom(TTree.Class()) is False:
            print t.GetName(),"is not a TTree.. skipping"
            continue
        tree = fin.Get(t.GetName())
        newtree = TTree(t.GetName()+"_corr",t.GetName()+"_corr")

        print "Working on",t.GetName(),":",tree.GetEntries(),"events found"

        leps,leplegs=parseLeps(t.GetName())
        n={args.branch: N.zeros(1,dtype=float), "scale_up": N.zeros(1,dtype=float), "scale_down": N.zeros(1,dtype=float)}
        pt=0.0
        eta=0.0

        newtree.Branch(args.branch,n[args.branch],args.branch+'/d')
        newtree.Branch("scale_up",n["scale_up"],"scale_up"+'/d')
        newtree.Branch("scale_down",n["scale_down"],"scale_down"+'/d')

        for i in tree:
            weight=1.0
            up=1.0
            down=1.0
            for l in range(len(leps)): # for each lepton, figure out type and get its weight.
                try:
                    pt = i.GetLeaf(leplegs[l]+"Pt").GetValue()
                    eta = i.GetLeaf(leplegs[l]+"Eta").GetValue()
                except ReferenceError: # this tree sucks and doesn't have the right vars
                    print "Trying to get",leplegs[l],"from tree",tree.GetName()
                    continue
                if leps[l] is "e":
                    weight*=lepW(he,pt,eta)
                    up*=0.98 + 0.0005*pt - 0.000004*pt**2
                    down*= 0.99 - 0.0002*pt + 0.000003*pt**2
                elif leps[l] is "m":
                    weight*=lepW(hm,pt,eta)
                    up*=0.98 + 0.0005*pt - 0.000004*pt**2
                    down*= 0.99 - 0.0002*pt + 0.000003*pt**2

            n[args.branch][0]=weight
            n["scale_up"][0]=up
            n["scale_down"][0]=down
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
    for tree in ["eeeeFinal","mmeeFinal","mmmmFinal"]:
        fout2.Get(tree).RemoveFriend(fout2.Get(tree+"_corr")) # needed so that combining the trees into llll doesn't hork up the corrections
    llllTree.Add(args.filein+"/eeeeFinal")
    llllTree.Add(args.filein+"/mmeeFinal")
    llllTree.Add(args.filein+"/mmmmFinal")
    llllTreeFinal=llllTree.CloneTree()

    llll_friend=TChain("llll_friend")
    llll_friend.Add(args.filein+"/eeeeFinal_corr")
    llll_friend.Add(args.filein+"/mmeeFinal_corr")
    llll_friend.Add(args.filein+"/mmmmFinal_corr")
    llll_friendFinal=llll_friend.CloneTree()

    try:
        llllTreeFinal.SetName("llllTree")
        llll_friendFinal.SetName("llllTree_corr")
        llll_friendFinal.Write()
        llllTreeFinal.AddFriend(llll_friendFinal.GetName())
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
