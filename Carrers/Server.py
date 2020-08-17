import boardGames

mabanque = boardGames.Bank([boardGames.BankNote(x) for x in [50,100,500,1000,5000,10000]],700000)


print(mabanque.equilibrium())

print(mabanque.details(1750))

player = boardGames.Player()