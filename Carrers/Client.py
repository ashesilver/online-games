import Libs.socketdatamanager as socketdatamanager, Libs.kernelPygame as kernelPygame, Libs.boardGames as boardGames
from Libs.socketdatamanager import IN,OUT

CATCHUP = 19999

def game_gen(players):
	board,decks = [],[]
	for z in players :
		z.inventory.deck = {}
	import data.gamedata as data
	for x in data.cards :
		ar = []
		for y in data.cards[x]["cards"] :
			tmp = boardGames.Card(*y[0])
			tmp.effect = y[1]
			#tmp.button_back = kernelPygame.Button( [int(382*screen_ratio),int(363*screen_ratio)*(x == "opt")+int(449*screen_ratio)*(x != "opt")],[int(131*screen_ratio),int(80*screen_ratio)],	f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png")
			ar.append(tmp)
		for z in players :
			z.inventory.deck[x] = boardGames.Deck(array = ar, counts = [0 for i in range(len(data.cards[x]["count"]))])
		decks.append( boardGames.Deck(array = ar, counts = [ (data.cards[x]["count"][i] if len(players)<5 else data.cards[x]["count"][i]+data.cards[x]["supp"][i]) for i in range(len(data.cards[x]["count"])) ] ))
	i=0
	for x in [1000,500,500,100,3000,1000,4000,5000,-1,100,0,0,0,0]:
		decks[0].id_list[i].price = x
		i+=1
	for x in data.board["pos"]:
		board.append(boardGames.Square(*data.board["squares"][data.board["pos"].index(x)]))
		board[data.board["pos"].index(x)].pos = [int(x[0]*screen_ratio),int(x[1]*screen_ratio)]
	board = boardGames.Board(board) 
	board.clickableGrid = kernelPygame.Button([0,0],[int(900*screen_ratio),int(900*screen_ratio)],"./sprites/Board.bck.jpg","./sprites/Board.bck.jpg","./sprites/Board.bck.jpg")
	board.clickableGrid.name = "Plateau du jeu"

	del data
	return board,decks,boardGames.Dice(6),boardGames.Bank(brouzoufs,1000000*len(players))

def game_connect(roomkey):
	adr = "127.0.0.1"
	return socketdatamanager.Stream(socketdatamanager.create_socket(adr,roomkey),way=IN)

def game_create():
	exchange = game_connect(CATCHUP)
	return exchange(retur=True)

#!!! original resolution : (1200,900) !!!
window = kernelPygame.Graphics(resRatio=4/3)

#!!! relative window (nice, userfriendly) !!!
screen_ratio = window.screen_l/1200

"""note : POUR LE MAIN SERVER"""
"""
for x in decks :
	x.chooseTopcard()"""

