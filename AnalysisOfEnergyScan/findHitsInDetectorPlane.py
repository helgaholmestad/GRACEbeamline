from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys

#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.

theta=(-40.0/180.0)*np.pi
rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85-0.1*np.cos(np.pi*50.0/180)
xtranslateion=0.1+(0.85-0.1*np.cos(np.pi*50.0/180))/(np.tan(50.0*np.pi/180.0));

file=open("hitsOnDetectorPlane.txt",'w')
def writeHitsOnDetector(filename):
    for line in open(filename,'r'):
        columns=line.split()
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            file.write(line)

for i in range(1,10,1):
    print "working with file","D1_0D2_3000E1_-3000E2_-3000_scanning"+str(i)+"keV.txt"
    writeHitsOnDetector("../scan/D1_0D2_3000E1_-3000E2_-3000_scanning"+str(i)+"keV.txt")
file.close()
