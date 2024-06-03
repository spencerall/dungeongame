import pygame,os,gui,level

game_folder = os.path.dirname(__file__)
soundfx_folder = os.path.join(game_folder,'audio','soundfx')
player_animations = os.path.join(game_folder,'playeranimations')

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions
	
def animation_loader(entity_name,animation_name,animation_frame_qty,scale):
	animation_frames_right = [] #defines lists for the images to be loaded into
	animation_frames_left = []
	
	for i in range (0,animation_frame_qty): #loops through all the images in the folder with the name of entity and the animation you specify and adds them to a list for when entity faces right
		img_right = pygame.image.load(os.path.join('entityanimations',entity_name,animation_name,animation_name+'_'+str(i)+'.png'))
		animation_frames_right.append(img_right) 
	
	for i in range (len(animation_frames_right)): #scales images properly
		animation_frames_right[i] = pygame.transform.scale(animation_frames_right[i],scale)
		
	for image in animation_frames_right: #flips images and adds them to a new, second list for when the entity faces left 
		flipped_image = pygame.transform.flip(image,True,False)
		animation_frames_left.append(flipped_image)
		
	return animation_frames_right,animation_frames_left #returns two lists of images: facing right and facing left images
	
class Slime:
	idle,holder = animation_loader('slime','idle',2,(32,32))
			
	for i in range (len(idle)):
		idle[i].set_colorkey((255,255,255))
		
	def __init__(self,x,y,size_x,size_y):
		self.index = 0
		self.jumping = False
		self.falling = True
		self.rect = pygame.Rect(x,y,size_x,size_y)
		self.vely = 0
		self.counter = 0
		self.timer = 0
		self.dy = 0
		self.dx = 0
		self.hitpoints = 10
		self.animation = self.idle
		self.animation_frame_qty = len(self.animation)
		self.animation_speed = 0.08
		self.frame_index = 0
		self.counter = 0
	def update(self,tile_rects,player):		
		
		self.counter += 1
		if self.counter > 80:
			self.counter =0
			
			if self.jumping == False and self.falling == False: #if not jumping or falling, 
				self.dy = -8#slime jumps

				if (player.rect.x - self.rect.x) > 0:  #checks to see where the player is and has it move towards the player
					self.dx = 4
				else:
					self.dx = -4			
					
				self.falling = True
			
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.animation):
			self.frame_index = 0
			
		self.rect.x += self.dx #collisions for movement on x axis
		collisions = collision_test(self.rect,tile_rects)
		for tile in collisions: 
			if self.dx > 0:
				self.rect.right = tile.left
			if self.dx < 0:
				 self.rect.left = tile.right		
		self.rect.y += self.dy #collisions for movemnt on y axis
		collisions = collision_test(self.rect,tile_rects)
		for tile in collisions:
			if self.dy > 0:
				self.rect.bottom  = tile.top
				self.vely = 0
				self.falling = False
				self.jumping = False
				self.dx = 0				
			if self.dy <= 0:
				self.rect.top = tile.bottom
				self.dy= 0
				self.falling = True
		
		self.vely = 0.6  #gravity
		self.dy += self.vely				
		if self.dy > 9:
			self.dy = 9			
		
	def draw(self,screen,scroll):
		screen.blit(self.animation[int(self.frame_index)],(self.rect.x-scroll[0],self.rect.y-scroll[1]))
		pygame.draw.rect(screen,(255,255,255),self.rect.move(scroll[0]*-1,scroll[1]*-1),2)#hitbox for debugging
		
	def do(self,screen,scroll,tile_rects,player):
		self.update(tile_rects,player)
		self.draw(screen,scroll)

