#!/usr/bin/env bash

# see fault and error code
echo "fault ? $(halcmd getp lcec.0.3.fault)"
echo "error : $(halcmd getp lcec.0.3.error-code)"