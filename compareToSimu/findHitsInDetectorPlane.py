from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import re

histo=TH2D("","",100,-0.1,0.1,100,-0.1,0.1)

#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.

theta=(-40.0/180.0)*np.pi
rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);

def findHitsOnDetector(filename,plotFile):
    histo=TH2D("","",100,-0.1,0.1,100,-0.1,0.1)
    hitsOnDetectorPlane=[]
    onDetector=0
    for line in open(filename,'r'):
        columns=line.split()
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        xshift=0.03
        yshift=0.00
        energy=float(columns[3])
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            histo.Fill(newPoint[0],newPoint[1])
        #scatter.Fill(newPoint[0],newPoint[1])
        hitsOnDetectorPlane.append(float(columns[3]))
    tcanvas=TCanvas()
    histo.Draw("colz")    
    tcanvas.Print(plotFile)
    hits=np.asarray(hitsOnDetectorPlane)
    return len(hitsOnDetectorPlane), np.mean(hits),np.std(hits),onDetector
   

settings=["0","1000","2000","3000","4000","5000"]

#scan 1
for i in settings:
    hits, mean,standDev,onDetector=findHitsOnDetector("../../ibsimuData/onDetector/D1_0D2_3000E1_"+i+"E2_3000_scanning33um.txt","/home/helga/gitThesis/thesis/Grace/fig/D1_0D2_3000E1_"+i+"E2_3000Endplate.pdf")
    print hits*1.4*1.4/(np.pi*10),onDetector*0.45
print "new settings"
for i in settings:
    hits, mean,standDev,onDetector=findHitsOnDetector("../../ibsimuData/onDetector/D1_0D2_3000E1_4000E2_"+str(i)+"_scanning33um.txt","/home/helga/gitThesis/thesis/Grace/fig/D1_0D2_3000E1_4000E2_"+i+".pdf")
    print hits*1.4*1.4/(np.pi*10),onDetector*0.45
