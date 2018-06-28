#!/usr/bin/env bash

# see position values
JOINT=$1
clear
halcmd show pin lcec.0.$((JOINT - 1))*position*
halcmd show pin joint${JOINT}_offset
halcmd show pin joint${JOINT}_jplan