import asyncio
import websockets
import sys
import pickle
import struct
from io import BytesIO

# communications of the form:
# | connection id | type     | data
# | (2 bytes)     | one byte | ....

def encode(obj):
	b = BytesIO()
	pickle.dump(obj, b)
	return b.getvalue()

def decode(obj):
	return pickle.loads(obj)

def encnum(obj):
	return struct.pack('H', obj)

def decnum(obj):
	return struct.unpack('H', obj)[0]

class PlayerInfo (object):
	nickname = None
	position = None
	color = None
	model = None
	arm_angle = None

	setup = ["nickname", "color", "model"]
	update = ["position", "arm_angle"]

	def __init__(self, **kwargs):
		for name, arg in kwargs.items():
			setattr(self, name, arg)
	def get_setup(self):
		result = {}
		for attrib in self.setup:
			result[attrib] = getattr(self, attrib)
		return result
	def get_update(self):
		result = {}
		for attrib in self.update:
			result[attrib] = getattr(self, attrib)
		return result
	def get_all(self):
		return {**get_setup(), **get_update()}

def get_info(kind):
	valid = ["setup", "update", "all"]
	if kind not in valid:
		raise ValueError("can only get data types in {!r}".format(valid))
	method_name = "get_" + kind
	result = {}
	for idnum, player in players.items():
		info_dict = getattr(player, method_name)()
		result[idnum] = info_dict
	return result

new_connection = 0x0

send_info = 0x1

get_all_info = 0x2
get_setup_info = 0x3
get_update_info = 0x4
get_simplifier = {get_all_info : "all", get_setup_info : "setup", get_update_info : "update"}

connections = []
players = {}

id_inc = 0

# coroutine for echo server
async def tank_coro(websocket, path):
	print("connection with {!r}".format(websocket.remote_address))
	data = await websocket.recv() # recieve some bytes
	print("received {!s} data: {!r}".format(len(data), data))
	if len(data) < 3:
		raise AssertionError()
	idnum = decnum(data[0:2])
	messagetype = data[2]
	message = data[3:]
	if messagetype == new_connection:
		global id_inc, players
		print("establishing new connection, sending id number ({}) to confirm".format(id_inc))
		await websocket.send(bytes([id_inc]))
		connections.append(id_inc)
		print("confirmed. {!s} connections total".format(len(connections)))
		print("creating player info for {}".format(id_inc))
		players[id_inc] = PlayerInfo()
		id_inc += 1
	else:
		if idnum not in connections:
			print("received info from {}; connection wasn't established".format(idnum))
			raise ValueError("invalid connection")
		if messagetype == send_info:
			print("recieved information about {!s}...".format(idnum))
			info = decode(message)
			print("message type: {!r}".format(type(info)))
			for attr, data in info.items():
				print("{}: {!r}".format(attr, data))
				setattr(players[idnum], attr, data)
		elif messagetype in get_simplifier:
			print("recieved request for all tank info from {}".format(idnum))
			tosend = encode(get_info(get_simplifier[messagetype]))
			print("sending...")
			await websocket.send(tosend)
			print("sent")
			


# get port environment variable from command line arguments
args = sys.argv
port = args[1]

address = ('0.0.0.0', port)

# start the async server
server = websockets.serve(tank_coro, address[0], address[1])
print("waiting for a connection")
# get event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_forever()