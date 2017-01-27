import asyncio
import websockets
import sys

# communications of the form:
# | connection id | type     | data
# | (2 bytes)     | one byte | ....

connections = []
data = {}

# coroutine for echo server
async def echo(websocket, path):
	print("connection with {!r}".format(websocket.remote_address))
	data = await websocket.recv() # recieve some bytes
	print("received {!s} data: {!r}".format(len(data), data))
	idnum = data[0:2]
	messagetype = data[2]
	if route:
		route_to = data[2:4]



	await websocket.send(data) # send them back!
	print("sent back")

# get port environment variable from command line arguments
args = sys.argv
port = args[1]

address = ('0.0.0.0', port)

# start the async server
server = websockets.serve(echo, address[0], address[1])
print("waiting for a connection")
# get event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_forever()