#!/usr/bin/python3
import struct

import json,sys

import asyncio
from aiocoap import *

import urllib
import requests
import sys
requests.packages.urllib3.disable_warnings()

full=78+1
num=int(sys.argv[1])
front=num
back=full-num
ledbuffer=b"\x00\x00\x00"*front
ledbuffer+=b"\xff\x00\x00"
ledbuffer+=b"\x00\x00\x00"*back
host="10.42.26.69"
setled_path="/v1/f/setLeds"


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
        print('Result: %s\n%r'%(response.code, response.payload))

def main(fn):
    asyncio.get_event_loop().run_until_complete(writeLeds())


if __name__ == "__main__":
    main("wd.lst")
    
