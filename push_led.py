#!/usr/bin/python3
import struct

import json,sys

import urllib
import requests
requests.packages.urllib3.disable_warnings()

ledbuffer=b""
def setLed(idx,state):
    global ledbuffer
    if state:
        ledbuffer+=b"\x00\xff\x00"
    else:
        ledbuffer+=b"\xff\x00\x00"


def writeLeds():
    print(ledbuffer)
def main(fn):
    with open(fn) as f:
        for ln,l in enumerate(f):
            l = l.strip()
            d = requests.get(l,verify=False).json()
            if 'open' in d:
                o =  d['open']
            elif 'state' in d and 'open' in d['state']:
                o = d['state']['open'] 
            else:
                print("cannot find 'open' for {}".format(l))
                raise
            print(ln,l,o)
            setLed(ln,o)
    writeLeds()


if __name__ == "__main__":
    main("wd.lst")
