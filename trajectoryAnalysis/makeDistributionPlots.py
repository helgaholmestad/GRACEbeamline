from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,TLegend
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import matplotlib.pyplot as plt
import operator


energy=TH1D("","",800,-1,800)
xposition=TH1D("","",100,-3,3.5)
yposition=TH1D("","",100,-3,3.5)
zcomponent=TH1D("","",100,0,1.2)
zangle=TH1D("","",900,0,90)
print "her"
teller=0
for line in open("../inputFiles/Degrader33um.txt",'r'):
    l=line.split()
    teller+=1
    #if teller>100000:
    #    break
    e,x,y,zc,xc,yc=float(l[0]),float(l[2]),float(l[3]),float(l[4]),float(l[5]),float(l[6])
    #if e>10.0 or zc<0.0:
    #    continue
    energy.Fill(e)
    #print "inni",(xc*xc+yc*yc)/zc
    #print "angel",180.0/np.pi*np.arctan(np.sqrt((xc*xc+yc*yc)/zc))
    zangle.Fill(180.0/np.pi*np.arctan(np.sqrt((xc*xc+yc*yc)/zc)))
    xposition.Fill(x)
    yposition.Fill(y)
    zcomponent.Fill(zc)

print "her da"


energyD=TH1D("","",800,-1,800)
xpositionD=TH1D("","",100,-3,3.5)
ypositionD=TH1D("","",100,-3,3.5)
zcomponentD=TH1D("","",100,0,1.2)
zangleD=TH1D("","",900,0,90)

print "her"
for line in open("/slagbjorn/homes/helga/ibsimuData/onDetector/D1_0D2_3000E1_3000E2_3000_scanning33um.txt",'r'):
    l=line.split()
    e,x,y,zc,xc,yc=float(l[5]),float(l[7]),float(l[8]),float(l[9]),float(l[10]),float(l[11])
    #if e>10.0:
    #    continue
    energyD.Fill(e)
    zangleD.Fill(180.0/np.pi*np.arctan(np.sqrt((xc*xc+yc*yc)/zc)))
    #print "inni",(xc*xc+yc*yc)/zc
    #print "angel",180.0/np.pi*np.arctan(np.sqrt((xc*xc+yc*yc)/zc))
    xpositionD.Fill(x)
    ypositionD.Fill(y)
    zcomponentD.Fill(zc)
#zcomponentD.Draw()
#input()
print "her da"
gStyle.SetOptStat("")




def printCanvas(histo,histoD,title,filename,maxy):
    canvas=TCanvas()
    histoD.SetFillColor(1)
    histo.SetFillColorAlpha(2,0.3)
    histo.SetLineColor(2)
    histoD.SetLineColor(1)
    histo.GetXaxis().SetTitle(title)
    histo.GetYaxis().SetTitle("Number of particles")
    #histo.Scale(1.0/histo.Integral())
    #histoD.Scale(scale)
    legend =TLegend(0.5,0.6,0.9,0.9);
    legend.AddEntry(histo,"Beam into GRACE")
    legend.AddEntry(histoD,"Beam reaching end-plate")
    histo.GetYaxis().SetRangeUser(1,maxy)
    histo.Draw("hist")
    legend.Draw("same")
    histoD.Draw("hist same")
    canvas.Update()
    canvas.SetLogy()
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/"+filename+".pdf")
    
printCanvas(xposition,xpositionD,"x-position [cm]","xposition",100000000)
printCanvas(yposition,ypositionD,"y-position [cm]","yposition",100000000)
#printCanvas(zcomponent,zcomponentD,"z-component of the momentum vector","zcomponent")
printCanvas(zangle,zangleD,"Deviation from beam z-direction","zcomponent",100000000)
printCanvas(energy,energyD,"energy [keV]","energy",100000000)