class Player:
	idle_right,idle_left = animation_loader('player','idle',2,(39,60))
	walk_right,walk_left = animation_loader('player','run',6,(39,60))
	jump_right,jump_left = animation_loader('player','jump',5,(39,60))
	stab_right,stab_left = animation_loader('player','jump',4,(39,60))
	
	def __init__(self,x,y,size_x,size_y):
		self.index = 0
		self.rect = pygame.Rect(x,y,size_x,size_y)
		self.vely = 0.6
		self.dx = 0
		self.dy = 0
		self.animation_speed = 0.1
		self.frame_index = 0
		self.direction = 1
		self.max_hitpoints = 10
		self.hitpoints = 10
		self.dmg_detect_timer = 0
		self.regeneration_timer = 0
		self.jumping = False
		self.animation = self.idle_right
		self.animation_frame_qty = len(self.animation)
		self.frame_index = 0
		self.damaged = False
		
	def update(self,player_gui,tile_rects,slime):
		self.damaged = False
		self.dmg_detect_timer += 1
		self.regeneration_timer += 1
		
		k = pygame.key.get_pressed() #input for movement
		m = pygame.mouse.get_pressed(num_buttons=3)
		
		if k[pygame.K_SPACE] and not self.jumping and not m[0]:
			self.dy = -15
			self.jumping = True

			if self.direction == 1:
				self.animation = self.jump_right
			else:
				self.animation = self.jump_left	
		if k[pygame.K_d] and k[pygame.K_a]:
			self.dx = 0		
			if self.direction == 1:
				self.animation = self.idle_right
			else:
				self.animation = self.idle_left
			self.animation_speed = 0.1
			
		elif k[pygame.K_d]:
			self.direction = 1
			self.dx = 5
			self.animation = self.walk_right
			self.animation_speed = 0.2
		
		elif k[pygame.K_a]:
			self.direction = -1
			self.dx = -5
			self.animation = self.walk_left	
			self.animation_speed = 0.2
				
		if k[pygame.K_a] == False and k[pygame.K_d] == False and not self.jumping:
			self.dx = 0
			self.animation_speed = 0.1
			
			if self.direction == 1:
				self.animation = self.idle_right
			else:
				self.animation = self.idle_left
				
		if m[0] == True:
			if self.direction == 1:
				self.animation = self.stab_right
			else:
				self.animation = self.stab_left
				
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.animation):
			self.frame_index = 0			
		
		self.rect.x += self.dx #collisions for movement on x axis
		collisions = collision_test(self.rect,tile_rects)
		for tile in collisions: 
			if self.dx > 0:
				self.rect.right = tile.left 
			if self.dx < 0:
				 self.rect.left = tile.right
		
		self.rect.y += self.dy #collisions for movement on y axis
		collisions = collision_test(self.rect,tile_rects)
		for tile in collisions:
			if self.dy > 0:
				self.rect.bottom  = tile.top
				self.dy = 0
				self.dx = 0
				self.jumping = False
			if self.dy < 0:
				self.rect.top = tile.bottom
				self.dy= 0			
		
		self.dy += self.vely#gravity				
		if self.dy > 11:
			self.dy = 11
			
		if self.regeneration_timer == 360: #handles player regeneration
			self.hitpoints += 1
			self.regeneration_timer = 0
			if self.hitpoints >= self.max_hitpoints:
				self.hitpoints = self.max_hitpoints
			player_gui.hitpoints[self.hitpoints] = True
		
		if self.dmg_detect_timer > 60: #detects collision with a slime and records damage to player
			if self.rect.colliderect(slime.rect):
				self.damaged = True
				self.hitpoints -= 1
				self.dmg_detect_timer = 0
				#pygame.mixer.Sound.play(self.player_dmg_sound)
				player_gui.hitpoints[self.hitpoints+1] = False
		
	def draw(self,screen,scroll):	
		screen.blit(self.animation[int(self.frame_index)],(self.rect.x-scroll[0],self.rect.y-scroll[1]))
		hitbox = pygame.draw.rect(screen,(255,255,255),self.rect.move(scroll[0]*-1,scroll[1]*-1),2) #hitbox for debugging
		
	def do(self,screen,scroll,player_gui,tile_rects,slime):
		self.update(player_gui,tile_rects,slime) 
		self.draw(screen,scroll)

# class StabWeapon:
	# stab_right,stab_left = animation_loader('spear','stab',1,(130,25)) #loads image to be used in animation
	# stab_right[0].set_colorkey((255,255,255))
	# stab_left[0].set_colorkey((255,255,255))
	
	# def __init__(self,player,scroll):
		# self.player = player
		# self.type = 'wooden'
		# self.direction = player.direction
		# self.animation = self.stab_right[0]
		# self.frame_index = 0
		# self.animation_speed = 0.05
		# self.rect =self.animation.get_rect(topleft=(self.player.rect.center[0]-scroll[0]-65,self.player.rect.center[1]-scroll[1]))
		# self.dmg = 2
		# self.visible = False
		
	# def update(self,player,scroll,mob_rects):
		# self.direction = player.direction
		# self.animation = self.stab_right if self.direction == 1 else self.stab_left #chooses whether the image should be facing left or right
		
		# self.frame_index += self.animation_speed #handles how many frames a given image should show for
		# if self.frame_index >= len(self.animation):
			# self.frame_index = 0
			# self.visible = False
		
		# self.rect =self.animation[0].get_rect(topleft=(self.player.rect.center[0]-scroll[0]-65,self.player.rect.center[1]-scroll[1])) #updates the spear's rect's location
		
		# #print(self.rect)
		# #print(mob_rects[0])
		# for rects in mob_rects:
			# if self.rect.colliderect(rects):
				# print(rects)
				# print(self.rect)
			# else:
				# pass

	# def draw(self,screen,scroll): #places image on screen relative to player's position
		# if self.visible:
			# screen.blit(self.animation[int(self.frame_index)],(self.player.rect.center[0]-scroll[0]-65,self.player.rect.center[1]-scroll[1])) 
			# pygame.draw.rect(screen,(255,255,255),self.rect,2) #hitbox for debugging
			
	# def do(self,screen,scroll,player,slime): #updates and draws the spear in one command
		# self.update(player,scroll,slime)
		# self.draw(screen,scroll)