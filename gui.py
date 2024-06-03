import pygame, os, pygame_gui, sys
class Menu: #need to add a save functionality and button. save and quit for example
	menu_images = {'singleplayer':pygame.image.load(os.path.join('ui','singleplayerbutton.png')),
				'multiplayer':pygame.image.load(os.path.join('ui','multiplayerbutton.png')),
				'settings':pygame.image.load(os.path.join('ui','settingsbutton.png')),
				'quit':pygame.image.load(os.path.join('ui','quitbutton.png')),
				'save':pygame.image.load(os.path.join('ui','savebutton.png')),
				'mainmenu':pygame.image.load(os.path.join('ui','mainmenubutton.png'))}
				
	for key in menu_images:
		menu_images[key] = pygame.transform.scale(menu_images[key],(600,100))
		menu_images[key].set_colorkey((255,255,255))

	def __init__(self,width,height):
		self.x = width
		self.y = height			
		self.main_menu_keys = ['singleplayer','multiplayer','settings','quit']
		self.pause_menu_keys = ['mainmenu','settings','quit']
		self.type = None
		self.button_rects = []
		self.buttonqty = 1
		self.clicked = False		

			
	def rect_distributor(self,screen):
		if self.type == 'pause':
			for key in self.pause_menu_keys: #creates and stores all the rects of the buttons in a list
				rects = pygame.Surface.get_rect(self.menu_images[key])
				self.button_rects.append(rects)

		elif self.type == 'main':
			for key in self.main_menu_keys: #creates and stores all the rects of the buttons in a list
				rects = pygame.Surface.get_rect(self.menu_images[key])
				self.button_rects.append(rects)
				
			
			spacer = 50			
			for rect in self.button_rects:
				rect.center = ((self.x/2),(self.y+spacer))
				spacer += 150
				pygame.draw.rect(screen,(255,255,255),rect,2) #debugging box for menu rects

	def button_manager(self):		
		buttons_pressed = {'mainmenu':False,
						'settings':False,
						'quit':False,
						'singleplayer':False,
						'multiplayer':False}						
		pos = pygame.mouse.get_pos()

		if self.type == 'pause':
			self.buttonqty = len(self.pause_menu_keys) + 2	#determines vertical distribution of buttons
			
			for rect in self.button_rects:
				if rect.collidepoint(pos) and self.clicked:
					rect_index = self.button_rects.index(rect) #detects which rect on the menu is clicked					
					if rect_index == 0: 
						buttons_pressed['main_menu'] = True
					elif rect_index == 1:
						buttons_pressed['settings'] = True
					elif rect_index == 2:
						buttons_pressed['quit'] = True
					
			self.button_rects = [] #wipes button rects for future loops
			
		if self.type == 'main':
			self.buttonqty = len(self.main_menu_keys) + 2 #determines vertical distribution of buttons
			
			for rect in self.button_rects:
				if rect.collidepoint(pos) and self.clicked:
					rect_index = self.button_rects.index(rect) #detects which rect on the menu is clicked					
					if rect_index == 0: 
						buttons_pressed['singleplayer'] = True
					elif rect_index == 1:
						buttons_pressed['multiplayer'] = True
					elif rect_index == 2:
						buttons_pressed['settings'] = True
					elif rect_index == 3:
						buttons_pressed['quit'] = True
			
		self.y = self.y/self.buttonqty #sets height for the first button 		
		self.clicked = False #resets self.clicked every loop so that it doesn't stay true after clicking
		
		if buttons_pressed['mainmenu'] == True: #This block of code handles the functions of all the buttons
			pass
		if buttons_pressed['settings'] == True:
			pass
		if buttons_pressed['quit'] == True:
			pygame.quit()
			sys.exit()
		if buttons_pressed['singleplayer'] == True:
			pass
		if buttons_pressed['multiplayer'] == True:
			pass
				
	def draw(self,screen,height):
	
		if self.type == 'main':
			for key in self.main_menu_keys:		
				screen.blit(self.menu_images[key],((self.x-600)/2,self.y))
				self.y += 150
			self.y = height
			
		if self.type == 'pause':
			for key in self.pause_menu_keys:
				screen.blit(self.menu_images[key],((self.x-600)/2,self.y))
				self.y += 150
			self.y = height
			
	def do(self,screen,height):
		self.button_manager()
		self.rect_distributor(screen)
		self.draw(screen,height)
		