menu_bttn_gameLaunch = kernelPygame.Button([int(415*screen_ratio),int(374*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.menu.idle.png","./sprites/Jouer.menu.click.png","./sprites/Jouer.menu.hover.png")

window.bckg = "./sprites/bck_menu.png"
window.caption = "Jeu du succès"

exit = False
menu = True
inGame = False
options = False

pawnImages = [ window.load_image(f"./sprites/pawn.{i}.png",[int(75*screen_ratio),int(75*screen_ratio)]) for i in range(12) ]
brouzoufs = [boardGames.BankNote(50),boardGames.BankNote(100),boardGames.BankNote(500),boardGames.BankNote(1000),boardGames.BankNote(5000),boardGames.BankNote(10000)]

#clickzonetemp=[]
while not (exit) :
	window.displayBackgroundUpdate()

	if menu :
		gameCreation = menu_bttn_gameLaunch()
		if gameCreation :
			menu = False
			del menu_bttn_gameLaunch
			window.bckg = "./sprites/bck.png"
			
			#!!! setup creation !!!
			selectMode = False
			deactivate = 60
			playerTotal = 2
			players = [
				kernelPygame.Textzone(25,[int(415*screen_ratio),int(250*screen_ratio)],maxlength=20, text="Joueur 1"),
				kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+55)*screen_ratio)],maxlength=20, text="Joueur 2")
				]
			for x in players :
				x.loadKeysAttributes()
			delPlayerButtons = [
				kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int(238*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"),
				kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+55)*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png")
			]
			selectColors = [
				kernelPygame.Button([int(415+(22*(15*1.1))*screen_ratio),int((238)*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/color.idle.png","./sprites/color.click.png","./sprites/color.hover.png"),
				kernelPygame.Button([int(415+(22*(15*1.1))*screen_ratio),int((238+55)*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/color.idle.png","./sprites/color.click.png","./sprites/color.hover.png")
			]
			colors=[0,1]
			addNewPlayer = kernelPygame.Button([int(445*screen_ratio),int(120*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.gameCreation.idle.png","./sprites/Jouer.gameCreation.click.png","./sprites/Jouer.gameCreation.hover.png")
			playButton = kernelPygame.Button([int(445*screen_ratio),int(10*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.menu.idle.png","./sprites/Jouer.menu.click.png","./sprites/Jouer.menu.hover.png")

	if gameCreation :
		#!!! game creation menu !!!
		delete = False

		for x in players:
			x()

		for x in colors :
			window.displayActivatable({"position":[int(300*screen_ratio),int((238+(55*colors.index(x)))*screen_ratio)],"image":kernelPygame.resizeImage(pawnImages[x],[int(35*screen_ratio),int(35*screen_ratio)])})
		i=0
		while not(selectMode) and i<playerTotal:
			if selectColors[i]() :
				colorChoice = kernelPygame.Button([int(50*screen_ratio),0],[int(75*screen_ratio),int(900*screen_ratio)],"./sprites/colorSelect.png","./sprites/colorSelect.png","./sprites/colorSelect.png")
				selectMode = True
				selection = i
				del selectColors
				selectColors = []
				tmp = colors[:]
				tmp.remove(colors[selection])
			i+=1

		if selectMode :
			
			if colorChoice() and not(int(colorChoice.mp[1]/(window.screen_h/12)) in tmp):
				colors[selection] = int(colorChoice.mp[1]/(window.screen_h/12))
				selectColors = [ kernelPygame.Button([int(415+(22*(15*1.1))*screen_ratio),int((238+(55*i))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/color.idle.png","./sprites/color.click.png","./sprites/color.hover.png") for i in range(playerTotal)]
				selectMode = False
				del colorChoice
				#print(colors[selection])

		i = 0
		while not(delete) and i<playerTotal:
			if delPlayerButtons[i]() and deactivate>30 :
				#del players[i],delPlayerButtons[i]
				deactivate = 0
				tmp = [x.text if x.text!= [] else x.base for x in players]
				del tmp[i],players,delPlayerButtons,selectColors
				del colors[i]
				players,delPlayerButtons,selectColors = [],[],[]
				delete = True
				playerTotal -= 1
				for x in tmp :
					players.append(kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+(55*(tmp.index(x))))*screen_ratio)],maxlength=20, text=f"Joueur {tmp.index(x)+1}"))
					players[tmp.index(x)].loadKeysAttributes()
					if not("Joueur" in x) :
						players[tmp.index(x)].text = x
					delPlayerButtons.append(kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+(55*(tmp.index(x))))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"))
					selectColors.append(kernelPygame.Button([int(415+(22*(15*1.1))*screen_ratio),int((238+(55*(tmp.index(x))))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/color.idle.png","./sprites/color.click.png","./sprites/color.hover.png"))

			i+=1
		if playerTotal<12 and addNewPlayer() and deactivate>20:
			playerTotal += 1
			players.append(kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+(55*(playerTotal-1)))*screen_ratio)],maxlength=20, text=f"Joueur {playerTotal}"))
			players[-1:][0].loadKeysAttributes()
			delPlayerButtons.append(kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+(55*(playerTotal-1)))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"))
			selectColors.append(kernelPygame.Button([int(415+(22*(15*1.1))*screen_ratio),int((238+(55*(playerTotal-1)))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/color.idle.png","./sprites/color.click.png","./sprites/color.hover.png"))
			i = playerTotal-1
			while True:
				if not(i%12 in colors) :
					colors.append(i%12)
					break
				else :
					i+=1
			deactivate = 0
		deactivate += 1 - 999*(deactivate > 1000)

		inGame = playButton()

		#
		if inGame :
			#!!! reset menus !!!
			gameCreation = False
			tmp = [x.text if x.text!= "" else x.base for x in players]

			#!!! del all buttons !!!
			del players
			del delPlayerButtons
			del addNewPlayer
			del playButton
			if selectMode:
				del colorChoice
			#!!! setup the game !!!

			players = [boardGames.Player(name=tmp[colors.index(x)],id = x,bank = {"bankNotes" : brouzoufs,"total" : 1000},inventory=True) for x in colors]
			zoomPerCarrer,fullLune = True,True
			board,decks,dice,gameBank = game_gen(players)

			inventory, displayLune = False, False
			ZOOM = {"pos" : [int(900*screen_ratio),0],"size" : [int(300*screen_ratio),int(300*screen_ratio)]}
			zoomTargetText = kernelPygame.Textzone(26,[ZOOM["pos"][0],ZOOM["pos"][1]+ZOOM["size"][1]],maxlength=34,text = "Cliquez sur un élément pour afficher sa description ici")
			zoomTargetText.loadKeysAttributes()
			zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
			zoomTarget = {**ZOOM,"imageAdress":"./sprites/whitespace.bmp","position":[int(900*screen_ratio),0],"image" : None}
			
			Lune = {"position" : [int(900*screen_ratio),0],"image" : window.load_image(f"./sprites/carrer.L.png",[int(300*screen_ratio),int(500*screen_ratio)])}

			inventoryTextzone = kernelPygame.Textzone(25,[ZOOM["pos"][0]+int(5*screen_ratio),ZOOM["pos"][1]+int(5*screen_ratio)],maxlength=20,text = "Coeurs : 0 // Etoiles : 0 // ßrouzoufs : 0 // Salaire : 0")

			actionButtons = []
			for i in range(11) :
				actionButtons.append(kernelPygame.Textzone(25,[int((935+(150*((i if i<=8 else i-1)>4)))*screen_ratio),int((372+(25*((i%4 if i<=8 else i%6))))*screen_ratio)],maxlength= 12,
				text = "Dés"*(i==0)+"Opportunité"*(i==1)+"Expérience"*(i==2)+"Payer"*(i==3)+"Passer tour"*(i==4)+"Sortir (Dés)"*(i==5)+"Vacances"*(i==6)+"Carrière"*(i==7)+"Plateau"*(i==8)+"Confirmer"*(i==9)+"Actions"*(i==10)))
				actionButtons[i].id = i
			actions = False
			confirm = False

			from random import shuffle
			shuffle(players)
			for x in players :
				x.inventory.button = kernelPygame.Button([int((900+(150*(x.id>5)))*screen_ratio),int((615+(50*(x.id%6)))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],f"./sprites/pawn.{x.id}.png",f"./sprites/pawn.{x.id}.png",f"./sprites/pawn.{x.id}.png")
				x.inventory.stars = 0
				x.inventory.hearts = 0
				x.inventory.salary = 1000
				x.square_id = 0
			
				x.name = kernelPygame.Textzone(25,[int((945+(150*(x.id>5)))*screen_ratio),int((622+(50*(x.id%6)))*screen_ratio)], text=f"J{players.index(x)+1}: {x.name}")
				x.name.graphicUpdate()

			currentPlayer = 0
			def roll(currentPlayer,dice):
				if players[currentPlayer].square_id > 100:
					dice.roll()
				else :
					dice.multiRoll()
				return dice.value["total"]

			def checkprice(currentPlayer,oppt=None,price=0,buyable_amount=1):
				if oppt != None :
					return players[currentPlayer].bank.verify(oppt.price)
				elif price!=0 :
					return players[currentPlayer].bank.verify(price)
				elif players[currentPlayer].square_id == 6:
					return players[currentPlayer].bank.verify(1000*buyable_amount) and players[currentPlayer].inventory.salary <= 1000*buyable_amount
				elif players[currentPlayer].square_id == 8:
					return players[currentPlayer].bank.verify(int(players[currentPlayer].inventory.salary/2))
				elif players[currentPlayer].square_id == 13:
					return players[currentPlayer].bank.verify(3000*buyable_amount) and buyable_amount<3
				elif players[currentPlayer].square_id == 26:
					return players[currentPlayer].bank.verify(3000*buyable_amount)
				else :
					return True

			execute = False

	if inGame :
		#window.displayActivatable(board.image)
		if board.clickableGrid(): 
			
			#print([int(board.clickableGrid.mp[0]*(1/screen_ratio)),int(board.clickableGrid.mp[1]*(1/screen_ratio))])
			"""
			if not([int(board.clickableGrid.mp[0]*(1/screen_ratio)),int(board.clickableGrid.mp[1]*(1/screen_ratio))]) in clickzonetemp:
				clickzonetemp.append([int(board.clickableGrid.mp[0]*(1/screen_ratio)),int(board.clickableGrid.mp[1]*(1/screen_ratio))])"""
			zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
			zoomImage = None
			displayLune = False
			inventory = False
			
			if board.clickableGrid.mp[0] < 134*screen_ratio :

				if board.clickableGrid.mp[1] < 134*screen_ratio :

					zoomImage = window.load_image("./sprites/board.A1.png",[int(300*screen_ratio),int(300*screen_ratio)])
					zoomTargetText.text = "faites 7, 11 ou un double aux dés OU payez 1/2 de votre argent liquide pour sortir."

				elif board.clickableGrid.mp[1] > 134*screen_ratio and board.clickableGrid.mp[1] < 757*screen_ratio :
					array = ["opt","A3","A4","opt","A6","A7","opt"]
					arrayTxt = [ "recevez une carte d'opportunité",
							"Vous pouvez partir en mer. Prix d'admission : 100ß",
							"Vous pouvez acheter un maximum de 2 tableaux pour 3000ß chacun. Marquez autant d'étoiles que le nombre des dés et de tableaux",
							"recevez une carte d'opportunité",
							"Vous pouvez faire des affaires. Prix d'admission : 500ß",
							"Payez le 1/4 de votre argent liquide",
							"recevez une carte d'opportunité"
					]

					for i in range(7):
						if 134*screen_ratio + i*89*screen_ratio < board.clickableGrid.mp[1] and 134*screen_ratio + (i+1)*89*screen_ratio > board.clickableGrid.mp[1] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[int(300*screen_ratio),int(300*screen_ratio)])
							zoomTargetText.text = arrayTxt[i]

				else :
					zoomImage = window.load_image("./sprites/board.A9.png",[int(300*screen_ratio),int(300*screen_ratio)])
					zoomTargetText.text = "faites 5 ou moins aux dés OU payez 1/2 salaire pour sortir."

			elif board.clickableGrid.mp[0] > 134*screen_ratio and board.clickableGrid.mp[0] < 757*screen_ratio :
				if board.clickableGrid.mp[1] < 134*screen_ratio :

					array = ["opt","C1","D1","opt","F1","G1","opt"]
					arrayTxt = [ "recevez une carte d'opportunité",
							"Payez 1/2 de votre salaire",
							"Vous pouvez faire de la politique. Prix d'admission : 3000ß",
							"recevez une carte d'opportunité",
							"Payez 10% de votre argent liquide mulitiplié par le nombre du dé",
							"Vous pouvez faire du cinéma. Prix d'admission : 1000ß",
							"recevez une carte d'opportunité"
					]

					for i in range(7):
						if 134*screen_ratio + i*89*screen_ratio < board.clickableGrid.mp[0] and 134*screen_ratio + (i+1)*89*screen_ratio > board.clickableGrid.mp[0] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[int(300*screen_ratio),int(300*screen_ratio)])
							zoomTargetText.text = arrayTxt[i]

				elif board.clickableGrid.mp[1] > 134*screen_ratio and board.clickableGrid.mp[1] < 757*screen_ratio :
					#carré interieur
					array= [ [l+c for l in "BCDEFGH"] for c in "2345678" ] if not(zoomPerCarrer) else [['M','M',"P","P","P","C","C"],['M','M',"P","P","P","C","C"],["A","A",None,None,None,"U","U"],["A","A",None,None,None,"U","U"],["A","A",None,None,None,"U","U"],["D","D","F","F","Ltop","Lbot","Lbot"],["D","D","F","F","Ltop","Lbot","Lbot"]]
					counterarray = [ l+c for l in "DEF" for c in "456"] + [None]

					for i in range(7):
						for y in range(7):
							if not(array[i][y] in counterarray) and (134*screen_ratio + y*89*screen_ratio < board.clickableGrid.mp[0] and 134*screen_ratio + (y+1)*89*screen_ratio > board.clickableGrid.mp[0] ) and ( 134*screen_ratio + i*89*screen_ratio < board.clickableGrid.mp[1] and 134*screen_ratio + (i+1)*89*screen_ratio > board.clickableGrid.mp[1] ):
								zoomImage = window.load_image(f"./sprites/{'board' if not(zoomPerCarrer) else 'carrer'}.{array[i][y]}.png",[int(300*screen_ratio),int(300*screen_ratio)])
					if (134*screen_ratio + 4*89*screen_ratio < board.clickableGrid.mp[0] and 134*screen_ratio + 7*89*screen_ratio > board.clickableGrid.mp[0] ) and ( 134*screen_ratio + 5*89*screen_ratio < board.clickableGrid.mp[1] and 134*screen_ratio + 7*89*screen_ratio > board.clickableGrid.mp[1] ) and zoomPerCarrer and fullLune :
						displayLune = True
								

				else :
					#bottom line
					array = ["B9","C9","opt","E9","opt","G9","opt"]
					arrayTxt = [ "Vous pouvez allez à l'université. Prix d'admission : 500ß",
							"Vous pouver acheter des coeurs jusqu'à 1 salaire. Rayez un coeur si vous n'en achetez pas",
							"recevez une carte d'opportunité",
							"Vous pouvez faire de l'agriculture. Prix d'admission : 1000ß",
							"recevez une carte d'opportunité",
							"Payez des impôts en fonction de votre salaire",
							"recevez une carte d'opportunité"
					]

					for i in range(7):
						if 134*screen_ratio + i*89*screen_ratio < board.clickableGrid.mp[0] and 134*screen_ratio + (i+1)*89*screen_ratio > board.clickableGrid.mp[0] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[int(300*screen_ratio),int(300*screen_ratio)])
							zoomTargetText.text = arrayTxt[i]

			else :
				if board.clickableGrid.mp[1] < 134*screen_ratio :
					#topright corner
					zoomImage = window.load_image("./sprites/board.I1.png",[int(300*screen_ratio),int(300*screen_ratio)])
					zoomTargetText.text = "recevez 4 coeurs on arrivant sur cette case. vous marquez 2 coeurs supp par tours en y restant (7 ou moins aux dés)"
				elif board.clickableGrid.mp[1] > 134*screen_ratio and board.clickableGrid.mp[1] < 757*screen_ratio:
					#sideright line
					array = ["opt","I3","I4","opt","I6","I7","I8"]
					arrayTxt = [ "recevez une carte d'opportunité",
							"Vous pouvez acheter des actions pour 3000ß chacune. ",
							"Vous pouvez participer à la prospection d'uranium. Prix d'admission : 4000ß",
							"recevez une carte d'opportunité",
							"Vous pouvez acheter des coeurs",
							"Vous pouvez faire participer à l'expédition lunaire. Prix d'admission : 5000ß",
							"Vous pouvez acheter des étoiles"
					]

					for i in range(7):
						if 134*screen_ratio + i*89*screen_ratio < board.clickableGrid.mp[1] and 134*screen_ratio + (i+1)*89*screen_ratio > board.clickableGrid.mp[1] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[int(300*screen_ratio),int(300*screen_ratio)])
							zoomTargetText.text = arrayTxt[i]

				else :
					#bottomright corner
					zoomImage = window.load_image("./sprites/board.I9.png",[int(300*screen_ratio),int(300*screen_ratio)])
					zoomTargetText.text = "Touchez votre salaire en passant sur cette case. Doublez si vous vous arretez dessus."

		#!!! inventaires !!!
		for x in players:
			rendered_playername = x.name.rendered
			x.name.mouseover()
			#!!! cheese strat !!!
			x.rendered = rendered_playername
			x.name.graphicUpdate(True)
			if x.inventory.button() or (x.name.focused and x.name.hover):
				zoomTargetText.text=f"Inventaire de : {x.name.base[4:]}"
				inventoryTextzone._text= f"Coeurs : {x.inventory.hearts}\nEtoiles : {x.inventory.stars}\nßrouzoufs : {x.money.total}\nSalaire : {x.inventory.salary}".split('\n')
				
				"""
				for x in x.decks :
					pass"""

				zoomImage = None
				displayLune = False
				inventory = True

		endturn = False
		#!!! actions !!!
		if not(actions and confirm) :
			actionButtons[-1].mouseover()
			actionButtons[-1].graphicUpdate(True)
			if (actionButtons[-1].focused and actionButtons[-1].hover) :
				actionButtons[-1].focused = False
				actionButtons[-1].graphicUpdate(True)
				actions = True
				inventory = False
		if actions:
			for x in actionButtons[:-2]:
				if x.id in board.squaresArray[players[currentPlayer].square_id].actions:
					x.mouseover()
					x.graphicUpdate(True)
					if (x.focused and x.hover) :
						x.focused = False
						x.graphicUpdate(True)
						actions = False
						confirm = True
						actionSelected = actionButtons.index(x)
		if confirm and not(actions):
			actionButtons[-2].mouseover()
			actionButtons[-2].graphicUpdate(True)
			if (actionButtons[-2].focused and actionButtons[-2].hover) :
				actionButtons[-2].focused = False
				actionButtons[-2].graphicUpdate(True)
				confirm = False
				execute = True
				#!!! éxecuter l'action !!!
				players[currentPlayer].action = actionSelected
		if execute:
			if actionSelected == 0 :
				#advance = roll(currentPlayer,dice)
				players[currentPlayer].square_id = (players[currentPlayer].square_id + roll(currentPlayer,dice)) #%32 for tests
				endturn = True
				execute = False
				actionSelected = -1
			
			"""
			elif actionSelected == 1:
				pass
			elif actionSelected == 2:
				pass
			elif actionSelected == 3:
				pass
			elif actionSelected == 4:
				pass
			elif actionSelected == 5:
				pass
			elif actionSelected == 6:
				pass
			elif actionSelected == 7:
				pass
			elif actionSelected == 8:
				pass"""

		#!!! tour suivant !!!
		if endturn :
			if players[currentPlayer].square_id in [1,3,5,9,12,15,17,20,23,25,28]:
				players[currentPlayer].inventory.deck["opt"].counts[decks[0].id_list.index(decks[0].draw())] += 1


			currentPlayer = (currentPlayer + 1)%len(players)
			
		#!!! display !!!
		for x in players :
			window.displayActivatable({"image":kernelPygame.resizeImage(pawnImages[x.id],[int(45*screen_ratio),int(45*screen_ratio)]),"position":board.squaresArray[x.square_id].pos})

		window.displayActivatable({"image":None,"imageAdress":"./sprites/line.png","size":[int(150*screen_ratio),int(5*screen_ratio)],"position" : [int((915+(150*(players[currentPlayer].id>5)))*screen_ratio),int((655+(50*(players[currentPlayer].id%6)))*screen_ratio)]})
		
		#!!! Zoom !!!
		zoomTarget["image"] = zoomImage
		
		if not displayLune :
			zoomTargetText.graphicUpdate()
			if inventory :
				inventoryTextzone.graphicUpdate(noInput = True)
			else :
				window.displayActivatable(zoomTarget)
		else :
			window.displayActivatable(Lune)

	if options:
		pass

	exit = window()

#print(clickzonetemp)