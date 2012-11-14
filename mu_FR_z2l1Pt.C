{
//=========Macro generated from canvas: can/can
//=========  (Tue Nov 13 09:36:54 2012) by ROOT version5.32/00
   TCanvas *can = new TCanvas("can", "can",1,1,600,576);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   can->SetHighLightColor(2);
   can->Range(-8.719512,-4834.668,82.7439,44975.47);
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
   grae->SetPoint(0,7.5,0.03815321);
   grae->SetPointError(0,2.5,2.5,0.0007573704,0.0007671208);
   grae->SetPoint(1,12.5,0.03524997);
   grae->SetPointError(1,2.5,2.5,0.001490001,0.001531585);
   grae->SetPoint(2,17.5,0.02867602);
   grae->SetPointError(2,2.5,2.5,0.00201532,0.002111346);
   grae->SetPoint(3,22.5,0.02651297);
   grae->SetPointError(3,2.5,2.5,0.002640103,0.002822459);
   grae->SetPoint(4,27.5,0.03031785);
   grae->SetPointError(4,2.5,2.5,0.003644796,0.003951853);
   grae->SetPoint(5,35,0.03426222);
   grae->SetPointError(5,5,5,0.003751623,0.004035966);
   grae->SetPoint(6,45,0.04871568);
   grae->SetPointError(6,5,5,0.006149308,0.006683399);
   grae->SetPoint(7,65,0.06336312);
   grae->SetPointError(7,15,15,0.00671351,0.007187127);
   
   TH1F *Graph_Graph4 = new TH1F("Graph_Graph4","",100,0,87.5);
   Graph_Graph4->SetMinimum(0);
   Graph_Graph4->SetMaximum(1);
   Graph_Graph4->SetDirectory(0);
   Graph_Graph4->SetStats(0);
   Graph_Graph4->SetLineStyle(0);
   Graph_Graph4->SetMarkerStyle(20);
   Graph_Graph4->GetXaxis()->SetTitle("z2l1Pt");
   Graph_Graph4->GetXaxis()->SetLabelFont(42);
   Graph_Graph4->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph4->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph4->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph4->GetXaxis()->SetTitleFont(42);
   Graph_Graph4->GetYaxis()->SetTitle("#mu Fake Rate");
   Graph_Graph4->GetYaxis()->SetLabelFont(42);
   Graph_Graph4->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph4->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph4->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph4->GetYaxis()->SetTitleFont(42);
   Graph_Graph4->GetZaxis()->SetLabelFont(42);
   Graph_Graph4->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph4->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph4->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph4);
   
   grae->Draw("ap");
   can->Modified();
   can->cd();
   can->SetSelected(can);
}
