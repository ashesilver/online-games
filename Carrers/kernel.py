#!/bin/usr/python3
# -*- coding:utf-8 -*-

import os,warnings,sys,time
import pygame
from pygame.locals import *

__version__ = "0.1.0"
__file__ = sys.argv[0]
__system_args__ = sys.argv[1:]
__start_time__ = time.time()

class Resolutions():
	"""Main class for all resolutions"""
	screen_h,screen_l = None,None

	def ratio(self, other):
		return [other.screen_l/self.screen_l,other.screen_h/self.screen_h]

	def resize(self, other, currentSize):
		ratios = self.ratio(other)
		return [int(currentSize[0]*ratios[0]),int(currentSize[1]*ratios[1])]

class Customres(Resolutions):
	"""docstring for Customres"""
	def __init__(self, screen_l, screen_h):
		self.screen_h = screen_h
		self.screen_l = screen_l

	def windowDownsize(self):
		self.screen_l = int(self.screen_l - self.screen_l*0.1)
		self.screen_h = int(self.screen_h - self.screen_h*0.1)


class Graphics(Resolutions):

	"""Graphic handler for all pygame graphicEvents"""
	pygame.init()
	screen = ()
	screen_l = int(pygame.display.Info().current_w*90/100)
	screen_h = int(pygame.display.Info().current_h*90/100)
	clock = pygame.time.Clock()

	def __init__(self,size=(None,None)):

		#print(sys.argv)

		if size!=(None,None):
			Graphics.screen_l,Graphics.screen_h = size[0],size[1]
			options["resolution"] = list(size)

		Graphics.screen = pygame.display.set_mode(options["resolution"])

		if [Graphics.screen_l,Graphics.screen_h] != options["resolution"] :
			Graphics.screen_l = options["resolution"][0]
			Graphics.screen_h = options["resolution"][1]
		
		self._bckg = None
		self.caption = options["caption"]
		del self.name

		#self.loadBasicAttributes()
		#self.loadKeysAttributes()
		#self.loadMouseAttributes()

		#print(pygame.display.get_caption())
	def __repr__(self):
		return self.name

	def __del__(self):
		if options["debug"] :
			print("{1} destructed at {0:.2f}s afar from {start_time}".format(time.time()-__start_time__,str(self),start_time="{}/{}/{} {}:{}\"{}s".format(time.localtime(__start_time__).tm_mday, time.localtime(__start_time__).tm_mon, time.localtime(__start_time__).tm_year,time.localtime(__start_time__).tm_hour, time.localtime(__start_time__).tm_min, time.localtime(__start_time__).tm_sec)))
		if self.__class__!=Graphics:
			self.__class__.instanceCount -= 1

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, text):
		self._name = text

	@name.deleter
	def name(self):
		self._name = "{} instance n°{}".format(self.__class__,self.instanceCount) if self.__class__!=Graphics else self.caption+ " Window"

	def loadKeysAttributes(self):
		""" cross-platform compatibility in progress
		if os.name == "posix" :
			self.keys_nb = [
				273,276,274,275,13,271,27,32,
				38,233,34,39
				]"""
		if os.name == "nt" :
			self.keys_nb = [273,276,274,275,13,271,27,32,303,304,9,305,306,301,8,
				49,50,51,52,53,54,55,56,57,48,45,61,
				113,98,99,100,101,102,103,104,105,106,107,108,59,110,111,112,97,114,115,116,117,118,122,120,121,119]
		else :
			warnings.warn("{} OS ins't supported for pygame kernel {}".format(os.name, __version__),Warning)
			self.keys_nb = []
		self.keys_name = ["UpARR","LeftARR","DownARR","RightARR","Enter","ENTER","esc"," ","Maj","Maj","Tab","ctrl","ctrl","VerrMaj","Backspace",
			"&","é","\"","\'","(","-","è","_","ç","à",")","=",
			"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

	def loadMouseAttributes(self):
		self.leftClick = 0
		self.rightClick = 0

		self._cursor = pygame.mouse.get_cursor()

	def loadBasicAttributes(self):

		self.square = pygame.image.load("./img/whitesquare.png").convert()

	#DISPLAY METHODS
	
	def displaySquare(self,coordinates):
		self.screen.blit(self.square, [ int(x*[self.screen_l,self.screen_h][coordinates.index(x)]) for x in coordinates])

	def displayActivatable(self,element,displaySet=True):
		if element["image"] == None:
			img = pygame.image.load(element["imageAdress"]).convert()
			img = pygame.transform.scale(img, element["size"] )
			element["image"] = img
		else :
			img = element["image"]
		if displaySet :
			self.screen.blit(img, element["position"])
		return element

	def load_image(self,Adr,size):
		return self.displayActivatable({"image":None,"imageAdress":Adr,"size":size},False)["image"]
	
	#background handler
	@property
	def bckg(self):
		return self._bckg

	@bckg.setter
	def bckg(self, adress):
		self._bckg = pygame.image.load(adress).convert()
		self._bckg = pygame.transform.scale(self._bckg, (self.screen_l,self.screen_h))
	
	def displayBackgroundUpdate(self,imageAdress=None,displaySet=True):
		if not imageAdress==None:
			self.bckg = pygame.image.load(imageAdress).convert()
			self.bckg = pygame.transform.scale(self.bckg, (self.screen_l,self.screen_h))
		if displaySet :
			self.screen.blit(self.bckg,(0,0))

	def generalDisplayUpdate(self):
		pygame.display.flip()
		

	def __call__(self, max_framerate=90):
		"""default max FPS set to 90, custom can be passed as arg[0]"""
		self.generalDisplayUpdate()
		Graphics.clock.tick(max_framerate)
		return self.mainloop()

	@property
	def cursor(self):
		return self._cursor

	@cursor.setter
	def cursor(self, ref):
		try : pygame.mouse.set_cursor(*ref)
		except: print("couldn't set cursor : "+str(ref))
		else : print("new cursor set !")

	@cursor.deleter
	def cursor(self):
		pygame.mouse.set_cursor(*self._cursor)

	@property
	def caption(self):
		return pygame.display.get_caption()[0]

	@caption.setter
	def caption(self,new):
		pygame.display.set_caption(new)

	@caption.deleter
	def caption(self):
		pygame.display.set_caption(options["caption"])

	#GETKEYS/MOUSE

	def mainloop(self):
		all_keys = pygame.key.get_pressed()
		if all_keys[pygame.K_F4] and (all_keys[pygame.K_LALT] or all_keys[pygame.K_RALT]):
			return(True)
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				return(True)

		return False

	def getKeys(self):
		keys_input = []
		all_keys = pygame.key.get_pressed()

		for k in self.keys_nb:
			if all_keys[k] :
				keys_input.append(self.keys_name[self.keys_nb.index(k)])
		"""
		try:
			print(all_keys.index(1))
		except ValueError:
			pass
		"""
		
		return keys_input

	def getMouse(self):
		self.leftClick = pygame.mouse.get_pressed()[0]
		self.rightClick = pygame.mouse.get_pressed()[2]
		return pygame.mouse.get_pos()

	##### obsolete

	"""
	def drawGrid(self):  #for level_editor.py
		for x in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(x*self.screen_l/60,0),(x*self.screen_l/60,self.screen_h))
		for y in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(0,y*self.screen_h/60),(self.screen_l,y*self.screen_h/60))"""

class Button(Graphics):
	"""UI clickable elements """

	instanceCount = 0
	def __init__(self,pos,size,*imgadr):

		Button.instanceCount += 1
		del self.name
		self.zone =[pos,size]
		self.clicked= False
		self.hover=False
		self.imgdata = {
			"base":None,
			"hov":None,
			"onclick":None
		}
		(self.base, self.onclick, self.hov) = imgadr

	@property
	def base(self):
		return self._base

	@base.setter
	def base(self,adress):
		self.imgdata["base"]=self.load_image(adress,self.zone[1])

	@property
	def onclick(self):
		return self._onclick

	@onclick.setter
	def onclick(self,adress):
		self.imgdata["onclick"]=self.load_image(adress,self.zone[1])

	@property
	def hov(self):
		return self._hov
	
	@hov.setter
	def hov(self,adress):
		self.imgdata["hov"]=self.load_image(adress,self.zone[1])
	
	def mouseover(self):
		mp = self.getMouse()
		if (( self.zone[0][0] <= mp[0] and self.zone[0][0]+self.zone[1][0] >= mp[0] ) and ( self.zone[0][1] <= mp[1] and self.zone[0][1]+self.zone[1][1] >= mp[1] )):
			if self.leftClick :
				self.clicked = True
				self.caption = self.name
			elif self.clicked and not self.leftClick :
				del self.caption
				return True
			else :
				self.hover = True
		else :
			del self.caption
			self.hover = False
			self.clicked = False
		return False

	def graphicUpdate(self):
		if self.clicked:
			self.displayActivatable({"image":self.imgdata["onclick"],"position":self.zone[0]})
		elif self.hover:
			self.displayActivatable({"image":self.imgdata["hov"],"position":self.zone[0]})
		else :
			self.displayActivatable({"image":self.imgdata["base"],"position":self.zone[0]})

	def __call__(self):
		self.graphicUpdate()
		return self.mouseover()

class Textzone(Graphics):
	"""docstring for Textzone"""

	instanceCount = 0

	def __init__(self, fontsize, coordinates, maxlength = 100, text = "Enter your text here"):

		Textzone.instanceCount+=1
		del self.name

		self.fontsize = fontsize
		self.coordinates = coordinates
		self.maxlength = maxlength
		self.textfont = pygame.font.Font(None, self.fontsize)
		self.focused = False
		self.hover = False
		self.text = ""
		self.textBuffer = ""
		self.base = text

		self.keylogger = []
		self.backspaceBuffer = 0
		self.rendered = False

		self.selected = ""
		#self.
		self.negative = (75,75,75,25)


	def write(self, text = ""):
		if text != "":
			self.text += text

		elif self.text == "" and not(self.rendered):
			if self.focused :
				self.display = self.textfont.render(" ", True, (255,255,255))
				self.rendered = True

			elif self.hover :
				self.display = self.textfont.render(self.base, True, (75,75,75))
				self.rendered = True

			elif not(self.focused):
				self.display = self.textfont.render(self.base, True, (150,150,150))
				self.rendered = True


		elif not(self.rendered):
			self.display = self.textfont.render(self.text, True, (0,0,0))
			self.rendered = True
		self.screen.blit(self.display, [self.coordinates[0],self.coordinates[1]+0.1*self.fontsize])

	def input(self):
		if self.focused :
			text = ""
			verrMaj = False
			keys = self.getKeys()
			if "Backspace" in keys and self.text!="":
				self.backspaceBuffer += 1
				if (self.backspaceBuffer % 4) == 0 :
					if self.textBuffer != "" :
						self.text = self.textBuffer[-1:] + self.text[:-1]
						self.textBuffer = self.textBuffer[:-1]
					else :
						self.text = self.text[:-1]
				if self.text == "":
					self.focused = False
				self.rendered = False
				return ""
			elif "Enter" in keys or "ENTER" in keys :
				self.focused = False
			for x in keys :
				if x == "VerrMaj":
						verrMaj = True
				elif not x in self.keylogger:
					self.keylogger.append(x)
					try :
						if len(x) == 1 and ("Maj" in keys or "Maj" in self.keylogger or verrMaj):
							if x in ["&","é","\"","\'","(","-","è","_","ç","à"]:
								text+=str((["&","é","\"","\'","(","-","è","_","ç","à"].index(x)+1)%10)
							elif x == ")" :
								text+="°"
							elif x == "=":
								text+="+"
							else :
								text+=x.upper()
						elif len(x) == 1 :
							text+=x.lower()
					except Exception as e:
						raise e
					else :
						self.rendered = False
			for x in self.keylogger:
				if not x in keys :
					self.keylogger.pop(self.keylogger.index(x))
			return text
		else :
			return ""

	def mouseover(self):
		mp = self.getMouse()
		if (( self.coordinates[0] <= mp[0] and self.coordinates[0]+(self.fontsize+1)*self.maxlength >= mp[0] ) and ( self.coordinates[1] <= mp[1] and self.coordinates[1]+self.fontsize*2 >= mp[1] )):
			if self.leftClick :
				self.focused = True
				self.rendered = False
			else :
				self.hover = True
				self.rendered = False
		elif self.hover :
			self.hover = False
			self.rendered = False
		elif self.leftClick :
			self.rendered = False
			self.focused = False

	def wrap(self,inp):
		if len(self.text)+len(inp) > self.maxlength :
			self.textBuffer += self.text[:self.maxlength-len(self.text)+len(inp)]
			self.text = self.text[len(self.text)+len(inp)-self.maxlength:]
		return inp


	def graphicUpdate(self):
		if self.selected != "": #work in progress
			size = self.textfont.size(self.selected)
			pygame.draw.rect(self.screen, self.negative,[self.coordinates[0],self.coordinates[1],size[0],size[1]])
		self.write(self.wrap(self.input()))
		if self.text == "" and self.focused :
			self.backspaceBuffer = 0


	def __call__(self):
		self.mouseover()
		self.graphicUpdate()
		if options["debug"] :
			#print("focus : {}, hov : {}".format(self.focused,self.hover))
			#print("rendering text at {}".format(self))
			#print(self.text)
			pass
		return self.textBuffer+self.text


######## Core


if __name__ == '__main__':
	print("kernel can't be launched\nNow searching for exe/bat/main files")
	files = [];path ="./"
	for file in os.listdir(path):
		if ".py" in file :
			print("found {} in {}".format(file,path))
			files.append(path+file)
	for x in files:
		if "main" in x.lower():
			print("Now starting {}".format(x))
			os.system("python -u {} -c {} -d".format(x,os.getcwd()))
			quit()

options = {
	"caption" : "Pygame kernel v"+__version__,
	"resolution" : [Graphics.screen_l,Graphics.screen_h],
	"helper" : "Pygame kernel v{v}\n".format(v=__version__) +
		"options :\n\n-c / --caption : << (use) -c caption >>\n sets a custom name for your pygame window\n" +
		"-r / --resolution : << (use) -r width height >>\n sets a custom resolutions for your pygame window\n" +
		"-i / --icon : << (use) -i filepath >>\n sets a custom icon for your pygame window\n" +
		"-d / --debug / -v / --verbose: << (use) -d\n sets dev/debug mode\n",
	"icon" : None,
	"debug" : False,
	"verbose" : False
}

for x in __system_args__:
	if "-c" == x or "--caption" == x :
		options["caption"] = __system_args__[__system_args__.index(x)+1]
	elif "-r" == x or "--resolution" == x :
		options["resolution"] = [int(__system_args__[__system_args__.index(x)+1]),int(__system_args__[__system_args__.index(x)+2])]
	elif "-i" == x or "--icon" == x :
		options["icon"] = __system_args__[__system_args__.index(x)+1]
	elif "-d" == x or "--debug" == x :
		options["debug"] = True
	elif "-v" == x or "--verbose" == x :
		options["verbose"] = True
	elif "-h" == x or "--help" == x :
		print(options["helper"])
		quit()