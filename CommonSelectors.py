'''
File: CommonSelectors.py
Author: Ian Ross
Description: Defines the selector objects and supporting functions.
'''

# TEMP -- isolations are "noFSR" IAR 05.Feb.2013

from Selector import *

def stdIso(leg, cut, lep, wcut=True):
	temp=""
	if (lep=="ele"):
		temp="(max("+leg+"StdIsoEcaldR03-rho*(0.101*(abs("+leg+"Eta)<1.479)+0.046*(abs("+leg+"Eta)>1.479))";
		temp+="+"+leg+"StdIsoHcaldR03-rho*(0.021*(abs("+leg+"Eta)<1.479)+0.040*(abs("+leg+"Eta)>1.479))";
		temp+="+"+leg+"StdIsoTk,0.0)/"+leg+"Pt";
	elif (lep=="mu"):
		temp="(max("+leg+"StdIsoEcaldR03-rho*(0.074*(abs("+leg+"Eta)<1.479)+0.022*(abs("+leg+"Eta)>1.479))";
		temp+="+"+leg+"StdIsoHcaldR03-rho*(0.022*(abs("+leg+"Eta)<1.479)+0.030*(abs("+leg+"Eta)>1.479))";
		temp+="+"+leg+"StdIsoTk,0.0)/"+leg+"Pt";
	else:
		print "Bad lepton choice! Try harder!"
		return "0"
	if not wcut:
		return temp+")"
	else:
		temp+="<"+str(cut)+")";
		return temp;


common = Selector([
#	"HLT_Any",
	"z1Charge==0",
#	"z1Mass>40",
#	"z1Mass<120",
#    "z2Mass>60",
#    "z2Mass<120",
#    "(mass<110 || mass >140) && mass < 300",
	])

pt20_10 = Selector([
    "((z1l1Pt>20&&(z1l2Pt>10||z2l1Pt>10||z2l2Pt>10)) || (z1l2Pt>20&&(z1l1Pt>10||z2l1Pt>10||z2l2Pt>10)) || (z2l1Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l2Pt>10)) || (z2l2Pt>20&&(z1l1Pt>10||z1l2Pt>10||z2l1Pt>10)))"
    ])

z1ee = Selector([
	"z1l1MissHits<2",
	"z1l2MissHits<2",
    "abs(z1l1Eta)<2.5",
    "abs(z1l2Eta)<2.5",
    "abs(z1l1SIP)<4",
    "abs(z1l2SIP)<4",
    "abs(z1l1dXY)<0.5",
    "abs(z1l1dXY)<0.5",
    "abs(z1l1dz)<1.0",
    "abs(z1l1dz)<1.0",
	])

z1mm = Selector([
    "abs(z1l1Eta)<2.4",
    "abs(z1l2Eta)<2.4",
    "abs(z1l1SIP)<4",
    "abs(z1l2SIP)<4",
    "abs(z1l1dXY)<0.5",
    "abs(z1l1dXY)<0.5",
    "abs(z1l1dz)<1.0",
    "abs(z1l1dz)<1.0",
	])

z1relIso = Selector([
    "z1l1pfCombIso2012<0.40",
    "z1l2pfCombIso2012<0.40",
    ])

z2relIso = Selector([
    "z2l1pfCombIso2012<0.40",
    "z2l2pfCombIso2012<0.40",
    ])

z1relIsoNoFSR = Selector([ #for use in FR measurements
    "z1l1pfCombIso2012_noFSR<0.40",
    "z1l2pfCombIso2012_noFSR<0.40",
    ])

z2ee = Selector([
#	"z2Mass>60",
#	"z2Mass<120",
	"z2l1Pt>7",
	"z2l2Pt>7",
    "z2l1mvaNonTrigPass>0",
    "z2l2mvaNonTrigPass>0",
	"z2l1MissHits<2",
	"z2l2MissHits<2",
    "abs(z2l1SIP)<4",
    "abs(z2l2SIP)<4",
	])

z2mm = Selector([
#	"z2Mass>60",
#	"z2Mass<120",
	"z2l1Pt>5",
	"z2l2Pt>5",
    "z2l1isPF",
    "z2l2isPF",
    "(z2l1isGlobal||z2l1isTracker)",
    "(z2l2isGlobal||z2l2isTracker)",
    "abs(z2l1SIP)<4",
    "abs(z2l2SIP)<4",
    "abs(z2l1dz)<1",
    "abs(z2l2dz)<1",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
#	"z2l1ValidHits>10",
#	"z2l2ValidHits>10",
	])

z2tt = Selector([
	"z2l1Pt>20",
	"z2l2Pt>20",
	"z2l1EleVeto",
	"z2l2EleVeto",
	"z2l1MuVeto",
	"z2l2MuVeto",
	"z2l1MediumIsoCombDB",
	"z2l2MediumIsoCombDB",
	"z2Mass>30",
	"z2Mass<80"
	])

z2et = Selector([
	"z2l1Pt>10",
	"z2l2Pt>20",
	"(z2l1CiCTight&1)==1",
	"z2l1RelPFIsoDB<0.10",
#	"z2l1MissHits==0",
	"z2l2EleVeto",
	"z2l2MuVeto",
	"z2Mass>30",
	"z2Mass<80"
	])

z2mt = Selector([
	"z2l1Pt>10",
	"z2l2Pt>20",
	"z2l2EleVeto",
	"z2l2MuVetoTight",
#	"z2l1ValidHits>10",
	"z2l1RelPFIsoDB<0.15",
	"z2Mass>30",
	"z2Mass<80"
	])

