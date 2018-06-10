from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os

shoot=3
rootdir="/home/helga/TimepixArticle/data/newTimepixFiles/20160528_33umAl_D1_0kV_D2_4kV_E1_4kV_E2_3kV_leadblocks/00_20160528_162324/test27_datadriven_AD/"
filename=rootdir+"data_"+str(shoot)+".dat"
histo=TH1D("","",200,-500,3000)
tmp=TH1D("","",40000,0,400000)

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    if float(columns[4])<6.0:
        continue
    tmp.Fill(float(columns[5]))
modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())
histo=TH1D("","",200,(modeTime-500)*1.0/1000,(modeTime+3000)*1.0/1000)

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    d=float(columns[5])
    histo.Fill(d*1.0/1000)
gStyle.SetOptStat("")


canvas=TCanvas()
histo.GetXaxis().SetTitle("Time of arrival [us]")
histo.GetYaxis().SetTitle("Number of pixels triggered ")
canvas.SetBottomMargin(0.14)
canvas.SetLeftMargin(0.14)
histo.GetYaxis().SetRangeUser(0,2100)
histo.GetXaxis().SetTitleSize(0.045)
histo.GetXaxis().SetLabelSize(0.04)
histo.GetYaxis().SetTitleSize(0.045)
histo.GetYaxis().SetLabelSize(0.044)
histo.GetXaxis().SetTitleOffset(0.83)
#histoD.SetFillColor(1)
histo.SetFillColorAlpha(4,0.3)
histo.SetLineColor(4)
histo.SetLineWidth(2)
histo.Draw("hist")
canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/timeDistro.pdf")
#canvas1.Print("/home/helga/Presantations/MedipixMeeting2017/fig/totalTimeDistro.pdf")
    
