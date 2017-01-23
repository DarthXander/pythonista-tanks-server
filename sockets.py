import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com",80))
ip = s.getsockname()[0]
s.close()

print "self ip: %s" % ip

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (ip, 10005)
s.bind(address)
s.listen(1)

while True:
	connection, client_address = s.accept()
	print "accepted connection at %s" % client_address[0]
	message = ""
	while True:
		data = connection.recv(15)
		if data:
			print "recieved %d data" % len(data)
			message += data
		else:
			print "finished receiving %d data in total" % len(message)
			break
	print "data: %s" % message
