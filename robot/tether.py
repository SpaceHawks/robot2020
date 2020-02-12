# Communication related functions
import asyncio
import websockets
import threading
import pickle


# start server, begin accepting connections

async def realrespond(msg,path,resp,proc):
    print(msg,path,resp)
    proc(msg,resp)

def accept_connections(proc):

    # respond to messages and call provided processor on contents
    async def respond(resp, path):
        while True:
            msg=await resp.recv()
            await realrespond(msg, path, resp,proc)
    start_server = websockets.serve(respond, "0.0.0.0", port=8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


