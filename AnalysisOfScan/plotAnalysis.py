from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,TLegend
gROOT.Reset()
import sys
import  numpy as  np

energyHisto=TH1D("","",10,0,10)
theta=TH1D("","",10,0,2*np.pi)
position=TH2D("","",8,-4,4,8,-4,4)
zcomponent=TH1D("","",20,0.94,1)
for line in open("hitsOnDetectorPlane.txt"):
    columns=line.split()
    energyHisto.Fill(float(columns[11]))
    if float(columns[10])==1.0:
        temp_theta=0;
    else:
        temp_theta=np.arccos(float(columns[8])/np.sqrt((float(columns[9])*float(columns[9])+float(columns[8])*float(columns[8]))))
        #calculate the sin value to see if the angle is larger than 180    
        if float(columns[9])/np.sqrt((float(columns[9])*float(columns[9])+float(columns[8])*float(columns[8])))<0:
            temp_theta=np.pi+temp_theta
    theta.Fill(temp_theta)
    position.Fill(float(columns[5])*100,float(columns[6])*100)
    #we have symmetry in the y direction, therefore we can add this
    if float(columns[6])!=0:
             position.Fill(float(columns[5])*100,-float(columns[6])*100)
    zcomponent.Fill(float(columns[10]))
tcanvas=TCanvas()
energyHisto.Draw()

tcanvas1=TCanvas()
theta.Draw()

tcanvas2=TCanvas()
position.Draw("colz")

tcanvas3=TCanvas()
zcomponent.Draw()

input()
