#!/bin/bash  
i=0 
while [ $i -lt 50 ]  
do  
  ((i++))  
  for j in '-' '\\' '|' '/'  
  do  
    echo -ne "$j\033[s"  
    echo -ne "\033[40;50H"$((i*5*100/100))%"\033[u\033[1D"  
    usleep 50000  
  done  
done  
echo 
