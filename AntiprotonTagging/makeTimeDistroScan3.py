from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,TLegend,gStyle
gROOT.Reset()
import numpy as np
import sys
import os
import os.path
import re

rootdir="/home/helga/dataFromEinzelLensesScan/"
gStyle.SetOptStat("")
def addClusters(filepath):
    listOfAntiprotons=[]
    tmpAntiproton=0
    timeList=[]
    histo=TH1D("","",23,1300,3600)
    numberOfShoot=0
    numberOfAntiProton=0
    print filepath+"_data.txt"
    goodFile=True
    for line in open("scan3"+"/"+filepath+"_data.txt"):
        columns=line.split()
        if columns[0]==filepath:
            continue
        if columns[0]=="new":
            if goodFile:
                numberOfShoot+=1
                listOfAntiprotons.append(tmpAntiproton)
            tmpAntiproton=0
            goodFile=True
            continue
        if columns[0]=="noFile":
            goodFile=False
            continue
        else:
            timeDelay=float(columns[0])
            if timeDelay<3000 and timeDelay>1200:
                histo.Fill(timeDelay)
                timeList.append(timeDelay)
                numberOfAntiProton+=2
                tmpAntiproton+=2
    listOfAntiprotons.append(tmpAntiproton)
    newListOfAntiprotons=[]
    for q in listOfAntiprotons:
        if q<50:
            newListOfAntiprotons.append(q)
    #        numberOfShoot=numberOfShoot-1
    average=sum(newListOfAntiprotons)*1.0/len(newListOfAntiprotons)
    variance=0
    for i in newListOfAntiprotons:
        variance+=(average-i)**2
    histo.Scale(1.0/len(newListOfAntiprotons))
    print "average number of antiprotons",filepath,average,"uncertainty",np.sqrt(variance*1.0/numberOfShoot)
#    print "interval for config",filepath,timeList[int(0.16*len(timeList))],timeList[(int(0.84*len(timeList)))]
    return histo,numberOfAntiProton
#listOfFiles=["D1_0kV_D2_1.5kV_E1_0kV_E2_3kV","D1_0kV_D2_1.5kV_E1_1kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_2kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_3kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_4kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_5kV_E2_3kV"]
listOfFiles=["D1_0kV_D2_1.5kV_E1_2kV_E2_3kV","D1_0kV_D2_1.5kV_E1_3kV_E2_3kV"]
histogramList=[]
cumulativeHistogram=[]
nameList=[]
canvas=TCanvas()
colorCounter=1
# nameList=["D1=0 kV D2= 1.5 kV  E1= 5 kV E2 =3 kV",
#           "D1=0 kV D2= 1.5 kV  E1= 4 kV E2 =3 kV",
#           "D1=0 kV D2= 1.5 kV  E1= 3  kV E2 =3 kV",
#           "D1=0 kV D2= 1.5 kV  E1= 2 kV E2 =3 kV",
#           "D1=0 kV D2= 1.5 kV  E1= 1 kV E2 =3 kV",
#           "D1=0 kV D2= 1.5 kV  E1= 0 kV E2 =3 kV"]


nameList=["D1=0 kV D2= 1.5 kV  E1= 2 kV E2 =3 kV",
          "D1=0 kV D2= 1.5 kV  E1= 3 kV E2 =3 kV"]

for config in listOfFiles:
    histogram=addClusters(config)
    histogram[0].SetLineWidth(5)
    colorCounter=colorCounter+1
    histogramList.append(histogram[0])

    
legend =TLegend(0.55,0.55,0.90,0.90);
counter=0

histogramList[0].GetYaxis().SetRangeUser(0,1.0)
histogramList[0].GetYaxis().SetTitle("Tagged antiprotons per shoot")
histogramList[0].GetXaxis().SetTitle("Time delay [ns]")
histogramList[0].Draw("histsame")
histogramList[0].SetFillColorAlpha(1,0.6)
histogramList[0].SetLineColor(1)
  
legend.AddEntry(histogramList[0],nameList[0])

histogramList[1].GetYaxis().SetRangeUser(0,1.0)
histogramList[1].SetFillColorAlpha(2,0.6)
histogramList[1].SetLineColor(2)
histogramList[1].Draw("histsame")
legend.AddEntry(histogramList[1],nameList[1])

canvas.Update()
legend.Draw("same")
canvas.Print("/home/helga/GRACEReport/fig/scan3RealData.pdf")
