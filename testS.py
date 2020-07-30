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

stream("wassup", vartype = "str")
stream(47,vartype = "int")
stream([1,2,3,4,5], vartype = "list", subtype = "int")
