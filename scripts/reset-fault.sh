#!/usr/bin/env bash

## state machine control word -> 0
./set-402-stop.sh

## reset fault
halcmd setp lcec.0.3.fault-reset 1
halcmd setp lcec.0.3.fault-reset 0