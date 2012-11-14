{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:54 2012) by ROOT version5.32/00
   TCanvas *can = new TCanvas("can", "can",1,1,600,576);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   can->SetHighLightColor(2);
   can->Range(-16.0061,-0.1585366,90.70122,1.060976);
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
   Double_t xAxis7[9] = {5, 10, 15, 20, 25, 30, 40, 50, 80}; 
   
   TH1F *mnum = new TH1F("mnum","mnum",8, xAxis7);
   mnum->SetBinContent(1,2413);
   mnum->SetBinContent(2,526);
   mnum->SetBinContent(3,188);
   mnum->SetBinContent(4,92);
   mnum->SetBinContent(5,62);
   mnum->SetBinContent(6,75);
   mnum->SetBinContent(7,55);
   mnum->SetBinContent(8,78);
   mnum->SetBinContent(9,18);
   mnum->SetEntries(3507);
   mnum->SetLineStyle(0);
   mnum->SetMarkerStyle(20);
   mnum->GetXaxis()->SetLabelFont(42);
   mnum->GetXaxis()->SetLabelOffset(0.007);
   mnum->GetXaxis()->SetLabelSize(0.05);
   mnum->GetXaxis()->SetTitleSize(0.06);
   mnum->GetXaxis()->SetTitleOffset(0.9);
   mnum->GetXaxis()->SetTitleFont(42);
   mnum->GetYaxis()->SetLabelFont(42);
   mnum->GetYaxis()->SetLabelOffset(0.007);
   mnum->GetYaxis()->SetLabelSize(0.05);
   mnum->GetYaxis()->SetTitleSize(0.06);
   mnum->GetYaxis()->SetTitleOffset(1.25);
   mnum->GetYaxis()->SetTitleFont(42);
   mnum->GetZaxis()->SetLabelFont(42);
   mnum->GetZaxis()->SetLabelOffset(0.007);
   mnum->GetZaxis()->SetLabelSize(0.05);
   mnum->GetZaxis()->SetTitleSize(0.06);
   mnum->GetZaxis()->SetTitleFont(42);
   mnum->Draw("");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
