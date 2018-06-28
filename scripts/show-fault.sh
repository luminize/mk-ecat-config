#!/usr/bin/env bash

# see fault and error code
JOINT=$1
echo "fault ? $(halcmd getp lcec.0.$((JOINT - 1)).fault)"
echo "error : $(halcmd getp lcec.0.$((JOINT - 1)).error-code)"