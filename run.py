#!/usr/bin/env python

import os
import sys
import time
import subprocess
import argparse

from machinekit import launcher
from machinekit import rtapi as rt
from machinekit import hal

import base as base_config

os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser(description='EtherCAT test setup run script')
parser.add_argument('-c', '--config', help='Give the name of the EtherCAT configuration to use', action='store')
parser.add_argument('-d', '--demo', help='Demo setup, no EtherCAT', action='store_true')
parser.add_argument('-t', '--testsetup', help='Test setup', action='store_true')

args = parser.parse_args()

try:
    launcher.check_installation()
    launcher.cleanup_session()
    launcher.start_realtime()
    
    rt.init_RTAPI()
    # LOAD ALL THE IMPORTANT STUFF HERE
    base_config.instantiate_threads()
    base_config.instantiate_components(args)

    launcher.register_exit_handler()

    while True:
        launcher.check_processes()
        time.sleep(1)

except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

sys.exit(0)