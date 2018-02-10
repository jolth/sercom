#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2016 Jorge Toro <jorge.toro@devmicrosystem.com>
#
# default: 115200,8,N,1
# usage: secom /dev/ttyUSB0 [script_file]
# script_file should not have comments or blank lines
#
import time
import sys
import serial


try:
    port = sys.argv[1]
except IndexError as e:
    print("{0}. argument /dev/ttyUSB not existing".format(e))
    sys.exit(1)


def read_Confile(f):
    with open(f, r'rb') as cf:
        for line in cf:
            line = line.replace(b'\r', b'')
            yield line


def write_Confile(ser):
    while ser.isOpen:
        line = (yield)
        time.sleep(1)  # build async
        ser.write(line)


def read(ser):
    while ser.isOpen:
        line = ser.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == '__main__':
    try:
        ser = serial.Serial(port, 115200, timeout=1)
    except serial.serialutil.SerialException as e:
        print(e)
        sys.exit(1)

    if len(sys.argv) > 2:
        write_cf = write_Confile(ser)
        write_cf.__next__()
        read_cf = read_Confile(sys.argv[2])
        for line in read_cf:
            write_cf.send(line)
        print("File is loaded successfully")

    with ser:
        settings = ("{0}:{1}".format(k, v) for k, v in
                    ser.get_settings().items())
        for s in settings:
            print(s, end='\t')
        else:
            print(end='\n\n')
        for line in read(ser):
            print(line.decode(), end='')
            # print(line)