z2em = Selector([
	"z2l1Pt>10",
	"z2l2Pt>10",
	"z2l1RelPFIsoDB<0.25",
	"(z2l1CiCTight&1)==1",
#	"z2l1MissHits<2",
	"z2Charge==0",
	"z2Mass<90"
])

z1StdIsoee = Selector([
	stdIso("z1l1",0.275,"ele",True),
	stdIso("z1l2",0.275,"ele",True)
	])

z1StdIsomm = Selector([
	stdIso("z1l1",0.275,"mu",True),
	stdIso("z1l2",0.275,"mu",True)
	])

z2StdIsoee = Selector([
	stdIso("z2l1",0.275,"ele",True),
	stdIso("z2l2",0.275,"ele",True)
	])

z2StdIsomm = Selector([
	stdIso("z2l1",0.275,"mu",True),
	stdIso("z2l2",0.275,"mu",True)
	])

eleDen = Selector([
    "met<25",
	"z2l1Pt>7",
    "abs(z2l1Eta)<2.5",
	"abs(z2l1SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "z2l1MissHits<2",
	])

eleNum = Selector([
	"met<25",
	"z2l1Pt>7",
    "abs(z2l1Eta)<2.5",
	"abs(z2l1SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l1dz)<1.0",
	"z2l1MissHits<2",
	"z2l1mvaNonTrigPass>0",
    "z2l1pfCombIso2012_noFSR<0.40",
	])

muDen = Selector([
	"met<25",
	"abs(z2l1Eta)<2.4",
	"z2l1Pt>5",
	"abs(z2l1SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "(z2l1isGlobal||z2l1isTracker)",
	])

muNum = Selector([
	"met<25",
	"abs(z2l1Eta)<2.4",
	"z2l1Pt>5",
	"abs(z2l1SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l1dz)<1.0",
	"z2l1isPF&&(z2l1isGlobal||z2l1isTracker)",
    "z2l1pfCombIso2012_noFSR<0.40",
	])

mmFakeable = Selector([
	"z2Mass>12",
	"z2Mass<120",
	"z2l1Pt>5",
	"z2l2Pt>5",
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1ValidHits>10",
	"z2l2ValidHits>10",
	])

eeFakeable = Selector([
	"z2Mass>12",
	"z2Mass<120",
	"z2l1Pt>7",
	"z2l2Pt>7",
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1MissHits<2",
	"z2l2MissHits<2",
#	"(z2l1CiCTight&1)==1",
#	"(z2l2CiCTight&1)==1",
	])

z1sip = Selector([
	"z1l1SIP<4",
	"z1l2SIP<4"
	])

z2sip = Selector([
	"z2l1SIP<4",
	"z2l2SIP<4"
	])

dz = Selector([
	"dz12<0.10",
	"dz13<0.10",
	"dz14<0.10"
	])

mmAI = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"abs(z2l1Eta)<2.4",
	"abs(z2l2Eta)<2.4",
	"((!z2l1isPF) || !(z2l1pfCombIso2012<0.40))",
    "(z2l1isTracker||z2l1isGlobal)", #'loose' req.
	"(z2l2isTracker||z2l2isGlobal)&&z2l2isPF",
	"z2l2pfCombIso2012<0.40"
	])

mmIA = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1Pt>5",
	"z2l2Pt>5",
	"abs(z2l1Eta)<2.4",
	"abs(z2l2Eta)<2.4",
    "(z2l2isTracker||z2l2isGlobal)",
	"((!z2l2isPF) || !(z2l2pfCombIso2012<0.40))",
	"(z2l1isTracker||z2l1isGlobal)&&z2l1isPF",
	"z2l1pfCombIso2012<0.40"
	])

mmAA = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1Pt>5",
	"z2l2Pt>5",
	"abs(z2l1Eta)<2.4",
	"abs(z2l2Eta)<2.4",
    "(z2l1isGlobal||z2l1isTracker)",
    "(z2l2isGlobal||z2l2isTracker)",

	"((!z2l1isPF) || !(z2l1pfCombIso2012<0.40))",
	"((!z2l2isPF) || !(z2l2pfCombIso2012<0.40))",
	])

eeAI = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1Pt>7",
	"z2l2Pt>7",
	"abs(z2l1Eta)<2.5",
	"abs(z2l2Eta)<2.5",
    "z2l1MissHits<2",
    "z2l2MissHits<2",
	"((!(z2l1mvaNonTrigPass>0)) || !(z2l1pfCombIso2012<0.40))",
	"z2l2mvaNonTrigPass>0",
	"z2l2pfCombIso2012<0.40"
	])

eeIA = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1Pt>7",
	"z2l2Pt>7",
	"abs(z2l1Eta)<2.5",
	"abs(z2l2Eta)<2.5",
    "z2l1MissHits<2",
    "z2l2MissHits<2",
	"((!(z2l2mvaNonTrigPass>0)) || !(z2l2pfCombIso2012<0.40))",
	"z2l1mvaNonTrigPass>0",
	"z2l1pfCombIso2012<0.40"
	])

eeAA = Selector([
	"abs(z2l1SIP)<4",
	"abs(z2l2SIP)<4",
    "abs(z2l1dXY)<0.5",
    "abs(z2l2dXY)<0.5",
    "abs(z2l1dz)<1.0",
    "abs(z2l2dz)<1.0",
	"z2l1Pt>7",
	"z2l2Pt>7",
	"abs(z2l1Eta)<2.5",
	"abs(z2l2Eta)<2.5",
    "z2l1MissHits<2",
    "z2l2MissHits<2",
	"((!(z2l1mvaNonTrigPass>0)) || !(z2l1pfCombIso2012<0.40))",
	"((!(z2l2mvaNonTrigPass>0)) || !(z2l2pfCombIso2012<0.40))",
	])

