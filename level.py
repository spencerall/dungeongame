import pygame,os,random,noise,time
from PIL import Image

random.seed(random.randint(0,10000))

tile_size = 48
chunk_size = 8

game_folder = os.path.dirname(__file__)#paths
tile_img_folder = os.path.join(game_folder,'tiles')
environment_folder = os.path.join(game_folder,'environment')

seed_offset = random.uniform(0,10000)

def load_tiles(path,image_name,colorkey):
	loaded_image = pygame.image.load(os.path.join(path, image_name))	
	scaled_image = pygame.transform.scale(loaded_image, (tile_size, tile_size))
	if colorkey:
		scaled_image.set_colorkey((255,255,255))

	return scaled_image
	
dirt_tile = load_tiles(tile_img_folder,'dirt_tile.png',False) #loads images
grass_tile = load_tiles(tile_img_folder,'grass_tile.png',False) 
rock_tile = load_tiles(tile_img_folder,'rock_tile.png',False)
rock_0 = load_tiles(environment_folder,'rock_0.png',True)
rock_1 = load_tiles(environment_folder,'rock_1.png',True)
rock_2 = load_tiles(environment_folder,'rock_2.png',True)
rock_3 = load_tiles(environment_folder,'rock_3.png',True)


tile_index = {1:grass_tile,
				2:dirt_tile,
				3:rock_tile,
				4:rock_0,
				5:rock_1,
				6:rock_2,
				7:rock_3,}
		
def generate_chunk (x,y):
	chunk_data = []
	for y_pos in range (chunk_size):
		for x_pos in range (chunk_size):
			target_x = (x * chunk_size + x_pos)
			target_y = (y * chunk_size + y_pos)
			tile_type = 0 #nothing
			height = int(noise.pnoise1((target_x + seed_offset)* 0.08,repeat = 9) * 5)
			if target_y > 8 - height+2:
				tile_type = 3 #dirt
			elif target_y == 8 - height:
				tile_type = 1 #grass
			elif target_y in range((8-height),(8-height+3)):
				tile_type = 2
			elif target_y == 8 - height - 1: #random rock scenery
				if random.randint(1,5) == 1:
					tile_type = random.randint(4,7)
			if tile_type != 0:
				chunk_data.append([[target_x,target_y],tile_type])
	return chunk_data
		
# class Backgrounds:
	# def __init__(self):	
		
# class EntityDistributor
	# def __init__(self):
		# self.frequency = 'integer'

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		