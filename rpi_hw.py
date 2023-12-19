#!/usr/bin/env python

import logging


def get_board_revision():
    """Extract board revision from cpuinfo file"""
    rev = "0000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:8] == 'Revision':
                length = len(line)
                rev = line[11:length - 1]
        f.close()
    except Exception as e:
        logging.error("caught exception " + str(e))
        rev = "0000"

    return rev


def get_cpu_temperature() -> float:
    """Get the CPU temperature, returns 11.1 in case of failure """
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as fd:
        #with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as fd:
            value = float(fd.read())
            value = round(value / 1000.0, 1)
            return value
    except Exception as e:
        logging.error("caught exception " + str(e))
        return 11.1
