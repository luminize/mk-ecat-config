#!/usr/bin/env bash

POSITION=$2
JOINT=$1
echo "target position joint $JOINT = $POSITION"
halcmd setp joint${JOINT}_jplan.0.pos-cmd $POSITION