import os
import numpy as np

volt=["0","1","2","3","4","5"]

#do scan on E1
rootdir="./datafiles"
def findFluxOnSetting(d2,e1,e2):
    numberOfShoots=0
    antiArray=[]
    anti=0
    for filename in os.listdir(rootdir):
        if str("D2_"+str(d2)) in filename and str("E1_"+str(e1)) in filename and str("E2_"+str(e2)) in filename and "meta" in filename:
           # print filename
            for line in open(rootdir+"/"+filename,'r'):
                if line.split()[0]=="newFile":
                    antiArray.append(anti)
                    anti=0
                    numberOfShoots+=1
                if line.split()[0]=="trough":
                    anti+=1
    antiArray=np.asarray(antiArray)
    return sum(antiArray)*1.0/numberOfShoots,np.std(antiArray)

print "scan E1"            
#do the scan on E1
for i in range(6):
    print i
    print findFluxOnSetting("3",str(i),"3")

print "scan E2"
#do the scan on E2
for i in range(5):
    print i
    print findFluxOnSetting("3","4",str(i))
    
    
