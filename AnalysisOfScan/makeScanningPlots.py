from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import matplotlib.pyplot as plt
import operator

#energy vs bending
#find the focusing that has the highest flux.
#array of the bending and the energy.
bendingArray=[0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
highestFlux=0
energy=[0]*11
errorEnergy=[0]*11
#bending vs flux
fluxArray=[0]*11
f1Array=[0]*11
f2Array=[0]*11
bendingArray=[0]*11

#energy vs focus

#flux vs energi

#find correlation between scattering (z-component) and energy

bending=0
index=0
for line in open("statistics.txt"):
    b1,b2,f1,f2,flux,mean,standDev=line.split()
    b1,b2,f1,f2,flux,mean,standDev=int(b1),int(b2),int(f1),int(f2),int(flux),float(mean),float(standDev)
    if flux>highestFlux:
        highestFlux=flux
        fluxArray[index]=flux
        energy[index]=mean
        errorEnergy[index]=standDev
        f1Array[index]=f1
        f2Array[index]=f2
        bendingArray[index]=bending
    if b2>bending:
        bending+=1000
        highestFlux=0
        index+=1

#print energy
#print fluxArray
#print errorEnergy

#here a dictornary with key bending voltage and value maximum flux is made
dictMaxFlux={}
for i in range(len(energy)):
    #print "bending",bendingArray[i],"energy",energy[i],"+-",errorEnergy[i],"focusing1",f1Array[i],"focusing2",f2Array[i]
    dictMaxFlux[bendingArray[i]]=(f1Array[i],f2Array[i])

#plt.plot(bendingArray,fluxArray,'*')
#plt.show()
#plt.errorbar(bendingArray,energy,errorEnergy,fmt='o')
#plt.show()

#scan focusing on the first focusing lenses

def findEnergy(bending,focus1,focus2):
    for line in open("statistics.txt"):
        b1,b2,f1,f2,flux,mean,standDev=line.split()
        b1,b2,f1,f2,flux,mean,standDev=int(b1),int(b2),int(f1),int(f2),int(flux),float(mean),float(standDev)
        if b2==bending and f1==focus1 and f2==focus2:
            return mean,standDev
        
def findFlux(bending,focus1,focus2):
    for line in open("statistics.txt"):
        b1,b2,f1,f2,flux,mean,standDev=line.split()
        b1,b2,f1,f2,flux,mean,standDev=int(b1),int(b2),int(f1),int(f2),int(flux),float(mean),float(standDev)
        if b2==bending and f1==focus1 and f2==focus2:
            print "her"
            return flux
        

plotBending=[0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
#plotBending=[1000,2000,4000,6000,8000,10000]
dictEnergy={}
dictFlux={}
dictEnergyError={}
for bending in plotBending:
    dictEnergy[bending]=[]
    dictFlux[bending]=[]
    for focus in plotBending:
        #print bending,focus,dictMaxFlux[bending][1],findEnergy(bending,focus,dictMaxFlux[bending][1])
        dictEnergy[bending].append(findEnergy(bending,focus,dictMaxFlux[bending][1]))
        dictFlux[bending].append(findFlux(bending,focus,dictMaxFlux[bending][1]))
        
    
for i in plotBending:
    energy = map(operator.itemgetter(0), dictEnergy[i])
    plt.plot(plotBending,energy)
plt.savefig("../fig/energyScan1.png")

plt.clf()
for i in plotBending:
    flux = dictFlux[i]
    print flux
    plt.plot(plotBending,flux)
plt.savefig("../fig/fluxScan1.png")








#repeat everything now with the focusing on the other lenses
plotBending=[0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
#plotBending=[1000,2000,4000,6000,8000,10000]
dictEnergy={}
dictFlux={}
dictEnergyError={}
for bending in plotBending:
    dictEnergy[bending]=[]
    dictFlux[bending]=[]
    for focus in plotBending:
        #print bending,focus,dictMaxFlux[bending][1],findEnergy(bending,focus,dictMaxFlux[bending][1])
        dictEnergy[bending].append(findEnergy(bending,dictMaxFlux[bending][0],focus))
        dictFlux[bending].append(findFlux(bending,dictMaxFlux[bending][0],focus))
plt.clf()    
for i in plotBending:
    energy = map(operator.itemgetter(0), dictEnergy[i])
    plt.plot(plotBending,energy)
plt.savefig("../fig/energyScan2.png")

plt.clf()
for i in plotBending:
    flux = dictFlux[i]
    print flux
    plt.plot(plotBending,flux)
plt.savefig("../fig/fluxScan2.png")
