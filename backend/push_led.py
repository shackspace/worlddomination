#!/usr/bin/env python3
"""usage: push-led HOST URLFILE [loop [TIMEOUT]]

HOST is the esp8266 coap endpoint
URLFILE is the path to the file which contains all the URL endpoints to be tested
if loop is requested TIMEOUT defines the number of minutes to wait before continuing
"""
import struct
import json,sys
from time import sleep
from time import perf_counter as clock
import grequests
import asyncio
from aiocoap import *
from signal import signal,alarm,SIGALRM
import urllib
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.CRITICAL)

log = logging.getLogger()

import urllib3
urllib3.disable_warnings()
logging.captureWarnings(True)

ledbuffer=b'\x00\x00\x00'
#ledbuffer+= b'\x00\x00\x00'*40
setled_path="/v1/f/setLeds"
shackspace_endpoint = "http://shackspace.de/spaceapi-query-0.13"

def main():
    from docopt import docopt
    args = docopt(__doc__)
    host = args['HOST']
    urlfile = args['URLFILE']

    while args['loop']:
        begin = clock()
        timeout = int(args['TIMEOUT'] or 10 ) * 60
        log.info("begin loop, timeout is {}".format(timeout))

        fetchmain(urlfile,host)
        end = clock()
        sleeptime = begin - end + timeout
        log.info("sleeping for another {:.2f} minutes".format(sleeptime/60))
        sleep(sleeptime)
    else:
        fetchmain(urlfile,host)


def customLed(idx,color_data):
    global ledbuffer
    ledbuffer+=color_data

def setLed(idx,state):
    global ledbuffer

    log.debug('State: {}'.format(state) )
    if state == 10:
        ledbuffer+=b"\x20\x25\x00"
    elif state:
        ledbuffer+=b"\x00\x25\x00"
    else:
        ledbuffer+=b"\x25\x00\x00"

@asyncio.coroutine
def writeLeds(host):
    log.info("beginning to write LEDs to {}".format(host))
    protocol = yield from Context.create_client_context()
    request = Message(code=POST,payload=ledbuffer)
    request.set_request_uri('coap://{}{}'.format(host,setled_path))

    try:
        response = yield from protocol.request(request).response
    except Exception as e:
        log.error('Failed to fetch resource:'.format(e))
    else:
        log.info('wrote leds: {}'.format(ledbuffer))
        log.debug('Result: %s\n%r'%(response.code, response.payload))

def fetchmain(fn,host):
    # fn: filename
    # tp: threadpool
    # host: remote host
    reqs = []
    with open(fn) as f:
        for url in f: reqs.append(grequests.get(url.strip(),timeout=5,verify=False))
    def exception_handler(request, exception):
        log.error("{} failed".format(request.url))

    for ln,resp in enumerate(grequests.map(reqs, exception_handler=exception_handler)):
        # l < url
        # d < space api response
        try:
            l = resp.url
            d = resp.json()
        except:
            log.debug("cannot get status of line {}".format(ln))
            l = None
            d = {}
        if l == shackspace_endpoint:
            customLed(ln,b'\x10\x10\xff')
            log.info('found shackspace')
            continue
        elif not d:
            o = 10
        if 'open' in d:
            o =  d['open']
        elif 'state' in d and 'open' in d['state']:
            o = d['state']['open']
        else:
            log.debug("cannot find 'open' for {}".format(l))
            o = 10
        log.info("{}: {} is {}".format(ln,l,o))
        setLed(ln,o)

    asyncio.get_event_loop().run_until_complete(writeLeds(host))


if __name__ == "__main__":
    main()

