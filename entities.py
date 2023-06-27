import pygame,os,gui,level

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions
	
class Slime:

	idle = [pygame.image.load(os.path.join('entityanimations','slime','idle','idle_0.png')),
			pygame.image.load(os.path.join('entityanimations','slime','idle','idle_1.png'))]
			
	for i in range (len(idle)):
		idle[i] = pygame.transform.scale(idle[i],(32,32))
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
		
	def update(self):
		self.counter += 1 #counts to keep track of animation
		self.timer += 1
		if self.timer > 90: #makes slime only do its movements every tick and a half at most
			
			if self.jumping == False and self.falling == False: #if not jumping or falling, 
				self.dy = -10#slime jumps

				if (player.rect.x - self.rect.x) > 0:  #checks to see where the player is and has it move towards the player
					self.dx = 5
				else:
					self.dx = -5				
				
			self.timer = 0
			self.falling = True
			
		self.rect.x += self.dx #collisions for movement on x axis
		collisions = collision_test(self.rect,tile_rects)
		for tile in collisions: 
			if self.dx > 0:
				self.rect.right = tile.left
				self.dx = 0
			if self.dx < 0:
				 self.rect.left = tile.right
				 self.dx = 0
		
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
		
	def do(self,screen,scroll):
		self.update()
		self.draw(screen,scroll)

class Player:
	walk_right = [pygame.image.load(os.path.join('playeranimations','run','run_0.png')),
				pygame.image.load(os.path.join('playeranimations','run','run_1.png')),
				pygame.image.load(os.path.join('playeranimations','run','run_2.png')),
				pygame.image.load(os.path.join('playeranimations','run','run_3.png')),
				pygame.image.load(os.path.join('playeranimations','run','run_4.png')),
				pygame.image.load(os.path.join('playeranimations','run','run_5.png'))]
	walk_left = []
	for i in range (len(walk_right)):
		walk_right[i] = pygame.transform.scale(walk_right[i],(39,60))
		
	for image in walk_right:
		flipped_image = pygame.transform.flip(image,True,False)
		walk_left.append(flipped_image)
		
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
		self.counter = 0
		self.direction = 1
		self.max_hitpoints = 10
		self.hitpoints = 10
		self.dmg_detect_timer = 0
		self.regeneration_timer = 0
		self.jumping = False

	def update(self,player_gui):

		walk_cooldown = 5
		self.dmg_detect_timer += 1
		self.regeneration_timer += 1
		
		k = pygame.key.get_pressed() #input for movement
		if k[pygame.K_SPACE] and not self.jumping:
			self.dy = -12
			self.jumping = True
		if k[pygame.K_a]:
			self.dx = -5
			self.counter += 1
			self.direction = -1
		elif k[pygame.K_d]:
			self.dx = 5
			self.counter += 1
			self.direction = 1
		if k[pygame.K_a] == False and k[pygame.K_d] == False:
			self.counter = 0
			self.index = 0
			self.dx = 0
		
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
		if self.counter + 1 >= 60:
			self.counter = 0		
		if self.direction == -1:
			screen.blit(self.walk_left[self.counter // 10],(self.rect.x-scroll[0],self.rect.y-scroll[1]))
			self.counter += 1
		if self.direction == 1:
			screen.blit(self.walk_right[self.counter // 10],(self.rect.x-scroll[0],self.rect.y-scroll[1]))
			self.counter += 1
		
	def do(self,screen,scroll,player_gui):
		self.update(player_gui) 
		self.draw(screen,scroll)		