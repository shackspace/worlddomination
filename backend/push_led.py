#!/usr/bin/python3
import struct

import json,sys

import asyncio
from aiocoap import *

import urllib
import requests
requests.packages.urllib3.disable_warnings()

ledbuffer=b'\x00\x00\x00'
#ledbuffer+= b'\x00\x00\x00'*40
host="esp8266"
setled_path="/v1/f/setLeds"

def customLed(idx,color_data):
    global ledbuffer
    ledbuffer+=color_data

def setLed(idx,state):
    global ledbuffer
    print(state)

    if state:
        print('true')
        ledbuffer+=b"\x00\x25\x00"
    else:
        ledbuffer+=b"\x25\x00\x00"

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
from multiprocessing import Pool
def async_get(url):
    url = url.strip()
    try:
        return (url,requests.get(url,verify=False,timeout=5).json())
    except Exception as e:
        print("ERROR: " + url + " -> " +str(e) )
        return (url,{})

def main(fn):
    tp = Pool(20)
    with open(fn) as f:
        for ln,ld in enumerate(tp.map(async_get,f)):
            # l < url
            # d < space api response
            l,d=ld

            if l == "http://shackspace.de/spaceapi-query-0.13":
                customLed(ln,b'\x10\x10\xff')
                print('found shackspace')
                continue
            elif not l:
                # fallback when hackerspace api is broken
                customLed(ln,b'\x25\x00\x25')
                continue
            if 'open' in d:
                o =  d['open']
            elif 'state' in d and 'open' in d['state']:
                o = d['state']['open'] 
            else:
                print("cannot find 'open' for {}".format(l))
                o = False
            print(ln,l,o)
            setLed(ln,o)
    
    
    asyncio.get_event_loop().run_until_complete(writeLeds())


if __name__ == "__main__":
    main("wd.lst")
    
