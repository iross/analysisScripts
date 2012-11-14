{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:55 2012) by ROOT version5.32/00
   TCanvas *can = new TCanvas("can", "can",1,1,600,576);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   can->SetHighLightColor(2);
   can->Range(-8.719512,-401.6762,82.7439,2688.141);
   can->SetFillColor(0);
   can->SetBorderMode(0);
   can->SetBorderSize(2);
   can->SetTickx(1);
   can->SetTicky(1);
   can->SetLeftMargin(0.15);
   can->SetRightMargin(0.03);
   can->SetTopMargin(0.05);
   can->SetBottomMargin(0.13);
   can->SetFrameFillStyle(0);
   can->SetFrameLineWidth(2);
   can->SetFrameBorderMode(0);
   Double_t xAxis8[9] = {5, 10, 15, 20, 25, 30, 40, 50, 80}; 
   
   TH1F *mden = new TH1F("mden","mden",8, xAxis8);
   mden->SetBinContent(1,63245);
   mden->SetBinContent(2,14922);
   mden->SetBinContent(3,6556);
   mden->SetBinContent(4,3470);
   mden->SetBinContent(5,2045);
   mden->SetBinContent(6,2189);
   mden->SetBinContent(7,1129);
   mden->SetBinContent(8,1231);
   mden->SetBinContent(9,751);
   mden->SetEntries(95538);
   mden->SetLineStyle(0);
   mden->SetMarkerStyle(20);
   mden->GetXaxis()->SetLabelFont(42);
   mden->GetXaxis()->SetLabelOffset(0.007);
   mden->GetXaxis()->SetLabelSize(0.05);
   mden->GetXaxis()->SetTitleSize(0.06);
   mden->GetXaxis()->SetTitleOffset(0.9);
   mden->GetXaxis()->SetTitleFont(42);
   mden->GetYaxis()->SetLabelFont(42);
   mden->GetYaxis()->SetLabelOffset(0.007);
   mden->GetYaxis()->SetLabelSize(0.05);
   mden->GetYaxis()->SetTitleSize(0.06);
   mden->GetYaxis()->SetTitleOffset(1.25);
   mden->GetYaxis()->SetTitleFont(42);
   mden->GetZaxis()->SetLabelFont(42);
   mden->GetZaxis()->SetLabelOffset(0.007);
   mden->GetZaxis()->SetLabelSize(0.05);
   mden->GetZaxis()->SetTitleSize(0.06);
   mden->GetZaxis()->SetTitleFont(42);
   mden->Draw("");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
