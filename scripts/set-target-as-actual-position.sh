#!/usr/bin/env bash

JOINT=$1
POSITION=$(halcmd getp joint${JOINT}_offset.fb-out)
echo "actual position joint $JOINT = $POSITION"
halcmd setp joint${JOINT}_jplan.0.pos-cmd $POSITION