from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import re
import os
import pp
import time

#on raptor
path="/slagbjorn/homes/helga/"
#on laptop
#path="/home/helga/GRACESimu/" 
#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.

theta=(-40.0/180.0)*np.pi
rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.75*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.75*np.sin(40.0*np.pi/180.0);

def findHitsOnDetector(filename,output):
    import re
    import numpy as np
    theta=(-40.0/180.0)*np.pi
    rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
    ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.75*np.cos(np.pi*40.0/180)
    xtranslateion=0.1+0.75*np.sin(40.0*np.pi/180.0);
    print "processing file",filename
    if os.path.isfile(filename)==False:
        print("not found",filename)
        return
    output=open(output, t'w')
    hitsOnDetectorPlane=[]
    for line in open(filename,'r'):
        columns=line.split()
        if float(columns[2])<1.2:
            continue
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            output.write(line)  
            
if __name__ == '__main__':
    findHitsOnDetector(sys.argv[1],sys.argv[2])
