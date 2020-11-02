import Libs.socketdatamanager as socketdatamanager, Libs.kernelPygame as kernelPygame, Libs.boardGames as boardGames
from Libs.socketdatamanager import IN,OUT

CATCHUP = 19999

def game_gen(players):
	board,decks,die = None,[],[]
	import data.gamedata as data
	for x in data.cards :
		ar = []
		for y in data.cards[x]["cards"] :
			tmp = boardGames.Card(*y)
			#tmp.button_back = kernelPygame.Button( [int(382*screen_ratio),int(363*screen_ratio)*(x == "opt")+int(449*screen_ratio)*(x != "opt")],[int(131*screen_ratio),int(80*screen_ratio)],	f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png")
			ar.append(tmp)
		decks.append( boardGames.Deck(array = ar, counts = [ (data.cards[x]["count"][i] if len(players)<5 else data.cards[x]["count"][i]+data.cards[x]["supp"][i]) for i in range(len(data.cards[x]["count"])) ] ))
		

	board = boardGames.Board()
	board.clickableGrid = kernelPygame.Button([0,0],[int(900*screen_ratio),int(900*screen_ratio)],"./sprites/Board.bck.jpg","./sprites/Board.bck.jpg","./sprites/Board.bck.jpg")
	board.clickableGrid.name = "Plateau du jeu"
	#board.image = {"image" : window.load_image("./sprites/Board.bck.jpg",[900,900]), "position" : [0,0]}

	return board,decks,die

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



menu_bttn_gameLaunch = kernelPygame.Button([int(415*screen_ratio),int(374*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.menu.idle.png","./sprites/Jouer.menu.click.png","./sprites/Jouer.menu.hover.png")

"""note : POUR LE MAIN SERVER"""
"""
for x in decks :
	x.chooseTopcard()"""

window.bckg = "./sprites/bck_menu.png"
window.caption = "Jeu du succès"

exit = False
menu = True
inGame = False
options = False
while not (exit) :
	window.displayBackgroundUpdate()

	if menu :
		gameCreation = menu_bttn_gameLaunch()
		if gameCreation :
			menu = False
			del menu_bttn_gameLaunch
			window.bckg = "./sprites/bck.png"
			
			#!!! setup creation !!!
			deactivate = 60
			playerTotal = 2
			players = [
				kernelPygame.Textzone(25,[int(415*screen_ratio),int(250*screen_ratio)],maxlength=40, text="Joueur 1"),
				kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+55)*screen_ratio)],maxlength=40, text="Joueur 2")
				]
			for x in players :
				x.loadKeysAttributes()
			delPlayerButtons = [
				kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int(238*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"),
				kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+55)*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png")
			]
			addNewPlayer = kernelPygame.Button([int(445*screen_ratio),int(120*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.gameCreation.idle.png","./sprites/Jouer.gameCreation.click.png","./sprites/Jouer.gameCreation.hover.png")
			playButton = kernelPygame.Button([int(445*screen_ratio),int(10*screen_ratio)],[int(311*screen_ratio),int(102*screen_ratio)],"./sprites/Jouer.menu.idle.png","./sprites/Jouer.menu.click.png","./sprites/Jouer.menu.hover.png")


	if gameCreation :
		#!!! game creation menu !!!
		delete = False
		for x in players:
			x()
		i = 0
		while not(delete) and i<playerTotal:
			if delPlayerButtons[i]() and deactivate>30 :
				#del players[i],delPlayerButtons[i]
				deactivate = 0
				tmp = [x.text if x.text!= "" else x.base for x in players]
				del tmp[i],players,delPlayerButtons
				players,delPlayerButtons = [],[]
				delete = True
				playerTotal -= 1
				for x in tmp :
					players.append(kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+(55*(tmp.index(x))))*screen_ratio)],maxlength=15, text=f"Joueur {tmp.index(x)+1}"))
					players[tmp.index(x)].loadKeysAttributes()
					if not("Joueur" in x) :
						players[tmp.index(x)].text = x
					delPlayerButtons.append(kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+(55*(tmp.index(x))))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"))


			i+=1
		if addNewPlayer() and deactivate>20:
			playerTotal += 1
			players.append(kernelPygame.Textzone(25,[int(415*screen_ratio),int((250+(55*(playerTotal-1)))*screen_ratio)],maxlength=15, text=f"Joueur {playerTotal}"))
			players[-1:][0].loadKeysAttributes()
			delPlayerButtons.append(kernelPygame.Button([int(415+(25*(15*1.1))*screen_ratio),int((238+(55*(playerTotal-1)))*screen_ratio)],[int(35*screen_ratio),int(35*screen_ratio)],"./sprites/Xcross.idle.png","./sprites/Xcross.click.png","./sprites/Xcross.hover.png"))
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
			#!!! start the game !!!
			players = tmp[:]
			zoomPerCarrer,fullLune = True,True
			board,decks,die = game_gen(players)
			ZOOM = {"pos" : [int(900*screen_ratio),0],"size" : [int(300*screen_ratio),int(300*screen_ratio)]}
			zoomTargetText = kernelPygame.Textzone(26,[ZOOM["pos"][0],ZOOM["pos"][1]+ZOOM["size"][1]],maxlength=34,text = "Cliquez sur un élément pour afficher sa description ici",lines=5)
			zoomTargetText.loadKeysAttributes()
			zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
			zoomTarget = {**ZOOM,"imageAdress":"./sprites/whitespace.bmp","position":[int(900*screen_ratio),0],"image" : None}
			Lune = {"position" : [int(900*screen_ratio),0],"image" : window.load_image(f"./sprites/carrer.L.png",[int(300*screen_ratio),int(500*screen_ratio)])}

	if inGame :
		#window.displayActivatable(board.image)

		if board.clickableGrid(): 
			#print([board.clickableGrid.mp[0]*screen_ratio,board.clickableGrid.mp[1]*screen_ratio])
			displayLune = False
			zoomImage = None
			zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
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

			zoomTarget["image"] = zoomImage
	
		#decks[0].topcard.button_back();decks[1].topcard.button_back()
		if not displayLune :
			zoomTargetText()
			window.displayActivatable(zoomTarget)
		else :
			window.displayActivatable(Lune)

	if options:
		pass


	exit = window()
