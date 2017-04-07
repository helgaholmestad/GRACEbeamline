#!/bin/bash

function run {
    ./simu 0 $1 $2 $3 inputFiles/Degrader33um.txt compareToSimu/datafiles 33um &
}



function runStop {
    echo "stop"
    ./simu 0 $1 $2 $3 inputFiles/Degrader33um.txt compareToSimu/datafiles 33um 
}


b=0

k=0
COUNTER1=0
while [  $COUNTER1 -lt 3000 ]; do
    let COUNTER1=COUNTER1+1500
    COUNTER2=-1000
    while [  $COUNTER2 -lt 5000 ]; do
	let COUNTER2=COUNTER2+1000
	COUNTER3=-1000
	while [ $COUNTER3 -lt 3000 ]; do
	    let COUNTER3=COUNTER3+1000
	    let k=k+1
	    if [ "$((k%10))" -eq "$b" ] 
	    then 
		runStop $COUNTER1 $COUNTER2 $COUNTER3
	    else
	        run $COUNTER1 $COUNTER2 $COUNTER3
	    fi
	done
    done
done
