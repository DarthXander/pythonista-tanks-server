import asyncio
import websockets
import sys

# coroutine for echo server
async def echo(websocket, path):
	print("connection with {!r}".format(path))
	data = await websocket.recv() # recieve some bytes
	print("received {!s} data: {!r}".format(len(data), data))
	
	await websocket.send(data) # send them back!
	print("sent back")

# get port environment variable from command line arguments
args = sys.argv
port = args[1]

address = ('0.0.0.0', port)

# start the async server
server = websockets.serve(echo, address[0], address[1])

# get event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_forever()