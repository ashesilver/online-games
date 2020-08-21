import boardGames

mabanque = boardGames.Bank([boardGames.BankNote(x) for x in [50,100,500,1000,5000,10000]],700000)

"""
print(mabanque.equilibrium())

print(mabanque.details(1750))

player = boardGames.Player()"""

#New game

def game_gen(players):
	decks=[]
	import data.gamedata as data
	for x in data.cards :
		decks.append( boardGames.Deck(array = [ boardGames.Card(*y) for y in data.cards[x]["cards"] ], counts = [ (data.cards[x]["count"][i] if len(players)<5 else data.cards[x]["count"][i]+data.cards[x]["supp"][i]) for i in range(len(data.cards[x]["count"])) ] ))
	board = boardGames.Board()
	dice = boardGames.Dice()

	return board,decks,dice


with open("connection_list.txt","r") as file :
	l = [ int(x.split("::")[-1].split()[-1][:-1]) for x in f.readlines() ]