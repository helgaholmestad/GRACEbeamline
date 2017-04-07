import numpy as np
import sys


z=float(sys.argv[1])
print np.power(10.0,-3)
e=np.power(10.0,-6)*1.0*np.pi
b=0.5+z*z/0.5
print e,b
sigma=np.sqrt(b*e)
print sigma*100
