import numpy as np
import sys
e=1.6*pow(10.0,-19)
particles=pow(10.0,5)
totalCharge=e*particles

r=0.01
k=9*pow(10,9)
eField=totalCharge*k/(r*r)

print eField
