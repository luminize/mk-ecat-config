#!/usr/bin/env bash

POSITION=$1
echo "target position = $POSITION"
halcmd setp joint6_offset.in $POSITION