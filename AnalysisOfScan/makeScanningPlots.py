from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import matplotlib.colors as colors
import numpy as np
import matplotlib
import math
import sys
import matplotlib.pyplot as plt

#energy vs bending
#find the focusing that has the highest flux.
#array of the bending and the energy.
bendingArray=[0,1000,2000,3000,4000,5000]
highestFlux=0
energy=[0]*6
errorEnergy=[0]*6
#bending vs flux
fluxArray=[0]*6


#energy vs focus

#flux vs energi

#find correlation between scattering (z-component) and energy

bending=0
index=0
for line in open("statistics.txt"):
    b1,b2,f1,f2,flux,mean,standDev=line.split()
    b1,b2,f1,f2,flux,mean,standDev=int(b1),int(b2),int(f1),int(f2),int(flux),float(mean),float(standDev)
    print line
    if flux>highestFlux:
        print "found highest"
        highestFlux=flux
        fluxArray[index]=flux
        energy[index]=mean
        errorEnergy[index]=standDev
    if b2>bending:
        bending+=1000
        highestFlux=0
        index+=1


print energy
print fluxArray
print errorEnergy


plt.plot(bendingArray,fluxArray,'*')
plt.show()
plt.errorbar(bendingArray,energy,errorEnergy,fmt='o')
plt.show()
