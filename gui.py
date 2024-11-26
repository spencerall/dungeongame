import pygame, os, pygame_gui, sys
		
class PlayerGui:		
	def __init__(self,health_x,health_y,hotbar_x,hotbar_y,screen):
		self.health_x = health_x 
		self.health_y = health_y
		self.hotbar_x = hotbar_x
		self.hotbar_y = hotbar_y
		self.show_inventory = False
		self.hitpoints = {1:True,2:True,3:True,4:True,5:True,6:True,7:True,8:True,9:True,10:True}
		self.hotbar = {1:True,2:False,3:False,4:False}
		self.hotbar_index = 1
		self.holding = [None,0] 
		
		rows = ['a', 'b', 'c', 'd', 'e']	#Generates a dictionary organized like this:
		cols = [1, 2, 3, 4]					#self.inv_rects = {cell_name:(rect,[contents,quantity])}
		self.inv_cells = {}					#for example, self.inv_rects = {a1:(pygame.Rect(x,y,64,64),['wood',10])}											#a-e and 1,4 (20 different key/value pairs)
		for row in rows:					
			for col in cols:
				key = f'{row}{col}'
				rect_x = self.hotbar_x + (col - 1) * 64
				rect_y = self.hotbar_y - (256 - (rows.index(row) * 64))
				self.inv_cells[key] = [pygame.Rect(rect_x, rect_y, 64, 64), [None, 0]]				
		
		self.ui_images = [pygame.image.load(os.path.join('ui','emptyheart.png')),
				pygame.image.load(os.path.join('ui','heart.png')),
				pygame.image.load(os.path.join('ui','invborder.png')).convert_alpha(),
				pygame.image.load(os.path.join('ui','invborder_selected.png')).convert_alpha(),
				pygame.image.load(os.path.join('ui','inventory.png')).convert_alpha()]
		for i in range (len(self.ui_images)):
			self.ui_images[i].set_colorkey((255,255,255))

		self.ui_images[2] = pygame.transform.scale(self.ui_images[2],(64,64))
		self.ui_images[3] = pygame.transform.scale(self.ui_images[3],(64,64))
		self.ui_images[4] = pygame.transform.scale(self.ui_images[4],(256,256))
	
	def update(self,screen):
		k = pygame.key.get_pressed()
				
		if k[pygame.K_1]:
			self.hotbar_index = 1		
		elif k[pygame.K_2]:
			self.hotbar_index = 2			
		elif k[pygame.K_3]:
			self.hotbar_index = 3			
		elif k[pygame.K_4]:
			self.hotbar_index = 4
	
	def display_icons(self,screen):
		for cell in self.inv_cells:																				#loop through inventory cells
			if self.inv_cells[cell][1][0] is not None:																#if there's something in it
				img = pygame.image.load(os.path.join('ui','invicons',f'inv_{self.inv_cells[cell][1][0]}.png'))	#load image for what's in there
				# img = pygame.transform.scale(img,(32,32))
				# img = img.set_colorkey((255,255,255))
				img_rect = img.get_rect()																#get a rect for the purposes of positioning
				img_rect.center = self.inv_cells[cell][0].center													#center the image's rect in the center of the cell
				
				font = pygame.font.Font(None,16)										#load the font
				qty = font.render(str(self.inv_cells[cell][1][1]),True,(0,0,0))						#write quantity in that font
					
				screen.blit(img,(img_rect.centerx,img_rect.centery))					#draw the icon in the middle of the appropriate cell
				screen.blit(qty,(img_rect.centerx+10,img_rect.centery+10))				#draw the quantity relative to the icon
				
	def draw(self,screen):
		if self.show_inventory == True:#Displays player's inventory
			screen.blit(self.ui_images[4],(self.hotbar_x,self.hotbar_y-256))
			
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
	
	def do(self,screen):
		self.update(screen)
		self.display_icons(screen)
		self.draw(screen)	
			
class MenuManager:
	def __init__(self,screen,width,height,menus_info_dict):
		self.menus_dict = {}
		for menu_name, menu_buttons_list in menus_info_dict.items():
			menu = Menu(screen, width, height, menu_name, menu_buttons_list)
			self.menus_dict[menu_name] = menu
			
		self.current_menu_name = None
	def set_current_menu(self, menu_name):
		self.current_menu_name = menu_name
		if self.current_menu_name is None:
			return
		self.current_menu = self.menus_dict[self.current_menu_name]
	def handle_event(self,event):
		if self.current_menu_name is None:
			return
		action = self.current_menu.handle_event(event)
		return action
	def draw(self):
		if self.current_menu_name is None:
			return
		self.current_menu.draw()		

class Menu:
	def __init__(self,screen,width,height,menu_name,button_names_list):
		self.menu_name = menu_name
		self.buttons_list = []
		button_qty = len(button_names_list)
		x = (width - 450) // 2
		if self.menu_name == 'GameOver':
			y = 475
		else:
			y = 50
		y_spacing = 125
		for button_name in button_names_list:
			button = Button(screen,button_name,(x,y),(450,75))
			self.buttons_list.append(button)
			y = y + y_spacing
		
	def handle_event(self,event):
		for button in self.buttons_list:
			action = button.handle_event(event)
			if action is not None:
				return action
	
	def draw(self):
		for button in self.buttons_list:
			button.draw()

class Button:
	def __init__(self,screen,button_name,position,scale):
		self.screen = screen
		self.position = position
		self.scale = scale
		self.button_name = button_name
		self.image = pygame.image.load(os.path.join('ui',self.button_name+'button.png')).convert()
		self.image = pygame.transform.scale(self.image,self.scale)
		self.image.set_colorkey((255,255,255))
		self.rect = pygame.Rect(self.position[0],self.position[1],scale[0],scale[1])
		self.collision = False
		self.brightener = pygame.Surface(scale)
		self.brightener.fill((20,20,20))

	def handle_event(self,event):
		if event.type == pygame.MOUSEMOTION:
			mouse_pos = event.pos
			if self.rect.collidepoint(mouse_pos):
				self.collision = True
			else:
				self.collision = False
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if self.collision:
				return self.button_name
				
		return None
			
	def draw(self):
		self.screen.blit(self.image,self.rect)
		if self.collision:
			self.screen.blit(self.brightener,self.rect,special_flags=pygame.BLEND_RGBA_ADD)

