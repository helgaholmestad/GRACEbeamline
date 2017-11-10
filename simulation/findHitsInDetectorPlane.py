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
ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);

def findHitOnDetector(filename):
    path="/slagbjorn/homes/helga/"
    import re
    import numpy as np
    theta=(-40.0/180.0)*np.pi
    rotation=np.matrix([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])
    ztranslation=0.5+0.1/np.sin(40.0/180*np.pi)+0.85*np.cos(np.pi*40.0/180)
    xtranslateion=0.1+0.85*np.sin(40.0*np.pi/180.0);
    print "processing file",filename
    if os.path.isfile(filename)==False:
        print("not found",filename)
        return
    settings=re.search("voltageScan/(.*).txt",filename)
    output=open(path+"ibsimuData/onDetector/"+settings.group(1)+".txt",'w')
    hitsOnDetectorPlane=[]
    for line in open(filename,'r'):
        columns=line.split()
        if float(columns[2])<1.2:
            continue
        point=np.matrix([[float(columns[0])-xtranslateion],[float(columns[1])],[float(columns[2])-ztranslation]])
        newPoint=rotation*point
        if  abs(newPoint[0])*abs(newPoint[0])+abs(newPoint[1])*abs(newPoint[1])<0.1*0.1 and abs(newPoint[2])<0.016:
            output.write(line)  
            
settings=["0","1000","2000","3000","4000","5000","6000","7000","8000","9000","10000"]

theFiles=[]

for i in settings:
    for k in settings:
        for j in settings:
            theFiles.append(str(path+"ibsimuData/voltageScan/D1_0D2_"+i+"E1_"+k+"E2_"+str(j)+"_scanning33um.txt"))

ppservers = ()

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

ppservers = ()

start_time = time.time()

jobs=[]
#run the clustering in paralell
for k in range(len(theFiles)):
    jobs.append(job_server.submit(findHitOnDetector,(theFiles[k],)))

# #jobs = [(input, job_server.submit(sum_primes,(input,), (isprime,), ("math",))) for input in inputs]
teller=0
for job in jobs:
    print "teller ", teller
    teller=teller+1
    print "er vi her"
    job()


# settings=["0","1000","2000","3000","4000","5000"]            
# for i in settings:
#     for k in settings:
#         findHitOnDetector(path+"ibsimuData/voltageScan/D1_0D2_1500E1_"+k+"E2_"+str(i)+"_scanning33um.txt")
