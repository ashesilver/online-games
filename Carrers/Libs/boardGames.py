class Piece(object):
	"""docstring for Piece"""
	def __init__(self):
		super(Piece, self).__init__()


class Dice(object):
	"""docstring for Dice"""
	def __init__(self, size):
		self.size = size
		self.history = []

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, arg):
		self.history.append(self._value)
		self._value = arg
		self.history = self.history[-25:]

	def roll(self):
		from random import randint
		self.value = {"total" : randint(self.size), "details" : None}

	def multiRoll(self, amount = 2, modifier = 0):
		from random import randint
		det,r = [],0
		for i in range(amount):
			a = randint(self.size)
			det.append(a)
			r+=a

		self.value = {"total" : r+modifier, "details" : det}

	def __call__(self, amount=1, modifier = 0):
		if amount > 1 :
			self.multiRoll(amount,modifier)
		else :
			self.roll(self)
		return self.value


class Card(object):
	"""docstring for Card"""
	def __init__(self, id, description, mood = ""):
		self.hidden = True
		self.description = description
		self.moodText = mood
		self.effect = None
		self.id = id

	def __repr__(self):
		return self.description

class Deck():
	"""docstring for Deck"""
	def __init__(self, array = [], counts = []):
		self.id_list = array
		self.counts = counts
		self.topcard = None

	def chooseTopcard(self):
		import random
		self.topcard = random.choice([ x for x in self.id_list for i in range(self.counts[self.id_list.index(x)]) ])

	def draw(self):
		if self.topcard == None :
			self.chooseTopcard()
		self.counts[index(self.topcard)] -=1
		res = self.topcard;self.topcard = None
		return res


	def __repr__(self):
		return str([ x.__repr__() for x in self.id_list for i in range(self.counts[self.id_list.index(x)])  ])




class Square(object):
	"""docstring for Square"""
	def __init__(self, id):
		self.id_list = id

		self.effect = None

class Board():
	"""docstring for Board"""
	def __init__(self, array = [Square(None)]):
		self.squaresArray = array
		


class BankNote(object):
	"""docstring for Buck"""
	def __init__(self, arg):
		self.value = arg

	def __str__(self):
		return str(self.value)

	def __lt__(self, other):
		return self.value<other.value
	def __le__(self, other):
		return self<other or self==other

	def __gt__(self, other):
		return not(self<=other)
	def __ge__(self, other):
		return not(self<other)

	def __eq__(self, other):
		return self.value == other.value
	def __ne__(self, other):
		return not(self == other)

	def __int__(self):
		return self.value

	def __add__(self,other):
		return int(self) + int(other)
	def __sub__(self,other):
		return int(self) - int(other)
	def __mul__(self,other):
		return int(self) * int(other)
	def __div__(self,other):
		return int(self) / int(other)
	def __mod__(self,other):
		return int(self) % int(other)

class Bank(object):
	"""docstring for Bank"""
	def __init__(self, bankNotes = (BankNote(0)), total = 0):
		self.banknotes_array = sorted(bankNotes)[::-1]
		#self.amount = amount if (amount!= None and len(amount)==len(bankNotes)) else [0 for x in bankNotes]
		self.total = total
	
	def details(self, custom = 0):
		r = []
		i = 0
		total = self.total if custom == 0 else custom
		while total > 0 :
			r.append(int(total/int(self.banknotes_array[i])))
			if r[-1] > 0:
				total = total%int(self.banknotes_array[i])
			i += 1

		if i < len(self.banknotes_array) :
			for y in range(i,len(self.banknotes_array)):
				r.append(0)

		return r

	def equilibrium(self):
		i=0
		for x in self.banknotes_array:
			i+=int(x)
		r = int(self.total/i)
		m = self.total%i
		return [ x+r for x in self.details(m) ]

	def verify(self, amount=0):
		return self.total - amount > 0


	def transfer(self,other,amount=0):
		if self.verify(amount):
			self.total += amount
			other.total -= amount
		else :
			return False




class Inventory():
	"""docstring for Inventory"""
	def __init__(self, *args):
		self.container

class Player():
 	"""docstring for Player"""
 	def __init__(self):
 		self.inventory = Inventory()
 		self.money = Bank()