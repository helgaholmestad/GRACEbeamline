from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,TLegend,gStyle
gROOT.Reset()
import numpy as np
import sys
import os
import os.path
import re
import math
gStyle.SetOptStat("")

def fillHistogram(filename):
    numberOfShoots=0
    histo=TH1D("","",26,1200,2500)
    histo.Sumw2()
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new":
            numberOfShoots+=1
            continue
        if columns[0].startswith("D1") or columns[0]=="noFile":
            continue
        histo.Fill(float(columns[0]))
    histo.Scale(1.0/histo.Integral())
    return histo



def fillHistogram1500(filename):
    numberOfShoots=0
    histo=TH1D("","",30,1300,3300)
    histo.Sumw2()
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new":
            numberOfShoots+=1
            continue
        if columns[0].startswith("D1") or columns[0]=="noFile":
            continue
        histo.Fill(float(columns[0]))
    histo.Scale(1.0/histo.Integral())
    return histo



def fillHistogramSimu1500(filename):
    c=299792458.0
    massProton=938.0/(c*c)
    histo=TH1D("","",30,1300,3300)
    for line in open(filename):
        columns=line.split()
        energyInMeV=float(columns[6])/1000.0
        v2=2*energyInMeV/massProton
        v=math.sqrt(v2)
        timeInSeconds=1.48/v
        timeInNanoSeconds=timeInSeconds*math.pow(10,9)+np.random.normal(0,100)
        histo.Fill(timeInNanoSeconds)
    histo.Scale(1.0/histo.Integral())
    return histo





def fillHistogramSimu(filename):
    c=299792458.0
    massProton=938.0/(c*c)
    histo=TH1D("","",26,1200,2500)
    for line in open(filename):
        columns=line.split()
        energyInMeV=float(columns[6])/1000.0
        v2=2*energyInMeV/massProton
        v=math.sqrt(v2)
        timeInSeconds=1.48/v
        timeInNanoSeconds=timeInSeconds*math.pow(10,9)+200+np.random.normal(0,100)
        histo.Fill(timeInNanoSeconds)
    histo.Scale(1.0/histo.Integral())
    return histo



def calculateFWHM(histo):
    lowerBin=histo.FindFirstBinAbove(histo.GetMaximum()/2);
    upperBin=histo.FindLastBinAbove(histo.GetMaximum()/2)
    fwhm = histo.GetBinCenter(upperBin) - histo.GetBinCenter(lowerBin);
    return fwhm



listOfFiles=[ "D1_0kV_D2_3kV_E1_3kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_5kV_E2_3kV"]
listOfFilesSimu=["D1_0D2_3000E1_3000E2_3000_scanning33um.txt","D1_0D2_3000E1_4000E2_3000_scanning33um.txt","D1_0D2_3000E1_5000E2_3000_scanning33um.txt"]
rootDirSimu="/home/helga/GRACESimu/ibsimuData/onDetector"
rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan1"
counter=0
scalingFactor=2*1.4*1.4/(np.pi*10)

for config in listOfFiles:
    legend =TLegend(0.7,0.7,0.90,0.90);
    canvas=TCanvas()
    histodata=fillHistogram(rootDirData+"/"+config+"_data.txt")
    histosimu=fillHistogramSimu(rootDirSimu+"/"+listOfFilesSimu[counter])
    histodata.SetLineColor(1)
    #histodata.SetFillColorAlpha(colorCounter,1)
    legend.AddEntry(histodata,"Data")
    histodata.GetXaxis().SetTitle("time delay")
    histodata.GetYaxis().SetTitle("normalized frequency")
    histosimu.SetFillColorAlpha(4,0.6)
    histosimu.SetLineColor(4)
    histodata.SetLineWidth(2)
    legend.AddEntry(histosimu,"simulation")
    histosimu.Draw()
    histodata.Draw("ehistsame")
    legend.Draw("same")
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/compare"+config+".pdf")
    counter+=1
    print config
    print "simu mean", histosimu.GetMean()
    print "simu fwhm",calculateFWHM(histosimu)
    print "data mean", histodata.GetMean()
    print "data fwhm",calculateFWHM(histodata)

    
listOfFiles=[ "D1_0kV_D2_3kV_E1_4kV_E2_2kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_4kV"]
listOfFilesSimu=["D1_0D2_3000E1_4000E2_2000_scanning33um.txt","D1_0D2_3000E1_4000E2_3000_scanning33um.txt","D1_0D2_3000E1_4000E2_4000_scanning33um.txt"]
rootDirSimu="/home/helga/GRACESimu/ibsimuData/onDetector"
rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan2"
counter=0
scalingFactor=2*1.4*1.4/(np.pi*10)

for config in listOfFiles:
    legend =TLegend(0.7,0.7,0.90,0.90);
    canvas=TCanvas()
    histodata=fillHistogram1500(rootDirData+"/"+config+"_data.txt")
    histosimu=fillHistogramSimu1500(rootDirSimu+"/"+listOfFilesSimu[counter])
    histodata.SetLineColor(1)
    #histodata.SetFillColorAlpha(colorCounter,1)
    legend.AddEntry(histodata,"Data")
    histodata.GetXaxis().SetTitle("time delay")
    histodata.GetYaxis().SetTitle("normalized frequency")
    histosimu.SetFillColorAlpha(4,0.6)
    histosimu.SetLineColor(4)
    histodata.SetLineWidth(2)
    legend.AddEntry(histosimu,"simulation")
    histodata.Draw("ehist")
    histosimu.Draw("same")
    legend.Draw("same")
    canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/compare"+config+".pdf")
    counter+=1
    print config
    print "simu mean", histosimu.GetMean()
    print "simu fwhm",calculateFWHM(histosimu)
    print "data mean", histodata.GetMean()
    print "data fwhm",calculateFWHM(histodata)



# listOfFiles=[ "D1_0kV_D2_1.5kV_E1_2kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_3kV_E2_3kV"]
# listOfFilesSimu=["configs_D1_0D2_1500E1_2000E2_3000_scanning33um.txt","configs_D1_0D2_1500E1_3000E2_3000_scanning33um.txt"]
# rootDirSimu="/home/helga/GRACESimu/IbsimuData/onDetector"
# rootDirData="/home/helga/GRACESimu/GRACEbeamline/AntiprotonTagging/scan3"
# counter=0
# scalingFactor=2*1.4*1.4/(np.pi*10)

# for config in listOfFiles:
#     legend =TLegend(0.7,0.7,0.90,0.90);
#     canvas=TCanvas()
#     histodata=fillHistogram1500(rootDirData+"/"+config+"_data.txt")
#     histosimu=fillHistogramSimu1500(rootDirSimu+"/"+listOfFilesSimu[counter])
#     histodata.SetLineColor(1)
#     #histodata.SetFillColorAlpha(colorCounter,1)
#     legend.AddEntry(histodata,"Data")
#     histodata.GetXaxis().SetTitle("time delay")
#     histodata.GetYaxis().SetTitle("normalized frequency")
#     histosimu.SetFillColorAlpha(4,0.6)
#     histosimu.SetLineColor(4)
#     histodata.SetLineWidth(2)
#     legend.AddEntry(histosimu,"simulation")
#     histodata.Draw("ehist")
#     histosimu.Draw("same")
#     legend.Draw("same")
#     canvas.Print("/home/helga/gitThesis/thesis/fig/compare"+config+".pdf")
#     counter+=1
#     print config
#     print "simu mean", histosimu.GetMean()
#     print "simu fwhm",calculateFWHM(histosimu)
#     print "data mean", histodata.GetMean()
#     print "data fwhm",calculateFWHM(histodata)





