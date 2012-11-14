{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:53 2012) by ROOT version5.32/00
   TCanvas *can = new TCanvas("can", "can",1,1,600,576);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   can->SetHighLightColor(2);
   can->Range(-8.719512,196.1477,82.7439,1283.858);
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
   Double_t xAxis6[9] = {5, 10, 15, 20, 25, 30, 40, 50, 80}; 
   
   TH1F *eden = new TH1F("eden","eden",8, xAxis6);
   eden->SetBinContent(1,40540);
   eden->SetBinContent(2,31692);
   eden->SetBinContent(3,15330);
   eden->SetBinContent(4,8924);
   eden->SetBinContent(5,5876);
   eden->SetBinContent(6,6612);
   eden->SetBinContent(7,3493);
   eden->SetBinContent(8,4015);
   eden->SetBinContent(9,1677);
   eden->SetEntries(118159);
   eden->SetLineStyle(0);
   eden->SetMarkerStyle(20);
   eden->GetXaxis()->SetLabelFont(42);
   eden->GetXaxis()->SetLabelOffset(0.007);
   eden->GetXaxis()->SetLabelSize(0.05);
   eden->GetXaxis()->SetTitleSize(0.06);
   eden->GetXaxis()->SetTitleOffset(0.9);
   eden->GetXaxis()->SetTitleFont(42);
   eden->GetYaxis()->SetLabelFont(42);
   eden->GetYaxis()->SetLabelOffset(0.007);
   eden->GetYaxis()->SetLabelSize(0.05);
   eden->GetYaxis()->SetTitleSize(0.06);
   eden->GetYaxis()->SetTitleOffset(1.25);
   eden->GetYaxis()->SetTitleFont(42);
   eden->GetZaxis()->SetLabelFont(42);
   eden->GetZaxis()->SetLabelOffset(0.007);
   eden->GetZaxis()->SetLabelSize(0.05);
   eden->GetZaxis()->SetTitleSize(0.06);
   eden->GetZaxis()->SetTitleFont(42);
   eden->Draw("");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
