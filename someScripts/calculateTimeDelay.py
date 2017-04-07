#!/usr/bin/python
import math
import sys

#everything is done in MeV
#lengthOfBeamline=float(sys.argv[2])
c=3*math.pow(10,8)
energyInMeV=float(sys.argv[1])/1000.0
print energyInMeV
massProton=940/(c*c)
v2=2*energyInMeV/massProton
v=math.sqrt(v2)
timeInSeconds=1.48/v
timeInNanoSeconds=timeInSeconds*math.pow(10,9)
print "energy ", energyInMeV*1000, "keV"
print "time delay ", timeInNanoSeconds,"ns"
