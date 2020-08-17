import Libs.socketdatamanager as socketdatamanager, Libs.kernelPygame as kernelPygame, Libs.boardGames as boardGames

window = kernelPygame.Graphics((1200,900))

def game_gen(players):
	board,decks,die = None,[],[]
	import data.gamedata as data
	for x in data.cards :
		ar = []
		for y in data.cards[x]["cards"] :
			tmp = boardGames.Card(*y)
			tmp.button_back = kernelPygame.Button(
				[382,363 if x == "opt" else 449],
				[131,80],
				f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png",f"./sprites/Card.{x}.back.png")
			ar.append(tmp)
		decks.append( boardGames.Deck(array = ar, counts = [ (data.cards[x]["count"][i] if len(players)<5 else data.cards[x]["count"][i]+data.cards[x]["supp"][i]) for i in range(len(data.cards[x]["count"])) ] ))
		

	board = boardGames.Board()
	board.clickableGrid = kernelPygame.Button([0,0],[900,900],"./sprites/Board.bck.jpg","./sprites/Board.bck.jpg","./sprites/Board.bck.jpg")
	#board.image = {"image" : window.load_image("./sprites/Board.bck.jpg",[900,900]), "position" : [0,0]}

	return board,decks,die


players = ["J1","J2","J3","J4","J5"]
board,decks,die = game_gen(players)
exit = False

menu = True
window.bckg = "./sprites/bck_menu.png"
menu_bttn_gameLaunch = kernelPygame.Button(
											[414,374],
											[311,102],
											"./sprites/Jouer.menu.idle.png","./sprites/Jouer.menu.click.png","./sprites/Jouer.menu.hover.png")

ZOOM = {"pos" : [900,0],"size" : [300,300]}
zoomTargetText = kernelPygame.Textzone(26,[ZOOM["pos"][0],ZOOM["pos"][1]+ZOOM["size"][1]],maxlength=34,text = "Cliquez sur un élément pour afficher sa description ici",lines=5)
zoomTargetText.loadKeysAttributes()
zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
zoomTarget = {**ZOOM,"imageAdress":"./sprites/whitespace.bmp","size":[300,300],"position":[900,0],"image" : None}
""" POUR LE MAIN SERVER"""
for x in decks :
	x.chooseTopcard()

while not (exit) :
	window.displayBackgroundUpdate()

	if menu :
		inGame = menu_bttn_gameLaunch()
		if inGame :
			menu = False


	if inGame :
		#window.displayActivatable(board.image)

		if board.clickableGrid(): 
			#print(board.clickableGrid.mp)
			zoomImage = None
			zoomTargetText.text = "Cliquez sur un élément pour afficher sa description ici"
			if board.clickableGrid.mp[0] < 134 :

				if board.clickableGrid.mp[1] < 134 :

					zoomImage = window.load_image("./sprites/board.A1.png",[300,300])
					zoomTargetText.text = "faites 7, 11 ou un double aux dés OU payez 1/2 de votre argent liquide pour sortir."

				elif board.clickableGrid.mp[1] > 134 and board.clickableGrid.mp[1] < 757 :
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
						if 134 + i*89 < board.clickableGrid.mp[1] and 134 + (i+1)*89 > board.clickableGrid.mp[1] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[300,300])
							zoomTargetText.text = arrayTxt[i]

				else :
					zoomImage = window.load_image("./sprites/board.A9.png",[300,300])
					zoomTargetText.text = "faites 5 ou moins aux dés OU payez 1/2 salaire pour sortir."

			elif board.clickableGrid.mp[0] > 134 and board.clickableGrid.mp[0] < 757:
				if board.clickableGrid.mp[1] < 134 :

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
						if 134 + i*89 < board.clickableGrid.mp[0] and 134 + (i+1)*89 > board.clickableGrid.mp[0] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[300,300])
							zoomTargetText.text = arrayTxt[i]

				elif board.clickableGrid.mp[1] > 134 and board.clickableGrid.mp[1] < 757 :
					#carré interieur
					array= [ [l+c for l in "BCDEFGH"] for c in "2345678" ]
					counterarray = [ l+c for l in "DEF" for c in "456"]

					for i in range(7):
						for y in range(7):
							if not(array[i][y] in counterarray) and (134 + y*89 < board.clickableGrid.mp[0] and 134 + (y+1)*89 > board.clickableGrid.mp[0] ) and ( 134 + i*89 < board.clickableGrid.mp[1] and 134 + (i+1)*89 > board.clickableGrid.mp[1] ):
								zoomImage = window.load_image(f"./sprites/board.{array[i][y]}.png",[300,300])


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
						if 134 + i*89 < board.clickableGrid.mp[0] and 134 + (i+1)*89 > board.clickableGrid.mp[0] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[300,300])
							zoomTargetText.text = arrayTxt[i]

			else :
				if board.clickableGrid.mp[1] < 134 :
					#topright corner
					zoomImage = window.load_image("./sprites/board.I1.png",[300,300])
					zoomTargetText.text = "recevez 4 coeurs on arrivant sur cette case. vous marquez 2 coeurs supp par tours en y restant (7 ou moins aux dés)"
				elif board.clickableGrid.mp[1] > 134 and board.clickableGrid.mp[1] < 757:
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
						if 134 + i*89 < board.clickableGrid.mp[1] and 134 + (i+1)*89 > board.clickableGrid.mp[1] :
							zoomImage = window.load_image(f"./sprites/board.{array[i]}.png",[300,300])
							zoomTargetText.text = arrayTxt[i]

				else :
					#bottomright corner
					zoomImage = window.load_image("./sprites/board.I9.png",[300,300])
					zoomTargetText.text = "Touchez votre salaire en passant sur cette case. Doublez si vous vous arretez dessus."






			zoomTarget["image"] = zoomImage

		
		decks[0].topcard.button_back();decks[1].topcard.button_back()

		zoomTargetText()
		window.displayActivatable(zoomTarget)


	exit = window()
