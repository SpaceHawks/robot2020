import asyncio
import websockets

# websocket;

async def response(websocket, path):
	async for msg in websocket:
		print(f"Received message: {msg}")
		await websocket.send("The server received your data.")

# The port can be set to whatever, as long as it's open
start_server = websockets.serve(response, port=8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
