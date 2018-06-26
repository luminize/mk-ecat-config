#!/usr/bin/env bash

## state machine control word -> 0
halcmd setp lcec.0.3.operation-enabled 0
halcmd setp lcec.0.3.pre-charge-relay-closed 0
halcmd setp lcec.0.3.quick-stop 0
halcmd setp lcec.0.3.main-power-on 0