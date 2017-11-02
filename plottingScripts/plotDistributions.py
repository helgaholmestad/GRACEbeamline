from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,TLegend,gStyle
gROOT.Reset()
import numpy as np
import sys
import os
import os.path
import re
import math
gStyle.SetOptStat("")
 

def findKineticEnergy(time):
    c=299792458.0
    massProton=938.0/(c*c)
    sign=1.0
    if time<0:
        sign=-1.0
    time=time*1.0/(math.pow(10,9))
    v2=math.pow((1.48/time),2)
    kineticEnergy=v2*massProton*1000.0/2
    return sign*kineticEnergy


def findTime(energy):
    c=299792458.0
    massProton=938.0/(c*c)
    v2=energy*2/(massProton*1000.0)
    time=1.48/math.sqrt(v2)
    time=time*math.pow(10,9)
    return time

def fillHistogram(filename):
    c=299792458.0
    massProton=938.0/(c*c)
    histo=TH1D("","",50,0,10)
    histo.Sumw2()
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new":
            continue
        if columns[0].startswith("D1") or columns[0]=="noFile":
            continue
        time=float(columns[0])
        #removing false hits from next event
        if time>10000:
            continue
        histo.Fill(findKineticEnergy(time))
    histo.Scale(1.0/histo.Integral())
    return histo

def fillHistogram1500(filename):
    histo=TH1D("","",50,0,10)
    histo.Sumw2()
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new":
            continue
        if columns[0].startswith("D1") or columns[0]=="noFile":
            continue
        time=float(columns[0])
        if time>10000:
            continue
        histo.Fill(findKineticEnergy(time))
    histo.Scale(1.0/histo.Integral())
    return histo



def fillHistogramSimu1500(filename):
    histo=TH1D("","",50,0,10)
    for line in open(filename):
        columns=line.split()
        energy=float(columns[3])
        time=findTime(energy)+np.random.normal(145,100)
        histo.Fill(findKineticEnergy(time))
    histo.Scale(1.0/histo.Integral())
    return histo




def fillHistogramSimu(filename):
    histo=TH1D("","",50,0,10)
    for line in open(filename):
        columns=line.split()
        energy=float(columns[3])
        time=findTime(energy)+np.random.normal(145,100)
        histo.Fill(findKineticEnergy(time))
    histo.Scale(1.0/histo.Integral())
    return histo



def calculateFWHM(histo):
    lowerBin=histo.FindFirstBinAbove(histo.GetMaximum()/2);
    upperBin=histo.FindLastBinAbove(histo.GetMaximum()/2)
    fwhm = histo.GetBinCenter(upperBin) - histo.GetBinCenter(lowerBin);
    return fwhm

#list of files for scan1
listOfFiles=[ "D1_0kV_D2_3kV_E1_3kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_5kV_E2_3kV"]
listOfFilesSimu=["D1_0D2_3000E1_3000E2_3000_scanning33um.txt","D1_0D2_3000E1_4000E2_3000_scanning33um.txt","D1_0D2_3000E1_5000E2_3000_scanning33um.txt"]
rootDirSimu="/home/helga/GRACESimu/ibsimuData/onDetector"
rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan1"
counter=0

for config in listOfFiles:
    legend =TLegend(0.7,0.7,0.90,0.90);
    canvas=TCanvas()
    histodata=fillHistogram(rootDirData+"/"+config+"_data.txt")
    histosimu=fillHistogramSimu(rootDirSimu+"/"+listOfFilesSimu[counter])
    histodata.SetLineColor(1)
    #histodata.SetFillColorAlpha(colorCounter,1)
    legend.AddEntry(histodata,"Data")
    histosimu.GetXaxis().SetTitle("Kinetic energy [keV]")
    histosimu.GetYaxis().SetTitle("normalized frequency")
    histosimu.SetFillColorAlpha(4,0.6)
    histosimu.SetLineColor(4)
    histodata.SetLineWidth(2)
    legend.AddEntry(histosimu,"simulation")
    histosimu.Draw("hist")
    histodata.Draw("ehistsame")
    legend.Draw("same")
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/compare"+config+".pdf")
    counter+=1
    print "  "
    print "  "
    print "the config",config
    print "  "
    print "&   "+str(histodata.GetMean())+ " &  "+str(histosimu.GetMean())+ " & "+ str(calculateFWHM(histodata))+  "  &  "+str(calculateFWHM(histosimu))
    print "   "
    print "  "
    print "  "
    print "  "

    
