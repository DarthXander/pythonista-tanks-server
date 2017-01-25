import asyncio
import websockets
import sys

# coroutine for echo server
async def echo(websocket, path):
	print("connection with {!r}".format(path))
    data = await websocket.recv() # recieve some bytes
    print("received {!s} data: {!r}".format(len(data), data))

    # send them back!
    await websocket.send(data)
    print("sent back")

# get port environment variable from command line arguments
args = sys.argv
port = args[1]

# start the async server
server = websockets.serve(echo, '0.0.0.0', port)

# get event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_forever()