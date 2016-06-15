#!/bin/bash 
#to loop over different inputfiles.  
COUNTER1=0
while [  $COUNTER1 -lt 10 ]; do
    let COUNTER1=COUNTER1+1
    echo $COUNTER1
    ./simu 0 3000 -3000 -3000 Analysis/scanAt$COUNTER1.txt $COUNTER1
done

