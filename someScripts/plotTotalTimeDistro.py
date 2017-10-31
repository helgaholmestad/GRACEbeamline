from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os

shoot=3
rootdir="/home/helga/TimepixArticle/data/newTimepixFiles/20160528_33umAl_D1_0kV_D2_4kV_E1_4kV_E2_3kV_leadblocks/00_20160528_162324/test27_datadriven_AD/"
filename=rootdir+"data_"+str(shoot)+".dat"
timeDistro=TH1D("","",200,-500,3000)
tmp=TH1D("","",40000,0,400000)

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    if float(columns[4])<6.0:
        continue
    tmp.Fill(float(columns[5]))
modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    d=float(columns[5])-modeTime
    timeDistro.Fill(d)

timeDistro.Draw()


canvas1=TCanvas()
timeDistro.GetXaxis().SetTitle("Time of arrival [ns]")
timeDistro.GetXaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitle("Frequency ")
timeDistro.GetYaxis().SetTitleOffset(0.9)
timeDistro.Draw()
canvas1.Print("/home/helga/gitThesis/thesis/Grace/fig/timeDistro.pdf")
#canvas1.Print("/home/helga/Presantations/MedipixMeeting2017/fig/totalTimeDistro.pdf")
    
