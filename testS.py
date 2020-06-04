from socketdatamanager import *
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),19999))
s.listen(10)

redirect = {"adr" : socket.gethostname(), "port" : 19998}
connection = None
while connection == None:
	client, connection = s.accept()
	stream = Data(client)
	stream.send(f"hello {connection}")


stream.send("S!bonjoir")