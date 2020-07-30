from socketdatamanager import *
import socket


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("tters66.freeboxos.fr", 19999))
response = None
while response == None:
    response = s.recv(128)
print("connected to server !", response.decode("utf-8")[:-8])

stream = Stream(s, way = "IN")
print(stream(retur = True))
print(stream(retur = True))
print(stream(retur = True))
