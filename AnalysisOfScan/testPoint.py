
from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import re

#this program is to take the output from the ibsimu and filter out the hits  that ended up on the endplate  on the detector.

testpoint=[0.6,0,4.8]
theta=(-40.0/180.0)*np.pi
rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);

point=np.matrix([[testpoint[0]-xtranslateion],[testpoint[1]],[testpoint[2]-ztranslation]])
print point
newPoint=rotation*point
print newPoint
