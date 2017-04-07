import os


volt=["0","1","2","3","4","5"]

#do scan on E1
rootdir="./datafiles"
def findFluxOnSetting(d2,e1,e2):
    print "new setting"
    numberOfShoots=0
    anti=0
    for filename in os.listdir(rootdir):
        if str("D2_"+str(d2)) in filename and str("E1_"+str(e1)) in filename and str("E2_"+str(e2)) in filename and "meta" in filename:
           # print filename
            for line in open(rootdir+"/"+filename,'r'):
                if line.split()[0]=="newFile":
                    numberOfShoots+=1
                if line.split()[0]=="trough":
                    anti+=1                
    return anti*1.0/numberOfShoots

print "scan E1"            
#do the scan on E1
for i in range(6):
    print findFluxOnSetting("3",str(i),"3")

print "scan E2"
#do the scan on E2
for i in range(5):
    print findFluxOnSetting("3","4",str(i))
    
    
