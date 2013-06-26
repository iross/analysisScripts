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

#python  unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzMass" --varmeas="mass" --tmVar="gMass" --bins="range(0,1050,50)" \
#    --plotname="llll_mass" --lumi=19.6 --testFile="DATA_test.root" --xTitle="M_{ZZ}" --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzPt" --varmeas="pt" --tmVar="gPt" --bins="range(0,175,25)" \
#    --plotname="llll_pt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ P_{T}" --wt="tnp_weight_final"
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="zzEta" --varmeas="eta" --bins="np.arange(-2.5,2.5,0.4)" \
#    --plotname="llll_eta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="ZZ #eta" --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1_eta_by_pt" --varmeas="z1_eta_by_pt" --tmVar="z1_eta_by_pt" --bins="np.arange(-2.5,2.9,0.4)"\
#    --plotname="llll_leadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --legY=0.65 --legX=0.2 --wt="tnp_weight_final"
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z2_eta_by_pt" --varmeas="z2_eta_by_pt" --tmVar="z2_eta_by_pt" --bins="np.arange(-2.5,2.9,0.4)"\
#    --plotname="llll_subleadingZeta" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --legY=0.65 --legX=0.2 --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs(z1_eta_by_pt)" --varmeas="abs(z1_eta_by_pt)" --tmVar="abs(z1_eta_by_pt)" --bins="np.arange(0,2.9,0.2)"\
#    --plotname="llll_leadingZeta_abs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} #eta" --legY=0.65 --legX=0.65 --wt="tnp_weight_final"
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="abs(z2_eta_by_pt)" --varmeas="abs(z2_eta_by_pt)" --tmVar="abs(z2_eta_by_pt)" --bins="np.arange(0,2.9,0.2)"\
#    --plotname="llll_subleadingZeta_abs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{2} #eta" --legY=0.65 --legX=0.65 --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="z1_pt_by_pt" --varmeas="z1_pt_by_pt" --tmVar="z1_pt_by_pt" --bins="range(0,425,25)"\
#    --plotname="llll_leadingZpt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Z_{1} P_{T}" --wt="tnp_weight_final"
#
#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="dR_Zs" --varmeas="dR_Zs" --tmVar="dR_Zs" --bins="0,0.5,1,1.5,3.0,6.0" \
#    --plotname="llll_dR_Z" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta R (Z_{1}, Z_{2})" --legX=0.2 --wt="tnp_weight_final"

python unfolding.py --tree="llllTree" --nice="llll" --vartrue="dPhi_Zs" --varmeas="dPhi_Zs" --tmVar="dPhi_Zs" --bins="np.arange(0.0,3.34,0.2)" \
    --plotname="dPhi_Zs" --lumi=19.6 --testFile="DATA_test.root" --xTitle="#Delta #phi (Z_{1}, Z_{2})" --legX=0.2 --wt="tnp_weight_final"

#python unfolding.py --tree="llllTree" --nice="llll" --vartrue="leading_lep_pt" --varmeas="leading_lep_pt" --tmVar="leading_lep_pt" --bins="range(0,170,10)" \
#    --plotname="leadingLep_pt" --lumi=19.6 --testFile="DATA_test.root" --xTitle="Leading lepton p_{T}" --legX=0.6 --wt="tnp_weight_final"
