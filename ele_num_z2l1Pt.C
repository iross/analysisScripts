{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:53 2012) by ROOT version5.32/00
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
   Double_t xAxis5[9] = {5, 10, 15, 20, 25, 30, 40, 50, 80}; 
   
   TH1F *enum = new TH1F("enum","enum",8, xAxis5);
   enum->SetBinContent(1,1064);
   enum->SetBinContent(2,1187);
   enum->SetBinContent(3,710);
   enum->SetBinContent(4,510);
   enum->SetBinContent(5,425);
   enum->SetBinContent(6,567);
   enum->SetBinContent(7,378);
   enum->SetBinContent(8,522);
   enum->SetBinContent(9,331);
   enum->SetEntries(5694);
   enum->SetLineStyle(0);
   enum->SetMarkerStyle(20);
   enum->GetXaxis()->SetLabelFont(42);
   enum->GetXaxis()->SetLabelOffset(0.007);
   enum->GetXaxis()->SetLabelSize(0.05);
   enum->GetXaxis()->SetTitleSize(0.06);
   enum->GetXaxis()->SetTitleOffset(0.9);
   enum->GetXaxis()->SetTitleFont(42);
   enum->GetYaxis()->SetLabelFont(42);
   enum->GetYaxis()->SetLabelOffset(0.007);
   enum->GetYaxis()->SetLabelSize(0.05);
   enum->GetYaxis()->SetTitleSize(0.06);
   enum->GetYaxis()->SetTitleOffset(1.25);
   enum->GetYaxis()->SetTitleFont(42);
   enum->GetZaxis()->SetLabelFont(42);
   enum->GetZaxis()->SetLabelOffset(0.007);
   enum->GetZaxis()->SetLabelSize(0.05);
   enum->GetZaxis()->SetTitleSize(0.06);
   enum->GetZaxis()->SetTitleFont(42);
   enum->Draw("");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
