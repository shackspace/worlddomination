import datetime
import logging
import binascii
import asyncio

import aiocoap.resource as resource
import aiocoap

class PinResource(resource.Resource):
    def __init__(self):
        super(PinResource, self).__init__()
        self.pin=7

    @asyncio.coroutine
    def render_get(self, request):
        return aiocoap.Message(code=aiocoap.CONTENT,
            payload=str(self.pin).encode())

    @asyncio.coroutine
    def render_post(self, request):
        self.pin = int(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED,
                payload=str(self.pin).encode())


class LedResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(LedResource, self).__init__()
        self.buf=""

    @asyncio.coroutine
    def render_get(self, request):
        return aiocoap.Message(code=aiocoap.CONTENT,payload=self.buf)

    @asyncio.coroutine
    def render_post(self, request):
        self.buf=request.payload
        rep = binascii.hexlify(request.payload)
        cn ='LEDs changed to  0x%s' % rep.decode()
        print(cn)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=cn.encode('utf-8'))

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    res=LedResource()
    root.add_resource(('v1','v','buffer'),res)
    root.add_resource(('v1','f','setLeds'),res)
    res2 = PinResource()
    root.add_resource(('v1','v','ledpin'),res2)
    root.add_resource(('v1','f','setLedPin'),res2)

    asyncio.async(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
