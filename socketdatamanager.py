#socketdatamanager
import socket

class Data(object):
	"""docstring for Data"""
	def __init__(self, socket):
		self.socket = socket
		self.history = []

	@property
	def content(self):
		return self._content

	@content.setter
	def content(self, value):
		self.history.append(self._content)
		self._content = value

	@content.deleter
	def content(self):
		self._content = None

	def send(self, string, endbuffer = "-TRover-", encoding= "utf-8"):
		self.socket.send(bytes(string+endbuffer,encoding))

	def recieve(self, bufferend= "-TRover-", encoding= "utf-8"):
		del self.content
		running = True
		data = bytearray()
		stop = bytes(bufferend,"utf-8")
		while running:
			data.extend(self.socket.recv(1))
			if (stop in data) :
				running =False
		self.content = str(data[:-len(bufferend)].decode(encoding))

	def unpack(self, vartype= "str"):
		types = ["list","dict","tuple","int","str","bool","object","func","exec"]
		headers = ['L!','D!','T!','I!','S!','B!','O!','F!','E!']
		if self.content[:1] == types[headers.index(vartype)]:
			try:
				self.content = types[headers.index(vartype)](self.content[2:])
			except TypeError:
				pass

	def pack(self, vartype = "str", splitter = None):
		types = ["list","dict","tuple","int","str","bool","object","func","exec"]
		headers = ['L!','D!','T!','I!','S!','B!','O!','F!','E!']
		head = headers[types.index(vartype)]
		if vartype in ["list","tuple"]:
			head += splitter
			for x in self.content :
				head += str(x)+splitter
			self.content = head[:-len(splitter)]
		if vartype == "bool":
			self.content = head if not(self.content) else head+"1"

