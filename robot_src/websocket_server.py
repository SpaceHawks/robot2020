import asyncio
import websockets

async def response(websocket, path):
	async for msg in websocket:
		print(f"Received message: {msg}")
		await websocket.send("This is a response from the server.")

start_server = websockets.serve(response, "localhost", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
