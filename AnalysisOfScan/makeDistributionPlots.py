from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import matplotlib.pyplot as plt
import operator


energy=TH1D("","",400,0,400)
xposition=TH1D("","",100,-3,3)
yposition=TH1D("","",100,-3,3)
zcomponent=TH1D("","",100,0,1.2)

print "her"
teller=0
for line in open("../inputFiles/Degrader33um.txt",'r'):
    l=line.split()
    teller+=1
    if teller>100000:
        break
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
for line in open("../particlesOnDetector/D1_0D2_3000E1_4000E2_4000_scanning33um.txt",'r'):
    l=line.split()
    e,x,y,zc=float(l[5]),float(l[7]),float(l[8]),float(l[9])
    if e>10.0:
        continue
    energyD.Fill(e)
    xpositionD.Fill(x)
    ypositionD.Fill(y)
    zcomponentD.Fill(zc)

print "her da"

canvas=TCanvas()
energy.Scale(1.0/energy.Integral())
energyD.Scale(1.0/energyD.Integral())
energy.Draw("hist")
energyD.Draw("hist same")
canvas.SetLogy()
canvas.Print("../fig/energy.png")


canvas=TCanvas()
xposition.Scale(1.0/xposition.Integral())
xpositionD.Scale(1.0/xpositionD.Integral())
xposition.Draw("hist")
canvas.SetLogy()
print xposition.GetMaximum()
xpositionD.Draw("hist same")
canvas.Print("../fig/xposition.png")


canvas=TCanvas()
yposition.Scale(1.0/yposition.Integral())
ypositionD.Scale(1.0/ypositionD.Integral())
canvas.SetLogy()
yposition.Draw("hist")
ypositionD.Draw("hist same")
canvas.Print("../fig/yposition.png")

canvas=TCanvas()
zcomponent.Scale(1.0/zcomponent.Integral())
zcomponentD.Scale(1.0/zcomponentD.Integral())
canvas.SetLogy()
zcomponent.Draw("hist")
zcomponentD.Draw("hist same")
canvas.Print("../fig/zcomponents.png")





