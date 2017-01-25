import asyncio
import websockets

async def call():
	async with websockets.connect(address) as websocket:
		print("connection made with {}".format(address))
		message = input("send message: ")
		await websocket.send(message)
		print("sent")

		echo = await websocket.recv()
		print("recieved message: {!r}")

address = "ws://boiling-caverns-15454.herokuapp.com:80"

loop = asyncio.get_event_loop()

loop.run_until_complete(call())