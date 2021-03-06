from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,TLegend,gStyle
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.
c=299792458.0
massProton=938.0/(c*c)
gStyle.SetOptStat("")
scalingFactor=1.4*1.4/(3*np.pi*100)
print  scalingFactor
def analyseFile(inputfile):
    particles={}
    antiprotons=[]
    timeDelay=TH1D("","",23,1200,2500)
    lineNumber=0
    for line in open(inputfile,'r'):
        columns=line.split()
        print line
        #particles[int(columns[0])]=str(str(columns[12])+"  "+str(columns[8])+"  "+str(columns[6])+"  "+str(columns[7])+"  "+str(columns[11])+"  "+str(columns[9])+"  "+str(columns[10])+"\n")               
        #antiprotons.append(float(columns[0]))
        energyInMeV=float(columns[5])/1000.0
        v2=2*energyInMeV/massProton
        v=math.sqrt(v2)
        timeInSeconds=1.48/v
        timeInNanoSeconds=timeInSeconds*math.pow(10,9)+200+np.random.normal(0,100)
        timeDelay.Fill(timeInNanoSeconds)
        lineNumber=lineNumber+1
    timeDelay.Scale(scalingFactor)
    return timeDelay


listOfHistograms=[]

nameList=["D1=0 kV D2= 3 kV  E1= 4 kV E2 =0 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =1 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =2 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =3 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =4 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =4 kV"]
    
for j in [0,1000,2000,3000,4000,5000]:
                                          #ibsimuData/onDetector/D1_0D2_3000E1_4000E2_0_scanning33um.txt 
    timeDelay=analyseFile("../../ibsimuData/onDetector/D1_0D2_3000E1_4000E2_"+str(j)+"_scanning33um.txt")
    timeDelay.SetLineWidth(5)
    listOfHistograms.append(timeDelay)
    

colorCounter=1
canvas=TCanvas()
legend =TLegend(0.55,0.55,0.90,0.90);
for i in range(5,-1,-1):
    listOfHistograms[i].GetXaxis().SetTitle("Estimated time delay [ns]")
    listOfHistograms[i].GetYaxis().SetTitle("Antiprotons per shoot")
    if i==5:
        listOfHistograms[i].SetFillColorAlpha(colorCounter,0.6)
        listOfHistograms[i].SetLineColor(colorCounter)
        listOfHistograms[i].GetYaxis().SetRangeUser(0,5)
        listOfHistograms[i].Draw("hist")
    else:
        listOfHistograms[i].SetFillColorAlpha(colorCounter,0.6)
        listOfHistograms[i].SetLineColor(colorCounter)
        listOfHistograms[i].Draw("same hist")
    legend.AddEntry(listOfHistograms[i],nameList[i])
    colorCounter=colorCounter+1
    print colorCounter
canvas.Update()
legend.Draw("same")
canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/scanEinzel2Simu.pdf")
