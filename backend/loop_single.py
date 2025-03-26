#!/usr/bin/python3
import struct,time

import json,sys

import asyncio
from aiocoap import *

import urllib
import requests
requests.packages.urllib3.disable_warnings()

ledbuffer=b''
host="10.42.24.7"
setled_path="/v1/f/setLeds"
#max_led=78
max_led=20
filler_buffer=b"\x25\x00\x25"
active_color=b"\x00\xff\x00"


def setLed(idx,color):
    print(f"LED: {idx}")
    global ledbuffer
    idx = idx+1
    ledbuffer=filler_buffer*idx 
    ledbuffer+=color
    ledbuffer+=filler_buffer*(max_led-idx)

async def writeLeds():
    protocol = await Context.create_client_context()
    request = Message(code=POST,payload=ledbuffer)
    request.set_request_uri('coap://{}{}'.format(host,setled_path))

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('wrote leds: {}'.format(ledbuffer))
        #print('Result: %s\n%r'%(response.code, response.payload))
        pass

def main(fn):
    while True:
        for ln in range(max_led):
            time.sleep(0.5)
            setLed(ln,active_color)
            #setLed(17,active_color)


    
            asyncio.get_event_loop().run_until_complete(writeLeds())


if __name__ == "__main__":
    main("wd.lst")
    
