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
scalingFactor=1.4*1.4/(np.pi*10)
print  scalingFactor
def analyseFile(inputfile):
    particles={}
    antiprotons=[]
    timeDelay=TH1D("","",23,1000,3300)
    lineNumber=0
    for line in open(inputfile,'r'):
        columns=line.split()
        #particles[int(columns[0])]=str(str(columns[12])+"  "+str(columns[8])+"  "+str(columns[6])+"  "+str(columns[7])+"  "+str(columns[11])+"  "+str(columns[9])+"  "+str(columns[10])+"\n")               
        #antiprotons.append(float(columns[0]))
        energyInMeV=float(columns[6])/1000.0
        v2=2*energyInMeV/massProton
        v=math.sqrt(v2)
        timeInSeconds=1.48/v
        timeInNanoSeconds=timeInSeconds*math.pow(10,9)+200+np.random.normal(0,100)
        timeDelay.Fill(timeInNanoSeconds)
        lineNumber=lineNumber+1
    timeDelay.Scale(scalingFactor)
    return timeDelay


listOfHistograms=[]

nameList=["D1=0 kV D2= 1.5 kV  E1= 2 kV E2 =3 kV",
          "D1=0 kV D2= 1.5 kV  E1= 3 kV E2 =3 kV"]
    
for j in [2000,3000]:
    timeDelay=analyseFile("configs_D1_0D2_1500E1_"+str(j)+"E2_3000_scanning81um.txt")
    timeDelay.SetLineWidth(5)
    listOfHistograms.append(timeDelay)
    


canvas=TCanvas()
legend =TLegend(0.55,0.55,0.90,0.90);

listOfHistograms[0].GetXaxis().SetTitle("Estimated time delay [ns]")
listOfHistograms[0].GetYaxis().SetTitle("Antiprotons per shoot")
listOfHistograms[0].SetFillColorAlpha(1,0.6)
listOfHistograms[0].SetLineColor(1)
listOfHistograms[0].GetYaxis().SetRangeUser(0,15)
listOfHistograms[0].Draw()
listOfHistograms[1].SetFillColorAlpha(2,0.6)
listOfHistograms[1].SetLineColor(2)
listOfHistograms[1].Draw("same")
legend.AddEntry(listOfHistograms[0],nameList[0])
legend.AddEntry(listOfHistograms[1],nameList[1])


# colorCounter=1
# canvas=TCanvas()
# legend =TLegend(0.55,0.55,0.90,0.90);
# for i in range(5,-1,-1):
#     listOfHistograms[i].GetXaxis().SetTitle("Estimated time delay [ns]")
#     listOfHistograms[i].GetYaxis().SetTitle("Clusters abow 30 pixels per shoot")
#     if i==5:
#         listOfHistograms[i].SetFillColorAlpha(colorCounter,0.6)
#         listOfHistograms[i].SetLineColor(colorCounter)
#         listOfHistograms[i].GetYaxis().SetRangeUser(0,15)
#         listOfHistograms[i].Draw()
#     else:
#         listOfHistograms[i].SetFillColorAlpha(colorCounter,0.6)
#         listOfHistograms[i].SetLineColor(colorCounter)
#         listOfHistograms[i].Draw("same")
#     legend.AddEntry(listOfHistograms[i],nameList[i])
#     colorCounter=colorCounter+1
#     print colorCounter
canvas.Update()
legend.Draw("same")
canvas.Print("/home/helga/GRACEReport/fig/scanEinzel1Scan3Simu.pdf")
