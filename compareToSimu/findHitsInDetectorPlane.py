
from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import re

#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.

theta=(-40.0/180.0)*np.pi
rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);

#histo=TH1D("","",100,-10.0,10.0)
histo=TH2D("","",100,0,10,100,-0.2,0.2)
scatter=TH2D("","",29,-0.2,0.2,29,-0.2,0.2)
#file=open("hitsOnDetectorPlane.txt",'w')
def findHitsOnDetector(filename):
    onDetector=0
    print filename.split("/")
    output=open("./resultfiles/onDetector"+filename.split("/")[1],'w')
    hitsOnDetectorPlane=[]
    for line in open(filename,'r'):
        columns=line.split()
        xshift=0.03
        yshift=0.00
        energy=float(columns[3])
        #if energy<6.0:
        #    continue
        if float(columns[2])<1.2:
            continue
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            output.write(line)
            columns=line.split()
            if abs(newPoint[0]-xshift)<0.007 and abs(newPoint[1]-yshift)<0.007:
                onDetector+=1
            histo.Fill(energy,newPoint[0])
            scatter.Fill(newPoint[0],newPoint[1])
            hitsOnDetectorPlane.append(float(columns[3]))
    hits=np.asarray(hitsOnDetectorPlane)
    return len(hitsOnDetectorPlane), np.mean(hits),np.std(hits),onDetector
   
#n=writeHitsOnDetector(sys.argv[1])

#hits, mean,standDev,onDetector=findHitsOnDetector("D1_0D2_"+i+"E1_"+j+"E2_"+k+"_scanning33um.txt")
#hits, mean,standDev,onDetector=findHitsOnDetector(sys.argv[1])


settings=["0","1000","2000","3000","4000","5000"]
# settings2=["3000","4000","5000"]
# file=open("statistics.txt","w")
#scan 1
for i in settings:
    hits, mean,standDev,onDetector=findHitsOnDetector("datafiles/D1_0D2_3000E1_"+i+"E2_3000_scanning33um.txt")
    print hits*1.4*1.4/(np.pi*100),onDetector*0.5
for i in settings:
    hits, mean,standDev,onDetector=findHitsOnDetector("datafiles/D1_0D2_3000E1_4000E2_"+str(i)+"_scanning33um.txt")
    print hits*1.4*1.4/(np.pi*100),onDetector*0.5


