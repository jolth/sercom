#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2016 Jorge Toro <jorge.toro@devmicrosystem.com>
#
# default: 115200,8,N,1
# usage: secom /dev/ttyUSB0
import serial
import sys
import time


def read(ser):
    while ser.isOpen:
        line = ser.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

try:
    port = sys.argv[1]
except IndexError as e:
    print e, ". argument /dev/ttyUSB not existing"
    sys.exit(1)

try:
    ser = serial.Serial(port, 115200, timeout=1)
except serial.serialutil.SerialException as e:
    print e
    sys.exit(1)
 

with ser:
    for line in read(ser):
        print line

