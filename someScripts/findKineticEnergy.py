#from ROOT import TCanvas#, TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis
#gROOT.Reset()
from ROOT import TH1D
print "her"
k=0
a=0
histo=TH1D("","",2000,0,2000)
for line in open("/home/helga/TimepixArticle/code/finalTimepix/fragmentsStudy/exam2001.log"):
#for line in open("exam2001.log"):
    columns = line.split()
    print line
    if len(columns)==0:
        continue
    # if columns[0]=="Kun":
    #     if a==0:
    #         print "no particles"
    #         continue
    #     print "average kinetic energy",k
    #     histo.Fill(k)
    #     k=0
    #if(len(columns)>0 and (columns[0]=="oo" or columns[0]=="-h-")):
    if(len(columns)>0 and columns[0]=="-h-"): 
        a+=1
        print float(columns[2])
        k+=float(columns[2])
print "average kinetic energy",k/a
histo.Draw()
input()
