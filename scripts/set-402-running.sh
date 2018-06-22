#!/usr/bin/env bash

## state machine control word -> 0x0f
halcmd setp lcec.0.3.main-power-on 1
halcmd setp lcec.0.3.quick-stop 1
halcmd setp lcec.0.3.pre-charge-relay-closed 1
halcmd setp lcec.0.3.operation-enabled 1