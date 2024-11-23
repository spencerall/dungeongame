import pygame,os,random
from PIL import Image

tile_size = 48

game_folder = os.path.dirname(__file__)#paths
tile_img_folder = os.path.join(game_folder, 'tiles')

class LoadTiles:
	def __init__(self,imageName):
		tile_rects = []
		self.imgLoad = pygame.image.load(os.path.join(tile_img_folder, imageName)) #.convert()
		self.imgScale = pygame.transform.scale(self.imgLoad, (tile_size, tile_size))

dirt_tile = LoadTiles('dirt_tile.png') #loads images
grass_tile = LoadTiles('grass_tile.png') 
rock_tile = LoadTiles('rock_tile.png')
		
class LevelModules:
	def __init__(self,biome,level_length):
		self.biome = biome
		self.module_index = 0
		self.module_img = 0
		self.module_qty = 4
		self.module_image_list = []
		self.level_length = level_length
		self.level_construct = []	
		self.level_image = None
		
	def level_constructor(self):
		for i in range(self.module_qty): #check how many modules there should be, open the images, and append them to a list
			self.module_img = Image.open(os.path.join(game_folder,'levelmodules','biome'+str(self.biome),'biome'+str(self.biome)+"-module"+str(i)+'.png'))
			self.module_img = self.module_img.convert('RGB')
			self.module_image_list.append(self.module_img)
				
		for i in range(self.level_length):
			self.level_construct.append(self.module_image_list[random.randint(1,self.module_qty-1)])
		#self.level_construct.append(self.module_image_list[0]) #End level with a solid chunk
		
		level_width = sum(module.width for module in self.level_construct)
		level_height = max(module.height for module in self.level_construct)
		
		self.level_image = Image.new('RGB', (level_width, level_height))
		
		module_offset = 0
		for module in self.level_construct:
			self.level_image.paste(module, (module_offset, 0))
			module_offset += module.width
		
		self.level_image.save('level_image.png')
		
	def construct_interpreter(self,screen,scroll):
		tile_rects = []

		width,height = self.level_image.size		

		for x in range(width):
			for y in range(height):
				r,g,b = self.level_image.getpixel((x,y))
				pixel = (r,g,b)
				if pixel == (125,124,124): #rock
					screen.blit(rock_tile.imgScale, ( x * tile_size - scroll[0], y * tile_size - scroll[1]))
				elif pixel == (106,190,48): #grass
					screen.blit(grass_tile.imgScale, ( x * tile_size - scroll[0], y * tile_size - scroll[1]))
				elif pixel == (143,86,59): #dirt
					screen.blit(dirt_tile.imgScale, ( x * tile_size - scroll[0], y * tile_size - scroll[1]))
				if pixel != (182,171,171): #anything but air					
					tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
		
		return tile_rects 
	
	def spawn_player_in_center(self, player):
    # Get the width and height of the level image (constructed map)
		level_width, level_height = self.level_image.size

    # Calculate the center of the level, accounting for player's size
		spawn_x = (level_width - player.rect.width) // 2
		spawn_y = (level_height - player.rect.height) // 2

    # Set the player's position to the center of the level
		player.rect.x = spawn_x
		player.rect.y = spawn_y
# class Backgrounds:
	# def __init__(self):	
		
# class EntityDistributor
	# def __init__(self):
		# self.frequency = 'integer'

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		