class PlayerGui:
	ui_images = [pygame.image.load(os.path.join('ui','emptyheart.png')),
				pygame.image.load(os.path.join('ui','heart.png')),
				pygame.image.load(os.path.join('ui','invborder.png')),
				pygame.image.load(os.path.join('ui','invborder_selected.png')),
				pygame.image.load(os.path.join('ui','inventory.png'))]
	for i in range (len(ui_images)):
		ui_images[i].set_colorkey((255,255,255))
	ui_images[2] = pygame.transform.scale(ui_images[2],(64,64))
	ui_images[3] = pygame.transform.scale(ui_images[3],(64,64))
	ui_images[4] = pygame.transform.scale(ui_images[4],(256,256))
		
	def __init__(self,health_x,health_y,hotbar_x,hotbar_y):
		self.health_x = health_x 
		self.health_y = health_y
		self.hotbar_x = hotbar_x
		self.hotbar_y = hotbar_y
		self.show_inventory = False
		self.hitpoints = {1:True,2:True,3:True,4:True,5:True,6:True,7:True,8:True,9:True,10:True}
		self.hotbar = {1:True,2:False,3:False,4:False}
		self.hotbar_index = 1
		self.inv_rects = {'a1':pygame.Rect(self.hotbar_x,self.hotbar_y-256,64,64),
						'a2':pygame.Rect(self.hotbar_x+64,self.hotbar_y-256,64,64),
						'a3':pygame.Rect(self.hotbar_x+128,self.hotbar_y-256,64,64),
						'a4':pygame.Rect(self.hotbar_x+192,self.hotbar_y-256,64,64),
						'b1':pygame.Rect(self.hotbar_x,self.hotbar_y-192,64,64),
						'b2':pygame.Rect(self.hotbar_x+64,self.hotbar_y-192,64,64),
						'b3':pygame.Rect(self.hotbar_x+128,self.hotbar_y-192,64,64),
						'b4':pygame.Rect(self.hotbar_x+192,self.hotbar_y-192,64,64),
						'c1':pygame.Rect(self.hotbar_x,self.hotbar_y-128,64,64),
						'c2':pygame.Rect(self.hotbar_x+64,self.hotbar_y-128,64,64),
						'c3':pygame.Rect(self.hotbar_x+128,self.hotbar_y-128,64,64),
						'c4':pygame.Rect(self.hotbar_x+192,self.hotbar_y-128,64,64),
						'd1':pygame.Rect(self.hotbar_x,self.hotbar_y-64,64,64),
						'd2':pygame.Rect(self.hotbar_x+64,self.hotbar_y-64,64,64),
						'd3':pygame.Rect(self.hotbar_x+128,self.hotbar_y-64,64,64),
						'd4':pygame.Rect(self.hotbar_x+192,self.hotbar_y-64,64,64)}
				
	def update(self,screen,main_menu_inst,mouse_pos):
		k = pygame.key.get_pressed()
		
		for event in pygame.event.get():	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_e: #toggles inventory view
					self.show_inventory = not self.show_inventory
					
				if event.key== pygame.K_ESCAPE and main_menu_inst.type == None:#toggles menu
					main_menu_inst.type = 'pause'
				elif event.key == pygame.K_ESCAPE and main_menu_inst.type == 'pause':
					main_menu_inst.type = None
					
			if event.type == pygame.MOUSEBUTTONDOWN:	
				if event.button == 5: #detects scrolling up
					if self.hotbar_index < 4:
						self.hotbar[self.hotbar_index] = False 
						self.hotbar_index += 1
						self.hotbar[self.hotbar_index] = True
					else:
						self.hotbar[self.hotbar_index] = False
						self.hotbar_index = 1
						self.hotbar[self.hotbar_index] = True
						
				elif event.button == 4: #detects scrolling down
					if self.hotbar_index > 1: 
						self.hotbar[self.hotbar_index] = False
						self.hotbar_index -= 1
						self.hotbar[self.hotbar_index] = True	
					else:
						self.hotbar[self.hotbar_index] = False
						self.hotbar_index = 4
						self.hotbar[self.hotbar_index] = True
						
				elif event.button == 1: #detects left click
					if self.show_inventory == True: #detects where in inventory the player is clicking.
						for rects in self.inv_rects:
							if self.inv_rects[rects].collidepoint(mouse_pos):
								pass #interact with inventory						
					
					if main_menu_inst.type == 'pause':
						main_menu_inst.clicked = True
						
				elif event.button == 3:#for future right click functionality
					pass
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		if k[pygame.K_1]:
			self.hotbar_index = 1
		
		elif k[pygame.K_2]:
			self.hotbar_index = 2
			
		elif k[pygame.K_3]:
			self.hotbar_index = 3
			
		elif k[pygame.K_4]:
			self.hotbar_index = 4
			
		for i in range(10): 
			if self.hitpoints[i+1] == True: #checks to see if the player has this heart and then blits a full heart if true
				screen.blit(self.ui_images[1],(self.health_x,25))				
			else:
				screen.blit(self.ui_images[0],(self.health_x,25)) #if player does not have that heart, blits empty heart
			self.health_x += 27 #changes how far away hearts are from one another
		self.health_x = 25 #keeps ui from moving on the screen
		
		for i in range(1,5): #Displays player's hotbar
			if i == self.hotbar_index:
				screen.blit(self.ui_images[3],(self.hotbar_x, self.hotbar_y))
			else:
				screen.blit(self.ui_images[2],(self.hotbar_x, self.hotbar_y))
			self.hotbar_x += 64
		self.hotbar_x = 25 #keeps ui from moving on the screen
				
		if self.show_inventory == True:#Displays player's inventory
			screen.blit(self.ui_images[4],(self.hotbar_x,self.hotbar_y-256))