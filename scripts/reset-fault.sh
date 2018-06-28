#!/usr/bin/env bash

## state machine control word -> 0
JOINT=$1
./set-402-stop.sh ${JOINT}

## reset fault
halcmd setp lcec.0.$((JOINT - 1)).fault-reset 1
halcmd setp lcec.0.$((JOINT - 1)).fault-reset 0