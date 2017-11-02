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
    histo=TH1D("","",23,1200,2500)
    numberOfShoot=0
    numberOfAntiProton=0
    print filepath+"_data.txt"
    goodFile=True
    for line in open("../AntiprotonTagging/scan1"+"/"+filepath+"_data.txt"):
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
            histo.Fill(float(columns[0]))
            timeList.append(columns[0])
            numberOfAntiProton+=2
            tmpAntiproton+=2
    listOfAntiprotons.append(tmpAntiproton)
    newListOfAntiprotons=[]
    for q in listOfAntiprotons:
        if q<80 and q!=0:
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
listOfFiles=["D1_0kV_D2_3kV_E1_0kV_E2_3kV","D1_0kV_D2_3kV_E1_1kV_E2_3kV", "D1_0kV_D2_3kV_E1_2kV_E2_3kV", "D1_0kV_D2_3kV_E1_3kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_5kV_E2_3kV"]
#listOfFiles=["D1_0kV_D2_3kV_E1_3kV_E2_3kV"]
histogramList=[]
cumulativeHistogram=[]
nameList=[]
canvas=TCanvas()
colorCounter=1
nameList=["D1=0 kV D2= 3 kV  E1= 5 kV E2 =3 kV",
          "D1=0 kV D2= 3 kV  E1= 4 kV E2 =3 kV",
          "D1=0 kV D2= 3 kV  E1= 3  kV E2 =3 kV",
           "D1=0 kV D2= 3 kV  E1= 2 kV E2 =3 kV",
          "D1=0 kV D2= 3 kV  E1= 1 kV E2 =3 kV",
          "D1=0 kV D2= 3 kV  E1= 0 kV E2 =3 kV"]

for config in reversed(listOfFiles):
    histogram=addClusters(config)
    histogram[0].SetFillColorAlpha(colorCounter,0.6)
    histogram[0].SetLineColor(colorCounter)
    histogram[0].SetLineWidth(5)
    colorCounter=colorCounter+1
    histogramList.append(histogram[0])
    nameList.append(config)
        
legend =TLegend(0.55,0.55,0.90,0.90);
counter=0
for histogram in histogramList:
    if histogram==histogramList[0]:
        histogram.GetYaxis().SetRangeUser(0,5)
        histogram.GetYaxis().SetTitle("Tagged antiprotons per shoot")
        histogram.GetXaxis().SetTitle("Time delay [ns]")
        histogram.Draw("histsame")        
    else:
        histogram.Draw("histsame")
    legend.AddEntry(histogram,nameList[counter])
    counter=counter+1

canvas.Update()
legend.Draw("same")
canvas.Print("/home/helga/gitThesis/thesis/Grace/fig/scan1RealData.pdf")
