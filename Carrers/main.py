import socketdatamanager,kernel

window = kernel.Graphics((900,900))
window.bckg = "./sprites/Original-game-board-for-Careers.png"


exit = False
while not (exit) :
	window.displayBackgroundUpdate()

	exit = window()
