from socketdatamanager import *
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("192.168.1.44",19999))
s.listen(10)

connection = None
while connection == None:
	client, connection = s.accept()
	stream = Stream(client, way = "OUT")
	stream.send(f"hello {connection}")

stream.way="IN"

print(stream(retur = True))
print(stream(retur = True))
print(stream(retur = True))

s.close()