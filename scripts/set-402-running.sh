#!/usr/bin/env bash

## state machine control word -> 0x0f
JOINT=$1
echo "stopping joint $JOINT, slave lcec.0.$((JOINT - 1))"

halcmd setp lcec.0.$((JOINT - 1)).main-power-on 1
halcmd setp lcec.0.$((JOINT - 1)).quick-stop 1
halcmd setp lcec.0.$((JOINT - 1)).pre-charge-relay-closed 1
halcmd setp lcec.0.$((JOINT - 1)).operation-enabled 1