#dSigma/dM_zz
#dSigma/dPt_zz
#dSigma/dEta_zz
#
#dSigna/dPt_z
#dSigma/dEta_z
#
#dSigma/dPt_leadinglepton
#dSigma/dEta_leadinglepton
#
#dSigma/dR_z_and_z
#dSigma/dPhi_l1_l2_in_one_z

python  unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzMass" --varmeas="mass" --bins="range(0,1050,50)" \
    --plotname="llll_mass" --lumi=19.6 --testFile="DATA_test.root" --xTitle="M_{ZZ}"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzPt" --varmeas="pt" --bins="range(0,175,25)" \
    --plotname="llll_pt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ P_{T}"
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzEta" --varmeas="eta" --bins="np.arange(-2.5,2.5,0.4)" \
    --plotname="llll_eta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ #eta"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1Eta*(z1Pt>z2Pt)+z2Eta*(z2Pt>z1Pt)" --varmeas="z1Eta*(z1Pt>z2Pt)+z2Eta*(z2Pt>z1Pt)" --bins="np.arange(-2.5,2.9,0.4)"\
    --plotname="llll_leadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --legY=0.65 --legX=0.2
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1Eta*(z1Pt<z2Pt)+z2Eta*(z2Pt<z1Pt)" --varmeas="z1Eta*(z1Pt<z2Pt)+z2Eta*(z2Pt<z1Pt)" --bins="np.arange(-2.5,2.9,0.4)"\
    --plotname="llll_subleadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --legY=0.65 --legX=0.2
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="max(z1Pt,z2Pt)" --varmeas="max(z1Pt,z2Pt)" --bins="range(0,425,25)"\
    --plotname="llll_leadingZpt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} P_{T}"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="sqrt((z1Eta-z2Eta)^2+(z1Phi-z2Phi)^2)" --varmeas="sqrt((z1Eta-z2Eta)^2+(z1Phi-z2Phi)^2)" --bins="0,0.5,1,1.5,3.0,6.0" \
    --plotname="llll_dR_Z" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta R (Z_{1}, Z_{2})" --legX=0.2

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs((z1Phi-z2Phi)+(6.28*((z1Phi-z2Phi)<-3.14))-6.28*(((z1Phi-z2Phi)>3.14)))" --varmeas="abs((z1Phi-z2Phi)+(6.28*((z1Phi-z2Phi)<-3.14))-6.28*(((z1Phi-z2Phi)>3.14)))" --bins="np.arange(0.0,3.34,0.2)" \
    --plotname="dPhi_Zs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta #phi (Z_{1}, Z_{2})" --legX=0.2

# this isn't necessarily the same "Z1" as the Z1Pt plot...
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs((z1l1Phi-z1l2Phi)+(6.28*((z1l1Phi-z1l2Phi)<-3.14))-6.28*(((z1l1Phi-z1l2Phi)>3.14)))" --varmeas="abs((z1l1Phi-z1l2Phi)+(6.28*((z1l1Phi-z1l2Phi)<-3.14))-6.28*(((z1l1Phi-z1l2Phi)>3.14)))" --bins="0,0.5,1.0,1.7,3.14" \
    --plotname="dPhi_Z1_leps" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta #phi (z1l1, z1l2)" --legX=0.2
