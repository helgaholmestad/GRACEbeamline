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
    meanx=0.0
    meany=0.0
    x2=0.0
    y2=0.0
    for line in open(filename,'r'):
        columns=line.split()
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        x,y,z=float(newPoint[0]),float(newPoint[1]),float(newPoint[2])
        xshift=0.03
        yshift=0.00
        energy=float(columns[3])
        if  abs(x)*abs(x)+abs(y)*abs(y)<0.1*0.1 and abs(z)<0.016:
            histo.Fill(newPoint[0],newPoint[1])
            meanx=meanx+x
            meany=meany+y
            x2=x2+x*x
            y2=y2+y*y
        hitsOnDetectorPlane.append(float(columns[3]))
    tcanvas=TCanvas()
    histo.Draw("colz")    
    tcanvas.Print(plotFile)
    hits=len(hitsOnDetectorPlane)
    return hits,1.0*meanx/hits,1.0*meany/hits,x2*1.0/hits,y2*1.0/hits
   

settings=["0","1000","2000","3000","4000","5000"]

#scan 1
print "Scan of first einzel"
for i in settings:
    print "  "
    print "hvilken setting",i
    hits, meanx,meany,x2,y2=findHitsOnDetector("../../ibsimuData/onDetector/D1_0D2_3000E1_"+i+"E2_3000_scanning33um.txt","/home/helga/gitThesis/thesis/Grace/fig/E1_V_"+i+".pdf")
    print "average hits",hits*1.4*1.4/(np.pi*10)
    print "mean x and y",meanx,meany
    print "spread x and y",x2,y2
    print "  "
print "Scan on second einzel"
for i in settings:
    print "  "
    print "hvilken setting",i
    hits, meanx,meany,x2,y2,=findHitsOnDetector("../../ibsimuData/onDetector/D1_0D2_3000E1_4000E2_"+str(i)+"_scanning33um.txt","/home/helga/gitThesis/thesis/Grace/fig/E2_V_"+i+".pdf")
    print "average hits",hits*1.4*1.4/(np.pi*10)
    print "mean x and y",meanx,meany
    print "spread x and y",x2,y2
    print "  "
