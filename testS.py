from socketdatamanager import *
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),19999))
s.listen(10)

connection = None
while connection == None:
	client, connection = s.accept()
	stream = Stream(client, "bonjouère", way = "OUT")
	stream.send(f"hello {connection}")

stream.send()