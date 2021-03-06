#!/usr/bin/python3
import struct,time

import json,sys

import asyncio
from aiocoap import *

import urllib
import requests
requests.packages.urllib3.disable_warnings()

ledbuffer=b''
host="10.42.25.253"
setled_path="/v1/f/setLeds"
max_led=78
def customLed(idx,color_data):
    global ledbuffer
    ledbuffer+=color_data

def setLed(idx,state):
    global ledbuffer
    idx = idx+1
    print(state)
    ledbuffer=b"\x00\x00\x00"*idx 
    if state:
        print('true')
        ledbuffer+=b"\x00\x25\x00"
    else:
        ledbuffer+=b"\x25\x00\x00"
    ledbuffer+=b"\x00\x00\x00"*(max_led-idx)

@asyncio.coroutine
def writeLeds():
    protocol = yield from Context.create_client_context()
    request = Message(code=POST,payload=ledbuffer)
    request.set_request_uri('coap://{}{}'.format(host,setled_path))

    try:
        response = yield from protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('wrote leds: {}'.format(ledbuffer))
        #print('Result: %s\n%r'%(response.code, response.payload))
        pass

def main(fn):
    with open(fn) as f:
        for ln,l in enumerate(f):
            l = l.strip()
            time.sleep(1)
            if not l:
                # fallback when hackerspace api is broken
                customLed(idx,b'\x25\x00\x25')
                continue
            d = requests.get(l,verify=False).json()
            if 'open' in d:
                o =  d['open']
            elif 'state' in d and 'open' in d['state']:
                o = d['state']['open'] 
            else:
                print("cannot find 'open' for {}".format(l))
            
            setLed(ln,o)
            asyncio.get_event_loop().run_until_complete(writeLeds())


if __name__ == "__main__":
    main("wd.lst")
    
