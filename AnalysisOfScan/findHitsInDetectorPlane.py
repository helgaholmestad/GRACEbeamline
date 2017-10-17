
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

histo=TH1D("","",100,-2.0,2.0)
scatter=TH2D("","",100,-1,1,100,-1,1)

#file=open("hitsOnDetectorPlane.txt",'w')
def findHitOnDetector(filename):
    settings=re.search("voltageScan/(.*).txt",filename)
    #output=open("fig/raw/"+settings.group(1)+".txt",'w')
    output=open("/slagbjorn/homes/helga/ibsimuData/onDetector/"+settings.group(1)+".txt",'w')
    hitsOnDetectorPlane=[]
    for line in open(filename,'r'):
        columns=line.split()
        if float(columns[2])<1.2:
            continue
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            output.write(line)
            histo.Fill(newPoint[0]*100.0,newPoint[1]*100.0)
            
            hitsOnDetectorPlane.append(float(columns[3]))
    hits=np.asarray(hitsOnDetectorPlane)
    return len(hitsOnDetectorPlane), np.mean(hits),np.std(hits)
   

#n=writeHitsOnDetector(sys.argv[1])

#hits, mean,standDev=findHitOnDetector("/slagbjorn/homes/helga/ibsimuData/voltageScan/D1_0D2_3000E1_4000E2_4000_scanning33um.txt")

#print "here"
#input()

number=0
settings=["0","1000","2000","3000","4000","5000","6000","7000","8000","9000","10000"]
settings2=["0","1000","2000","3000","4000","5000","6000","7000","8000"]
file=open("statistics.txt","w")
for i in settings2:
    for k in settings2:
        for j in settings2:
            hits, mean,standDev=findHitOnDetector("/slagbjorn/homes/helga/ibsimuData/voltageScan/D1_0D2_"+i+"E1_"+k+"E2_"+str(j)+"_scanning33um.txt")
            #hits, mean,standDev=findHitsOnDetector("../oldData/D1_0D2_3000E1_-4000E2_-"+str(j)+"_scanning81.txt")
            file.write(str(0)+"  "+i+"  "+k+"  "+j+"  "+str(hits)+"  "+str(mean)+"  "+str(standDev)+"\n") 
            #print findHitsOnDetector("../voltageScan/D1_0D2_"+i+"E1_-"+k+"E2_-"+str(j)+"_scanning33um.txt")
            #print i,k,j
            number+=1
            print number
print "hitsOnDetector",0.44*1.4*1.4*n*1.0/(10*10*np.pi)
file.close()

