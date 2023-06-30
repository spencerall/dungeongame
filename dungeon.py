import pygame, os, gui, level
import entities as e			

WIDTH = 1080#Useful constants
HEIGHT = 720
FPS = 60

game_folder = os.path.dirname(__file__)#paths

music_folder = os.path.join(game_folder,'audio','music')
player_animations = os.path.join(game_folder,'playeranimations')
soundfx_folder = os.path.join(game_folder,'audio','soundfx')

pygame.init() #starts pygame
pygame.mixer.init() #starts sound mixer
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates window 
pygame.display.set_caption("Video Game") #names window
clock = pygame.time.Clock() #starts clock

#load sounds
pygame.mixer.music.load(os.path.join(music_folder,'ambient.mp3'))
player_dmg_sound = pygame.mixer.Sound(os.path.join(soundfx_folder,'playerdmg.wav'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

player = e.Player(WIDTH/2,HEIGHT/5,39,60)#Instantiates player
slime = e.Slime(WIDTH/3,HEIGHT/5,32,32)#Instantiates Slime
player_gui = gui.Player_gui(64,64,25,657)#Instantiates player gui
spear = e.Spear(player,26,5,1)#instantiates spear

scroll = [0,0]

running = True #game loop
while running:
	clock.tick(FPS)
	screen.fill((140,209,255))		
	
	scroll[0] += (player.rect.x-scroll[0]-500)/10
	scroll[1] += (player.rect.y-scroll[1]-300)/10
	
	tile_rects = level.drawMap(screen,scroll)

	player.do(screen,scroll,player_gui,tile_rects)	#updates and draws player
	slime.do(screen,scroll,tile_rects,player) #updates and draws slime
	player_gui.update(screen) #updates and draws hitpoints bar, player's hotbar, and inventory
	
	
	mouse_pos = pygame.mouse.get_pos()
	#print(mouse_pos)
	for event in pygame.event.get():
	
		if event.type == pygame.KEYDOWN:#toggles inventory view
			if event.key == pygame.K_e:
				player_gui.show_inventory = not player_gui.show_inventory
			
		if event.type == pygame.MOUSEBUTTONDOWN:
		
			if event.button == 5: #detects scrolling up
				if player_gui.hotbar_index < 4:
					player_gui.hotbar[player_gui.hotbar_index] = False 
					player_gui.hotbar_index += 1
					player_gui.hotbar[player_gui.hotbar_index] = True
				else:
					player_gui.hotbar[player_gui.hotbar_index] = False
					player_gui.hotbar_index = 1
					player_gui.hotbar[player_gui.hotbar_index] = True
					
			if event.button == 4: #detects scrolling down
				if player_gui.hotbar_index > 1: 
					player_gui.hotbar[player_gui.hotbar_index] = False
					player_gui.hotbar_index -= 1
					player_gui.hotbar[player_gui.hotbar_index] = True	
				else:
					player_gui.hotbar[player_gui.hotbar_index] = False
					player_gui.hotbar_index = 4
					player_gui.hotbar[player_gui.hotbar_index] = True
					
			if event.button == 1: #detects left click
				if player_gui.show_inventory == True: #detects where in inventory the player is clicking.
					for rects in player_gui.inv_rects:
						if player_gui.inv_rects[rects].collidepoint(mouse_pos):
							print(rects)#rects is the inventory cell name or key for the inv_rects dictionary
				spear.do(screen,scroll,player)
				print(player.direction)			
			if event.button == 3:#for future right click functionality
				pass
			
		if event.type == pygame.QUIT:
			running = False 						
	pygame.display.update()	
pygame.quit()