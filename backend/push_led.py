#!/usr/bin/env python3
"""usage: push-led HOST URLFILE [loop [TIMEOUT]]

HOST is the esp8266 coap endpoint
URLFILE is the path to the file which contains all the URL endpoints to be tested
if loop is requested TIMEOUT defines the number of minutes to wait before continuing
"""
import struct
import json,sys
from time import clock,sleep

from multiprocessing import Pool
import asyncio
from aiocoap import *
from signal import signal,alarm,SIGALRM
import urllib
import requests
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
requests.packages.urllib3.disable_warnings()

ledbuffer=b'\x00\x00\x00'
#ledbuffer+= b'\x00\x00\x00'*40
setled_path="/v1/f/setLeds"
shackspace_endpoint = "http://shackspace.de/spaceapi-query-0.13"

loop_timeout=120

def main():
    from docopt import docopt
    args = docopt(__doc__)
    host = args['HOST']
    urlfile = args['URLFILE']

    pool = Pool(30)
    while args['loop']:
        begin = clock()
        timeout = int(args['TIMEOUT'] or 10 ) * 60
        log.info("begin loop, timeout is {}, alarm at 1minute".format(timeout))

        def _timeout(dont,care):raise RuntimeError()

        signal(SIGALRM,_timeout  )
        alarm(loop_timeout)
        try:
            fetchmain(urlfile,pool,host)
        except RuntimeError as e:
            log.error("waited {} secs for loop to complete,loop took too long!".format(loop_timeout))
            pool.terminate()
        finally:
            alarm(0)


        sleeptime = timeout + (clock()-begin)
        log.info("sleeping for another {:.2f} minutes".format(sleeptime/60))
        sleep(sleeptime)
    else:
        fetchmain(urlfile,pool,host)


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

def async_get(url):
    url = url.strip()
    try:
        return (url,requests.get(url,verify=False,timeout=5).json())
    except Exception as e:
        log.error("Error while fetching {}: {}".format(url,e) )
        return (url,{})

def fetchmain(fn,tp,host):
    # fn: filename
    # tp: threadpool
    # host: remote host

    
    with open(fn) as f:
        for ln,ld in enumerate(tp.map(async_get,f)):
            # l < url
            # d < space api response
            l,d=ld

            if l == shackspace_endpoint:
                customLed(ln,b'\x10\x10\xff')
                log.debug('found shackspace')
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
                log.warn("cannot find 'open' for {}".format(l))
                o = 10
            log.info("{}: {} is {}".format(ln,l,o))
            setLed(ln,o)

    asyncio.get_event_loop().run_until_complete(writeLeds(host))


if __name__ == "__main__":
    main()

