from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import os.path
import re
import  tagAntiprotons
print "skriv her"
pixelList=[]
distanceT=20.
distanceR=6.1
rootdir="/home/helga/dataFromEinzelLensesScan/"
counter=0
def countNumberForSetting(filepattern,outputfile):
    outputfile.write(filepattern+"\n")
    counter=0
    totalNumberOfAntiprotons=0
    totalNumberOfShoots=0
    for subdir, dirs, files in os.walk(rootdir):
        if not filepattern in subdir:
            continue
        for file in files:
            if os.path.isfile(subdir+"/"+file) and "clustering" in file and ".dat" in file and "test27" in subdir and not "~" in file:
                nameOfFile=str('./fig/testing'+str(counter)+"file")
                title=str(file)
                outputfile.write("new shoot\n")
                try:
                    results=tagAntiprotons.findAntiprotonsInFile(str(subdir+"/"+file), nameOfFile)
                    if results=="noFile":
                        outputfile.write("noFile\n")
                    else:
                        for time  in results:
                            outputfile.write(str(time)+"\n")
                except:
                    print "something went wrong"
                    print  "processing file",subdir+"/"+file
                                    
                    
#listOfFiles=["D1_0kV_D2_3kV_E1_0kV_E2_3kV","D1_0kV_D2_3kV_E1_1kV_E2_3kV", "D1_0kV_D2_3kV_E1_2kV_E2_3kV", "D1_0kV_D2_3kV_E1_3kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_5kV_E2_3kV"]

#listOfFiles=["D1_0kV_D2_1.5kV_E1_0kV_E2_3kV","D1_0kV_D2_1.5kV_E1_1kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_2kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_3kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_4kV_E2_3kV", "D1_0kV_D2_1.5kV_E1_5kV_E2_3kV"]

#listOfFiles=["D1_0kV_D2_3kV_E1_4kV_E2_0kV","D1_0kV_D2_3kV_E1_4kV_E2_1kV", "D1_0kV_D2_3kV_E1_4kV_E2_2kV", "D1_0kV_D2_3kV_E1_4kV_E2_3kV", "D1_0kV_D2_3kV_E1_4kV_E2_4kV", "D1_0kV_D2_3kV_E1_3kV_E2_5kV"]

listOfFiles=["D1_0kV_D2_3kV_E1_4kV_E2_4kV"]

outfilename=open("antiprotons.txt","w")
for pattern in listOfFiles:
    outputfile=open(str(pattern)+"_data.txt",'w')
    countNumberForSetting(pattern,outputfile)
    outputfile.close()
