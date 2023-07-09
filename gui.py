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
	 	
	def __init__(self,x,y):
		self.x = x
		self.y = y			
		self.main_menu_keys = ['singleplayer','multiplayer','settings','quit']
		self.pause_menu_keys = ['mainmenu','settings','quit']
		self.type = None
		
	def button_function(self):
		button_rects = []
		buttons_pressed = {'mainmenu':False,
						'settings':False,
						'quit':False,
						'singleplayer':False,
						'multiplayer':False}						
		pos = pygame.mouse.get_pos()
		
		for key in self.pause_menu_keys:
			rects = pygame.Surface.get_rect(self.menu_images[key])
			button_rects.append(rects)

		if self.type == 'pause':
			for rects in button_rects:
				if rects.collidepoint(pos):
					print(buttons_pressed[rects])
						
	def draw(self,screen,y):	
		if self.type == 'main':
			for key in self.main_menu_keys:		
				screen.blit(self.menu_images[key],(self.x,self.y))
				self.y += 150
			self.y = y
			
		if self.type == 'pause':
			for key in self.pause_menu_keys:		
				screen.blit(self.menu_images[key],(self.x,self.y))
				self.y += 150
			self.y = y
			
	def do(self,screen,y):
		self.button_function()
		self.draw(screen,y)
		
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
				
	def update(self,screen,main_menu,mouse_pos,stab_weapon):
		k = pygame.key.get_pressed()
		
		for event in pygame.event.get():	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_e: #toggles inventory view
					self.show_inventory = not self.show_inventory
					
				if event.key== pygame.K_ESCAPE and main_menu.type == None:#toggles menu
					main_menu.type = 'pause'
				elif event.key == pygame.K_ESCAPE and main_menu.type == 'pause':
					main_menu.type = None
				
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
					stab_weapon.visible = True				
					if main_menu.type == 'pause':
						main_menu.button_function()
						
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

# class Button():
	# def __init__(self,x,y,image,scale):
		# width = image.get_width()
		# height = image.get_height()
		# self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		# self.rect = self.image.get_rect()
		# self.rect.topLeft = (x,y)
		# self.clicked = False
		
	# def draw(self,surface):
		# action = False
		# pos = pygame.mouse.get_pos()
		
		# if self.rect.collidepoint(pos):
			# if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
			# self.clicked = True
			# action = True
			
		# if pygame.mouse.get_pressed()[0] == 0:
			# self.clicked = False
		
		# surface.blit(self.image, (self.rect.x,self.rect.y))
		
		# return action
