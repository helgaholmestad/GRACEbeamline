from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import os.path
import re

histo=TH2D("","",256,0,256,256,0,256)
for line in open("antiprotons.txt","r"):
    x=float(line.split()[0])
    y=float(line.split()[1])
    e=float(line.split()[2])
    histo.Fill(x,y,e)


histo.Draw("colz")
input()
