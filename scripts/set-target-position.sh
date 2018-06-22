#!/usr/bin/env bash

POSITION=$1
echo "target position = $POSITION"
halcmd setp lcec.0.3.target-position $POSITION