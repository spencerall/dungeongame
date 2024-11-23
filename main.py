import pygame, os, sys
import gui, level
import entities as e
from pygame.locals import *		

WIDTH = 1080
HEIGHT = 720
FPS = 60

game_folder = os.path.dirname(__file__)#paths
soundfx_folder = os.path.join(game_folder,'audio','soundfx')
music_folder = os.path.join(game_folder,'audio','music')

pygame.init() #starts pygame
pygame.mixer.init() #starts sound mixer
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates window 
pygame.display.set_caption("Video Game") #names window
pygame.display.set_icon(pygame.image.load(os.path.join('ui','gameicon.png')))
clock = pygame.time.Clock() #starts clock

pygame.mixer.music.load(os.path.join(music_folder,'ambient.mp3')) #load sounds
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

player_dmg_sound = pygame.mixer.Sound(os.path.join(soundfx_folder,'playerdmg.wav'))
scroll = [0,0]

player = e.Player(WIDTH/2,HEIGHT/5,39,60)#Instantiates player
slime = e.Slime(WIDTH/3,HEIGHT/5,32,32)#Instantiates Slime
player_gui =gui.PlayerGui(64,64,25,657,screen) 

menus_dict = {'Main': ['singleplayer', 'settings', 'quit'],
			'Pause': ['continue','mainmenu', 'settings', 'quit'],
			'GameOver': ['mainmenu','quit']}
menu_manager = gui.MenuManager(screen,WIDTH,HEIGHT,menus_dict)
menu_manager.set_current_menu('Main')

gameover_overlay = pygame.Surface((WIDTH,HEIGHT))
gameover_overlay.fill((255,94,99))
gameover_overlay.set_alpha(100)
gameover_img = pygame.image.load(os.path.join('ui','gameover.png'))
gameover_img.set_colorkey((255,255,255))

game_map = level.LevelModules(1,3)
game_map.level_constructor()
game_map.spawn_player_in_center(player)


running = True #game loop
while running:
	
	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and menu_manager.current_menu_name == None:
				menu_manager.set_current_menu('Pause')
			elif event.key == pygame.K_ESCAPE and menu_manager.current_menu_name == 'Pause':
				menu_manager.set_current_menu(None)
			elif event.key == pygame.K_e:
				player_gui.show_inventory = not player_gui.show_inventory
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if event.button == 5: #scroll up
				if player_gui.hotbar_index < 4:
					player_gui.hotbar[player_gui.hotbar_index] = False 
					player_gui.hotbar_index += 1
					player_gui.hotbar[player_gui.hotbar_index] = True
				else:
					player_gui.hotbar[player_gui.hotbar_index] = False 
					player_gui.hotbar_index = 1
					player_gui.hotbar[player_gui.hotbar_index] = True
			elif event.button == 4: #scroll down
				if player_gui.hotbar_index > 1:
					player_gui.hotbar[player_gui.hotbar_index] = False 
					player_gui.hotbar_index -= 1
					player_gui.hotbar[player_gui.hotbar_index] = True
				else:
					player_gui.hotbar[player_gui.hotbar_index] = False 
					player_gui.hotbar_index = 4
					player_gui.hotbar[player_gui.hotbar_index] = True
			elif event.button == 1: #left click
				if player_gui.show_inventory == True:
					for rects in player_gui.inv_rects:
						if player_gui.inv_rects[rects].collidepoint(pos):
							print(rects)
			elif event.button == 3: #right click
				pass
			
		if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN):			
			action = menu_manager.handle_event(event)			
			if action is not None:						#if you click a button
				if action == 'singleplayer':			#if that button is "buttonname"					
					menu_manager.set_current_menu(None)	#do "something"
					player = e.Player(WIDTH/2,HEIGHT/5,39,60)
					player_gui =gui.PlayerGui(64,64,25,657,screen)
				elif action == 'continue':				#elif so that it doesn't need to evaluate each	
					menu_manager.set_current_menu(None)
				elif action == 'settings':
					pass
				elif action == 'quit':
					pygame.quit()
					sys.exit()
				elif action == 'mainmenu' and menu_manager.current_menu_name == 'GameOver' or 'Pause':
				
					menu_manager.set_current_menu('Main')										
					
	screen.fill((140,209,255))
	
	if menu_manager.current_menu_name == None:		
		screen.fill((140,209,255)) #background color
		
		scroll[0] += (player.rect.x-scroll[0]-500)/10 #makes the camera follows the player on x-axis
		scroll[1] += (player.rect.y-scroll[1]-300)/10 #makes the camera follows the player on y-axis
			
		tile_rects = game_map.construct_interpreter(screen,scroll) #draws the tiles on the screen
		
		player.do(screen,scroll,tile_rects,slime,player_gui,menu_manager)#updates and draws player
		slime.do(screen,scroll,tile_rects,player) #updates and draws slime
		player_gui.do(screen)
		
	elif menu_manager.current_menu_name == 'Pause':
		tile_rects = game_map.construct_interpreter(screen,scroll)
		player.draw(screen,scroll)
		slime.draw(screen,scroll)
		player_gui.draw(screen)
		
	if menu_manager.current_menu_name == 'GameOver':
		tile_rects = game_map.construct_interpreter(screen,scroll)
		player.draw(screen,scroll)
		slime.draw(screen,scroll)
		player_gui.draw(screen)
	
		screen.blit(gameover_overlay,(0,0))
		screen.blit(gameover_img,((WIDTH/2-300),(HEIGHT-500)))
		player = e.Player(WIDTH/2,HEIGHT/5,39,60)
		player_gui =gui.PlayerGui(64,64,25,657,screen)
			
	menu_manager.draw()
	
	pygame.display.update()

	clock.tick(FPS) #limits how often this loop can run