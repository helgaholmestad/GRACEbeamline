import os
import numpy as np

degraders=["30um","35um","38um","43um"]

#do scan on E1
rootdir="./datafiles"
def findFluxOnSetting(thickness):
    numberOfShoots=0
    antiArray=[]
    anti=0
    for filename in os.listdir(rootdir):
        if thickness in filename and "meta" in filename:
            for line in open(rootdir+"/"+filename,'r'):
                if line.split()[0]=="newFile":
                    antiArray.append(anti)
                    anti=0
                    numberOfShoots+=1
                if line.split()[0]=="trough":
                    anti+=1
    antiArray=np.asarray(antiArray)
    print "number of shoots",numberOfShoots
    return sum(antiArray)*1.0/numberOfShoots,np.std(antiArray)/(numberOfShoots-1)

for t in degraders:
    print " "
    print "thickness",t
    print findFluxOnSetting(t)
    print " "
