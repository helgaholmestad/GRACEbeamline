from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import matplotlib.pyplot as plt
import operator


energy=TH1D("","",110,0,11)
xposition=TH1D("","",100,-3,3)
yposition=TH1D("","",100,-3,3)
zcomponent=TH1D("","",100,0,1.2)

print "her"
teller=0
for line in open("../inputFiles/Degrader33.txt",'r'):
    l=line.split()
    teller+=1
    #if teller>100000:
    #    break
    e,x,y,zc=float(l[0]),float(l[2]),float(l[3]),float(l[4])
    if e>10.0:
        continue
    energy.Fill(e)
    xposition.Fill(x)
    yposition.Fill(y)
    zcomponent.Fill(zc)

print "her da"

energyD=TH1D("","",110,0,11)
xpositionD=TH1D("","",100,-3,3)
ypositionD=TH1D("","",100,-3,3)
zcomponentD=TH1D("","",100,0,1.2)

print "her"
for line in open("/slagbjorn/homes/helga/ibsimuData/onDetector/D1_0D2_3000E1_4000E2_4000_scanning33um.txt",'r'):
    l=line.split()
    e,x,y,zc=float(l[5]),float(l[7]),float(l[8]),float(l[9])
    if e>10.0:
        continue
    energyD.Fill(e)
    xpositionD.Fill(x)
    ypositionD.Fill(y)
    zcomponentD.Fill(zc)

print "her da"
gStyle.SetOptStat("")




def printCanvas(histo,histoD,title,filename):
    canvas=TCanvas()
    histoD.SetFillColorAlpha(1,0.3)
    histo.SetFillColorAlpha(2,0.3)
    histo.SetLineColor(2)
    histoD.SetLineColor(1)
    histo.GetXaxis().SetTitle(title)
    histo.GetYaxis().SetTitle("Normalized frequency")
    histo.Scale(1.0/histo.Integral())
    histoD.Scale(1.0/histoD.Integral())
    histoD.Draw("hist")
    histo.Draw("hist same")
    canvas.Update()
    canvas.Print("../fig/"+filename+".pdf")
    
printCanvas(energy,energyD,"energy","energy")
printCanvas(xposition,xpositionD,"x-position [cm]","xposition")
printCanvas(yposition,ypositionD,"y-position [cm]","yposition")
printCanvas(zcomponent,zcomponentD,"z-component of the momentum vector","zcomponent")
