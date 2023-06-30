import pygame,os,gui,level

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions
	
def animation_loader(entity_name,animation_name,animation_frame_qty,scale):
	animation_frames_right = []
	animation_frames_left = []
	
	for i in range (0,animation_frame_qty):
		img_right = pygame.image.load(os.path.join('entityanimations',entity_name,animation_name,animation_name+'_'+str(i)+'.png'))
		animation_frames_right.append(img_right)
	
	for i in range (len(animation_frames_right)): #scales images properly
		animation_frames_right[i] = pygame.transform.scale(animation_frames_right[i],scale)
		
	for image in animation_frames_right: #flips images 
		flipped_image = pygame.transform.flip(image,True,False)
		animation_frames_left.append(flipped_image)	
		
	return animation_frames_right,animation_frames_left
	
class Slime:
	idle,holder = animation_loader('slime','idle',2,(32,32))
			
	for i in range (len(idle)):
		idle[i].set_colorkey((255,255,255))
		
	def __init__(self,x,y,size_x,size_y):
		self.index = 0
		self.x = x
		self.y = y
		self.size_x = size_x
		self.size_y = size_y
		self.jumping = False
		self.falling = True
		self.rect = pygame.Rect(self.x,self.y,self.size_x,self.size_y)
		self.vely = 0 
		self.counter = 0
		self.timer = 0
		self.dy = 0
		self.dx = 0
		
	def update(self,tile_rects,player):
		self.counter += 1 #counts to keep track of animation
		self.timer += 1
		if self.timer > 90: #makes slime only do its movements every tick and a half at most
			
			if self.jumping == False and self.falling == False: #if not jumping or falling, 
				self.dy = -8#slime jumps

				if (player.rect.x - self.rect.x) > 0:  #checks to see where the player is and has it move towards the player
					self.dx = 4
				else:
					self.dx = -4			
				
			self.timer = 0
			self.falling = True
			
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
		if self.counter + 1 >= 22:
			self.counter = 0
		screen.blit(self.idle[self.counter // 12],(self.rect.x-scroll[0],self.rect.y-scroll[1]))
		
	def do(self,screen,scroll,tile_rects,player):
		self.update(tile_rects,player)
		self.draw(screen,scroll)

class Player:
	idle_right,idle_left = animation_loader('player','idle',2,(39,60))
	walk_right,walk_left = animation_loader('player','run',6,(39,60))
	jump_right,jump_left = animation_loader('player','jump',5,(39,60))
	
	def __init__(self,x,y,size_x,size_y):
		self.index = 0
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.size_x = size_x
		self.size_y = size_y
		self.rect = pygame.Rect(self.x,self.y,self.size_x,self.size_y)
		self.vely = 0 
		self.animation_speed = 0.15
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

	def update(self,player_gui,tile_rects):

		self.dmg_detect_timer += 1
		self.regeneration_timer += 1
		
		k = pygame.key.get_pressed() #input for movement
		if k[pygame.K_SPACE] and not self.jumping:
			self.dy = -12
			self.jumping = True
			self.animation_speed = 0.1
			if self.direction == 1:
				self.animation = self.jump_right
			else:
				self.animation = self.jump_left
		if k[pygame.K_a]:
			self.dx = -5
			self.direction = -1
			self.animation_speed = 0.15
			if not self.jumping:
				self.animation = self.walk_left
		elif k[pygame.K_d]:
			self.dx = 5
			self.direction = 1
			self.animation_speed = 0.15
			if not self.jumping:
				self.animation = self.walk_right
		if k[pygame.K_a] == False and k[pygame.K_d] == False and not self.jumping:
			self.dx = 0
			self.animation_speed = 0.07
			if self.direction == 1:
				self.animation = self.idle_right
			else:
				self.animation = self.idle_left 
		
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
				self.dy = 0
				self.jumping = False
			if self.dy < 0:
				self.rect.top = tile.bottom
				self.dy= 0			
		
		self.vely = 0.6  #gravity
		self.dy += self.vely				
		if self.dy > 11:
			self.dy = 11
			
		if self.regeneration_timer == 360: #handles player regeneration
			self.hitpoints += 1
			self.regeneration_timer = 0
			if self.hitpoints >= self.max_hitpoints:
				self.hitpoints = self.max_hitpoints
			player_gui.hitpoints[self.hitpoints] = True
		
		# if self.dmg_detect_timer > 60: #detects collision with a slime and records damage to player
			# if self.rect.colliderect(slime.rect):
				# self.hitpoints -= 1
				# self.dmg_detect_timer = 0
				# pygame.mixer.Sound.play(player_dmg_sound)
				# player_gui.hitpoints[self.hitpoints+1] = False
					
	def draw(self,screen,scroll):	
		screen.blit(self.animation[int(self.frame_index)],(self.rect.x-scroll[0],self.rect.y-scroll[1]))

	def do(self,screen,scroll,player_gui,tile_rects):
		self.update(player_gui,tile_rects) 
		self.draw(screen,scroll)

class Spear:
	stab_right = pygame.image.load(os.path.join('weaponimages','wooden_spear.png'))
	stab_right = pygame.transform.scale(stab_right,(72,20))
	stab_right.set_colorkey((255,255,255))
	stab_left = pygame.transform.flip(stab_right,False,True)
	
	def __init__(self,player,size_x,size_y,direction):
		self.x = player.x
		self.y = player.y
		self.dx = 0
		self.dy = 0
		self.size_x = size_x
		self.size_y = size_y
		self.rect = pygame.Rect(self.x,self.y,size_x,size_y)
		self.type = 'wooden'
		self.direction = direction
		self.image = 0
		self.player = player
	def update(self,direction):
		print(self.x,self.y)
		if self.direction == -1:
			self.image = self.stab_right
		else:
			self.image = self.stab_left
	def draw(self,screen,scroll):
		screen.blit(self.image,(self.rect.x-scroll[0],self.rect.y-scroll[1]))
		
	def do(self,screen,scroll,direction):
		self.update(direction)
		self.draw(screen,scroll)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	