#socketdatamanager
import socket

IN = True
OUT = False

class Data(object):
	"""docstring for SuperData"""

	history = []
	def __init__(self, arg):
		self._content = None
		self.content = arg

	@property
	def content(self):
		return self._content

	@content.setter
	def content(self, value):
		self.history.append(self._content)
		self.history = self.history[-25:]
		self._content = value

	@content.deleter
	def content(self):
		self._content = None

	def unpack(self, retur = False):
		types = ["list","tuple",int,str,bool,"object",float,"exec"]
		headers = ['L!','T!','I!','S!','B!','O!','F!','E!']

		if self.content[:2] in "L!T!" :
			splitter = self.content[4]
			a = self.content.split(splitter)
			TMP = a[1:]
			datatype = a[0][2:]
			self.content = [ Data(datatype+x).unpack(True) for x in TMP ]
			if self.content[:2] == "T!" :
				self.content = tuple(self.content)
				self.history.pop()

		elif self.content[:2] in "I!B!F!" :
			self.content = types[headers.index(self.content[:2])](self.content[2:])
		
		elif self.content[:2] in "S!" :
			self.content = self.content[2:]

		if retur :
			return self.content

	def pack(self, vartype = "str", splitter = ';', subtype = None):
		types = ["list","tuple","int","str","bool","object","float","exec"]
		headers = ['L!','T!','I!','S!','B!','O!','F!','E!']
		head = headers[types.index(vartype)]
		if not(subtype is None) :
			head += headers[types.index(subtype)]
		if vartype in ["list","tuple"]:
			head += splitter
			for x in self.content :
				head += str(x)+splitter
			self.content = head[:-len(splitter)]

		elif vartype in ["str","int","float"] :
			self.content = head+str(self.content)
		
		elif vartype == "bool" :
			self.content = head+'1' if self.content else head+'0'
			#self.content = head+str(int(self.content))

class Stream(Data):
	"""docstring for Data"""
	def __init__(self, socket, content = None, way = None):
		Data.__init__(self, content)
		self.socket = socket
		self.way = way

	def send(self, string = None, endbuffer = "-TRover-", encoding= "utf-8"):
		self.socket.send(bytes((string if string != None else self.content)+endbuffer,encoding))

	def recieve(self, endbuffer= "-TRover-", encoding= "utf-8"):
		del self.content
		running = True
		data = bytearray()
		stop = bytes(endbuffer,"utf-8")
		while running:
			data.extend(self.socket.recv(1))
			if (stop in data) :
				running = False
		self.content = str(data[:-len(endbuffer)].decode(encoding))

	def __call__(self, content = None , vartype = "str", splitter = ';', subtype = None, endbuffer = "-TRover-", encoding= "utf-8", retur = False) :
		if not(content is None) :
			self.content = content
		if self.way :
			self.recieve(endbuffer = endbuffer, encoding= encoding)
			return self.unpack(retur = retur)
		else :
			self.pack(vartype = vartype, splitter = splitter, subtype = subtype)
			self.send(endbuffer = endbuffer, encoding= encoding)


def create_socket(adr,port,server = False):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	if server :
		s.bind((adr, port))
		s.listen(1)

		connection = None
		while connection == None:
			client, connection = s.accept()
		s.send(bytes(f"hello {connection}",encoding))

	else :

		s.connect((adr, port))
		response = None
		while response == None:
		    response = s.recv(128)
		print("connected to server !", response.decode("utf-8")[:-8])

	return s