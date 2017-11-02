from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy as np
import sys
import os
import pp
import time
import matplotlib.pyplot as plt

rootdir="/home/helga/dataFromEinzelLensesScan/"

def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

def make_array(file_date):
    counts={}
    filenames=[]
    for subdir, dirs, files in os.walk(rootdir):
        if "last" in subdir or "notUsed" in subdir:
            continue
        if not file_date in subdir:             
            continue
        for file in files:
            if "data_" in file:
                hits=file_len(subdir+"/"+file)
                if hits<20000:
                    continue
                number=int(file.split("data_")[1].split(".dat")[0])
                counts[number]=hits
    x=[]
    y=[]
    for key, value in counts.iteritems():
        x.append(key)
        y.append(value)
    average=sum(y)/len(y)
    antall =len(y)
    print antall
    return x,y,average

x,y,average=make_array("20160504_33umAl_D1_0kV_D2_3kV_E1_4kV_E2_4kV")

x1,y1,average1=make_array("20160504_33umAl_D1_0kV_D2_3kV_E1_4kV_E2_3kV")

#x2,y2,average2=make_array("20161107_33umAl_0kV_3kV_5kV_3kV_REFLECTION_COLLIM_LSA_GOLD")

#x3,y3,average3=make_array("20161110_33umAl_0kV_3kV_5kV_3kV_REFLECTION_COLLIM_LSA_GOLD")



fig, ax = plt.subplots()   
print "averages",average,average1
ax.set_ylim([15000,65000])
ax.plot(x,y,"ro",markersize=12,label="4000")
ax.plot(x1,y1,"b*",markersize=12,label="3000")
#ax.plot(x2,y2,"gv",markersize=12,label="day3 gold")
#ax.plot(x3,y3,"k<",markersize=12,label="day4 gold")
ax.set_ylabel("total number of hits")
ax.set_xlabel("shot number #")
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')

plt.show()


