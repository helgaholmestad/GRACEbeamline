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
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);

histo=TH1D("","",100,-2.0,2.0)

file=open("hitsOnDetectorPlane.txt",'w')
def writeHitsOnDetector(filename):
    hitsOnDetectorPlane=0
    for line in open(filename,'r'):
        columns=line.split()
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            file.write(line)
            hitsOnDetectorPlane+=1
    return hitsOnDetectorPlane

n=writeHitsOnDetector(sys.argv[1])

print "hitsOnDetector",0.34*1.4*1.4*n*1.0/(10*10*np.pi)
file.close()
histo.Draw()
input()
