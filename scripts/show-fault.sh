#!/usr/bin/env bash

# see fault and error code
JOINT=$1
echo "Check if lcec.0.$((JOINT - 1)).fault: $(halcmd getp lcec.0.$((JOINT - 1)).fault)"
echo "The error code is      : $(halcmd getp lcec.0.$((JOINT - 1)).error-code)"