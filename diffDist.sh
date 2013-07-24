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

python  unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzMass" --varmeas="mass" --tmVar="gMass" --bins="0,200,250,300,350,400,500,600,800" \
    --plotname="llll_mass" --lumi=19.6 --testFile="DATA_test.root" --xTitle="m_{ZZ}" --xUnits="GeV" --wt="tnp_weight_final" --legY=0.60

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzPt" --varmeas="pt" --tmVar="gPt" --bins="0,25,50,75,100,150" \
    --plotname="llll_pt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ p_{T}" --xUnits="GeV" --wt="tnp_weight_final" --legY=0.60
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzEta" --varmeas="eta" --bins="np.arange(-2.5,2.5,0.4)" \
#    --plotname="llll_eta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ #eta" --xUnits="GeV"--wt="tnp_weight_final"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1_eta_by_pt" --varmeas="z1_eta_by_pt" --tmVar="z1_eta_by_pt" --bins="np.arange(-3.5,3.9,0.4)"\
    --plotname="llll_leadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --xUnits="" --legY=0.65 --legX=0.22 --wt="tnp_weight_final" --yMax=0.22
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z2_eta_by_pt" --varmeas="z2_eta_by_pt" --tmVar="z2_eta_by_pt" --bins="np.arange(-3.5,3.9,0.4)"\
    --plotname="llll_subleadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --xUnits="" --legY=0.65 --legX=0.22 --wt="tnp_weight_final"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1_eta_by_pt" --varmeas="z1_eta_by_pt" --tmVar="z1_eta_by_pt" --bins="np.arange(-3.5,3.9,0.4)"\
    --plotname="llll_leadingZeta_extended" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --xUnits="" --legY=0.65 --legX=0.22 --wt="tnp_weight_final" --yMax=0.22
python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z2_eta_by_pt" --varmeas="z2_eta_by_pt" --tmVar="z2_eta_by_pt" --bins="np.arange(-3.5,3.9,0.4)"\
    --plotname="llll_subleadingZeta_extended" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --xUnits="" --legY=0.65 --legX=0.22 --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs(z1_eta_by_pt)" --varmeas="abs(z1_eta_by_pt)" --tmVar="abs(z1_eta_by_pt)" --bins="np.arange(0,2.9,0.2)"\
#    --plotname="llll_leadingZeta_abs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --xUnits="" --legY=0.65 --legX=0.65 --wt="tnp_weight_final"
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs(z2_eta_by_pt)" --varmeas="abs(z2_eta_by_pt)" --tmVar="abs(z2_eta_by_pt)" --bins="np.arange(0,2.9,0.2)"\
#    --plotname="llll_subleadingZeta_abs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --xUnits="" --legY=0.65 --legX=0.65 --wt="tnp_weight_final"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1_pt_by_pt" --varmeas="z1_pt_by_pt" --tmVar="z1_pt_by_pt" --bins="0,25,50,75,100,125,150,200,250"\
    --plotname="llll_leadingZpt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} p_{T}" --xUnits="GeV" --wt="tnp_weight_final" --legY=0.6

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="dR_Zs" --varmeas="dR_Zs" --tmVar="dR_Zs" --bins="0,1.0,2.0,3.0,4.0,5.0,6.0" \
    --plotname="llll_dR_Z" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta R (Z_{1}, Z_{2})" --xUnits="" --legX=0.22 --wt="tnp_weight_final" --legY=0.6

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="dPhi_Zs" --varmeas="dPhi_Zs" --tmVar="dPhi_Zs" --bins="0,1.5,2.0,2.25,2.5,2.75,3.0,3.25" \
    --plotname="dPhi_Zs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta #phi (Z_{1}, Z_{2})" --xUnits="" --legX=0.22 --wt="tnp_weight_final" --legY=0.6

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="leading_lep_pt" --varmeas="leading_lep_pt" --tmVar="leading_lep_pt" --bins="20,30,40,50,60,70,80,90,100,110,120,130,140" \
    --plotname="leadingLep_pt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Lead. lep. p_{T}" --xUnits="GeV" --legX=0.6 --wt="tnp_weight_final" --legY=0.6
