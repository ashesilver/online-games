from socketdatamanager import *
import os

BORNEINF = 19995
PORTS = [ i for i in range(BORNEINF,20000)]


"""
def get_available_port():
	r=20000
	with open("connection_list.txt",'r') as f :
		#l = int(f.readlines().pop().split("::")[-1].split()[-1])
		l = [ int(x.split("::")[-1].split()[-1][:-1]) for x in f.readlines() ]
		for x in PORTS:
			if not(x in l) :
				r = x
	return r

def await_connection(port) :
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((socket.gethostname(),19999))
	s.listen(10)

	connection = None
	while connection == None:
		client, connection = s.accept()
		stream = Stream(client, way = "OUT")
		stream(port, vartype = "int")

	return s,stream,connection

def register_connection(port,name,adress):
	with open("connection_list.txt",'a') as f:
		f.write(f"(id)={name}::(client)={adress}::(host)={port}")
	return
"""


while True :
	"""
	port = get_available_port()
	sckt,stream,adress = await_connection(port)
	stream.way = "IN"
	register_connection(port,stream(),adress)"""

