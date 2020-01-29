# Communication related functions
import asyncio
import websockets
import threading


# start server, begin accepting connections
def accept_connections(proc):

    # respond to messages and call provided processor on contents
    async def respond(resp, path):
        async for msg in resp:
            proc(msg, resp)

    # listen for new requests
    def listen():

        start_server = websockets.serve(respond, port=8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    # put it on separate thread
    t = threading.Thread(target=listen)
    t.daemon = True
    t.start()
