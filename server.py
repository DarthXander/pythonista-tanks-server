import asyncio
import websockets
import sys

# communications of the form:
# | connection id | type     | data
# | (2 bytes)     | one byte | ....

class PlayerInfo (object):
	def __init__(self, **kwargs):
		for name, arg in kwargs:
			setattr(self, name, arg)

new_connection = 0x0
get_tank_positions = 0x1
send_tank_position = 0x2
send_nickname = 0x3
get_nicknames = 0x4

connections = []
players = {}

# coroutine for echo server
async def echo(websocket, path):
	print("connection with {!r}".format(websocket.remote_address))
	data = await websocket.recv() # recieve some bytes
	print("received {!s} data: {!r}".format(len(data), data))
	if len(data) < 3:
		raise AssertionError()
	idnum = data[0:2]
	messagetype = data[2]
	message = data[3:]
	if messagetype == new_connection:
		print("establishing new connection with {!s}, sending 0x1 to confirm".format(idnum))
		await websocket.send(bytes([0x1]))
		connections.append(idnum)
		print("confirmed. {!s} connections total".format(len(connections)))
	elif messagetype == send_nickname:
		players[idnum] = PlayerInfo(nickname = message.decode("utf-8"))
	elif messagetype = send_tank_position:
		if idnum in players:
			players[idnum].position = ()

	

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