listOfFiles=[ "D1_0kV_D2_3kV_E1_4kV_E2_2kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_4kV"]
listOfFilesSimu=["D1_0D2_3000E1_4000E2_2000_scanning33um.txt","D1_0D2_3000E1_4000E2_3000_scanning33um.txt","D1_0D2_3000E1_4000E2_4000_scanning33um.txt"]
rootDirSimu="/home/helga/GRACESimu/ibsimuData/onDetector"
rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan2"
counter=0

for config in listOfFiles:
    legend =TLegend(0.7,0.7,0.90,0.90);
    canvas=TCanvas()
    histodata=fillHistogram(rootDirData+"/"+config+"_data.txt")
    histosimu=fillHistogramSimu(rootDirSimu+"/"+listOfFilesSimu[counter])
    histodata.SetLineColor(1)
    #histodata.SetFillColorAlpha(colorCounter,1)
    legend.AddEntry(histodata,"Data")
    histosimu.GetXaxis().SetTitle("Kinetic energy [keV]")
    histosimu.GetYaxis().SetTitle("normalized frequency")
    histosimu.SetFillColorAlpha(4,0.6)
    histosimu.SetLineColor(4)
    histodata.SetLineWidth(2)
    legend.AddEntry(histosimu,"simulation")
    histosimu.Draw("ehist")
    histodata.Draw("histsame")
    legend.Draw("same")
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/compare"+config+".pdf")
    counter+=1
    print "  "
    print "  "
    print "the config",config
    print "  "
    print "&   "+str(histodata.GetMean())+ " &  "+str(histosimu.GetMean())+ " & "+ str(calculateFWHM(histodata))+  "  &  "+str(calculateFWHM(histosimu))
    print "   "
    print "  "
    print "  "
    print "  "




listOfFiles=[ "D1_0kV_D2_1.5kV_E1_2kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_3kV_E2_3kV","D1_0kV_D2_1.5kV_E1_4kV_E2_3kV"]
listOfFilesSimu=["D1_0D2_1500E1_2000E2_3000_scanning33um.txt","D1_0D2_1500E1_3000E2_3000_scanning33um.txt","D1_0D2_1500E1_4000E2_3000_scanning33um.txt"]
rootDirSimu="/home/helga/GRACESimu/ibsimuData/onDetector"
rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan3"
counter=0

for config in listOfFiles:
    legend =TLegend(0.7,0.7,0.90,0.90);
    canvas=TCanvas()
    histodata=fillHistogram1500(rootDirData+"/"+config+"_data.txt")
    histosimu=fillHistogramSimu1500(rootDirSimu+"/"+listOfFilesSimu[counter])
    histodata.SetLineColor(1)
    #histodata.SetFillColorAlpha(colorCounter,1)
    legend.AddEntry(histodata,"Data")
    histosimu.GetXaxis().SetTitle("Kinetic energy [keV]")
    histosimu.GetYaxis().SetTitle("normalized frequency")
    histosimu.SetFillColorAlpha(4,0.6)
    histosimu.SetLineColor(4)
    histodata.SetLineWidth(2)
    legend.AddEntry(histosimu,"simulation")
    histosimu.Draw("ehist")
    histodata.Draw("histsame")
    legend.Draw("same")
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/compare"+config.replace(".","")+".pdf")
    counter+=1
    print "  "
    print "  "
    print "the config",config
    print "  "
    print "&   "+str(histodata.GetMean())+ " &  "+str(histosimu.GetMean())+ " & "+ str(calculateFWHM(histodata))+  "  &  "+str(calculateFWHM(histosimu))
    print "   "
    print "  "
    print "  "
    print "  "
    #print "simu mean", histosimu.GetMean()
    #print "simu fwhm",calculateFWHM(histosimu)
    #print "data mean", histodata.GetMean()
    #print "data fwhm",calculateFWHM(histodata)





