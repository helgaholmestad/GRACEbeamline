import numpy as np
import matplotlib.pyplot as plt

fig,ax=plt.subplots()
x=[30,33,35,38,40]

ysimu=[30.79,53.0,33.77,11.1,2.2]

ydata=[3.034,13.42,15.35,0.61,0.0]


yerror=[0.17,0.11,0.14,0.082,0.0]
yerr=np.asarray(yerror)
ax.errorbar(x,ydata,yerr=2.0,fmt='ko',label="testbeamdata",markersize=10,linewidth=4)
ax.plot(x,ysimu,'ro',label="simulated data",markersize=10)
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.80')
plt.xlim(25,45)
plt.ylim(-5,60)
plt.xlabel("Degrader thickness [mu]")
plt.ylabel("Average particles detected per shoot")
plt.savefig("degraderScan.pdf")
