from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,TLegend
gROOT.Reset()
import sys
import  numpy as  np

#This program is used to make inputfiles in oder  to scan over different initial states of the beam

def makeFile(energy):
    outputfiel=open("scanAt"+str(energy)+".txt",'w')
    for  x  in np.linspace(-4,4.0,20):#input  x position
        for y in np.linspace(-4,4,20):#input y position
            if y>0:
                continue
            for i in np.linspace(0.95,1.0,50,endpoint=True):# z componenten of  the momentum direction vector
                for theta in np.linspace(0,2*np.pi,50):#  scan over all angels 
                    outputfiel.write(str(energy)+"  "+str(0)+" "+str(x)+"  "+str(y)+"  "+str(i)+"  "+str(np.sqrt(1-i*i)*np.cos(theta))+"  "+str(np.sqrt(1-i*i)*np.sin(theta))+"\n")

for i in range(11):
    makeFile(i)




