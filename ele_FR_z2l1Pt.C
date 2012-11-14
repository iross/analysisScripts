{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:53 2012) by ROOT version5.32/00
   TCanvas *can = new TCanvas("can", "can",0,0,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   can->SetHighLightColor(2);
   can->Range(0,0,1,1);
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
   
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(8);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);
   grae->SetMarkerStyle(20);
   grae->SetPoint(0,7.5,0.02624568);
   grae->SetPointError(0,2.5,2.5,0.000786749,0.0008023521);
   grae->SetPoint(1,12.5,0.03745425);
   grae->SetPointError(1,2.5,2.5,0.001057559,0.001077046);
   grae->SetPoint(2,17.5,0.04631442);
   grae->SetPointError(2,2.5,2.5,0.00167887,0.001718388);
   grae->SetPoint(3,22.5,0.05714926);
   grae->SetPointError(3,2.5,2.5,0.002425856,0.002492112);
   grae->SetPoint(4,27.5,0.07232811);
   grae->SetPointError(4,2.5,2.5,0.003332876,0.003430043);
   grae->SetPoint(5,35,0.08575318);
   grae->SetPointError(5,5,5,0.003403801,0.003487437);
   grae->SetPoint(6,45,0.1082164);
   grae->SetPointError(6,5,5,0.005184339,0.005334051);
   grae->SetPoint(7,65,0.1300125);
   grae->SetPointError(7,15,15,0.005248996,0.005371991);
   
   TH1F *Graph_Graph3 = new TH1F("Graph_Graph3","",100,0,87.5);
   Graph_Graph3->SetMinimum(0);
   Graph_Graph3->SetMaximum(1);
   Graph_Graph3->SetDirectory(0);
   Graph_Graph3->SetStats(0);
   Graph_Graph3->SetLineStyle(0);
   Graph_Graph3->SetMarkerStyle(20);
   Graph_Graph3->GetXaxis()->SetTitle("z2l1Pt");
   Graph_Graph3->GetXaxis()->SetLabelFont(42);
   Graph_Graph3->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3->GetXaxis()->SetTitleFont(42);
   Graph_Graph3->GetYaxis()->SetTitle("e Fake Rate");
   Graph_Graph3->GetYaxis()->SetLabelFont(42);
   Graph_Graph3->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3->GetYaxis()->SetTitleFont(42);
   Graph_Graph3->GetZaxis()->SetLabelFont(42);
   Graph_Graph3->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3);
   
   grae->Draw("ap");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
