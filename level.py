import pygame,os

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
		
def loadMap(path):
	f = open(path +'.txt','r')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map
	
game_map = loadMap('map')	

def drawMap(screen,scroll):
	tile_rects = []
	y = 0
	for row in game_map: #iterates through the list which holds the data for the level map
		x = 0
		for tile in row: #checks to see what data value each tile has then places the tile accordingly
			if tile == '1':
				screen.blit(dirt_tile.imgScale, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
			if tile == '2':
				screen.blit(grass_tile.imgScale, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
			if tile == '3':
				screen.blit(rock_tile.imgScale, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
			if tile != '0':	
				tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
			x += 1
		y += 1
	return tile_rects