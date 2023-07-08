import pygame, os, gui, level
import entities as e			

WIDTH = 1080#Useful constants
HEIGHT = 720
FPS = 60

game_folder = os.path.dirname(__file__)#paths
soundfx_folder = os.path.join(game_folder,'audio','soundfx')
music_folder = os.path.join(game_folder,'audio','music')

pygame.init() #starts pygame
pygame.mixer.init() #starts sound mixer
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates window 
pygame.display.set_caption("Video Game") #names window
clock = pygame.time.Clock() #starts clock

pygame.mixer.music.load(os.path.join(music_folder,'ambient.mp3')) #load sounds
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

player_dmg_sound = pygame.mixer.Sound(os.path.join(soundfx_folder,'playerdmg.wav'))
scroll = [0,0]

player = e.Player(WIDTH/2,HEIGHT/5,39,60)#Instantiates player
slime = e.Slime(WIDTH/3,HEIGHT/5,32,32)#Instantiates Slime
stab_weapon = e.StabWeapon(player,scroll)#instantiates spear

main_menu = gui.Menu(WIDTH/4,HEIGHT/5)#Instantiates menu class
player_gui = gui.PlayerGui(64,64,25,657)#Instantiates player gui

running = True #game loop
while running:
	clock.tick(FPS) #limits how often this loop can run
	screen.fill((140,209,255)) #background color		
	
	scroll[0] += (player.rect.x-scroll[0]-500)/10 #makes the camera follows the player on x-axis
	scroll[1] += (player.rect.y-scroll[1]-300)/10 #makes the camera follows the player on y-axis
	
	tile_rects = level.drawMap(screen,scroll) #draws the tiles on the screen
	mouse_pos = pygame.mouse.get_pos() #get mouse position to do stuff
	
	player.do(screen,scroll,player_gui,tile_rects,slime)#updates and draws player
	slime.do(screen,scroll,tile_rects,player) #updates and draws slime
	stab_weapon.do(screen,scroll,player,slime) #updates and draws stab_weapon
	
	player_gui.update(screen) #updates and draws hitpoints bar, player's hotbar, and inventory
	main_menu.do(screen,HEIGHT/5)#updates and draws pause menu. Will also handle main menu.
	
	if stab_weapon.rect.colliderect(slime.rect):
		print('stabbed')
		
	if player.rect.colliderect(slime.rect):
		print('hit')

	for event in pygame.event.get():	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e: #toggles inventory view
				player_gui.show_inventory = not player_gui.show_inventory
				
			if event.key== pygame.K_ESCAPE and main_menu.type == None:#toggles menu
				main_menu.type = 'pause'
			elif event.key == pygame.K_ESCAPE and main_menu.type == 'pause':
				main_menu.type = None
			
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
					
			elif event.button == 4: #detects scrolling down
				if player_gui.hotbar_index > 1: 
					player_gui.hotbar[player_gui.hotbar_index] = False
					player_gui.hotbar_index -= 1
					player_gui.hotbar[player_gui.hotbar_index] = True	
				else:
					player_gui.hotbar[player_gui.hotbar_index] = False
					player_gui.hotbar_index = 4
					player_gui.hotbar[player_gui.hotbar_index] = True
					
			elif event.button == 1: #detects left click
				if player_gui.show_inventory == True: #detects where in inventory the player is clicking.
					for rects in player_gui.inv_rects:
						if player_gui.inv_rects[rects].collidepoint(mouse_pos):
							pass #interact with inventory						
				stab_weapon.visible = True
				
				if main_menu.type == 'pause':
					main_menu.button_function()
					
			elif event.button == 3:#for future right click functionality
				pass
				
		if event.type == pygame.QUIT:
			running = False 
		
	pygame.display.update()	
pygame.quit()