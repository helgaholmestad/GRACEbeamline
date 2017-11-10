#!/bin/bash

function run {
    ./simu 0 $1 $2 $3 inputFiles/Degrader3shoots.txt /slagbjorn/homes/helga/ibsimuData/voltageScan 33um &
}



function runStop {
    echo "stop"
    ./simu 0 $1 $2 $3 inputFiles/Degrader3shoots.txt /slagbjorn/homes/helga/ibsimuData/voltageScan 33um 
}


b=0

k=0
COUNTER1=0
while [  $COUNTER1 -lt 10000 ]; do
    let COUNTER1=COUNTER1+1000
    COUNTER2=-1000
    while [  $COUNTER2 -lt 10000 ]; do
	let COUNTER2=COUNTER2+1000
	COUNTER3=-1000
	while [ $COUNTER3 -lt 10000 ]; do
	    let COUNTER3=COUNTER3+1000
	    let k=k+1
	    if [ "$((k%5))" -eq "$b" ] 
	    then 
		runStop $COUNTER1 $COUNTER2 $COUNTER3
	    else
		run $COUNTER1 $COUNTER2 $COUNTER3
	    fi
	done
    done
done
