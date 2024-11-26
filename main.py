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
screen_rect = pygame.Rect(scroll[0],scroll[1],1080,720)

player = e.Player(0,0,39,60)#Instantiates player
slime = e.Slime(720,352,32,32)#Instantiates Slime, adjust where it spawns here 
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

game_map = {}

running = True #game loop
while running:
	scenery_rects = []
	tile_rects = []
	
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
				left_clicked = True 						#holds whether a left click happened for one cycle
				
				
				if player_gui.show_inventory == True:							#if the inventory is showing,
					
					for slot in player_gui.inv_cells:							#loop through all the inventory slots
						if player_gui.inv_cells[slot][0].collidepoint(pos):		#if the mouse is colliding with a slot,
						
							slot_contents = player_gui.inv_cells[slot][1][0]	#setting variables for readability
							slot_qty = player_gui.inv_cells[slot][1][1]
							held_contents = player_gui.holding[0]
							held_qty = player_gui.holding[1]
							
							if held_contents is None:									#if player is not holding anything
								if slot_contents is not None:							#if the slot has something in it
									player_gui.holding = player_gui.inv_cells[slot][1]	#player is now holding the list [item,qty] of whatever was in the slot
									player_gui.inv_cells[slot][1] = [None,0]			#slot is now empty
									
							elif player_gui.holding is not None:								#if player is holding something,
								if slot_contents is not None: 									#if the slot has something in it,
									slot_contents,held_contents = held_contents,slot_contents	#Swap the contents													
									slot_qty,held_qty = held_qty,slot_qty						#swap the quantity
								
								else:															#if the slot is empty
									player_gui.inv_cells[slot][1] = player_gui.holding			#slot now contains list [item,qty] of whatever was in player's hand
									player_gui.holding = [None,0]							#player is no longer holding anything
						
						print(player_gui.inv_cells[slot][1])
					print('***************************************************')
					
			elif event.button == 3: #right click
				pass
			
		if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN):			
			action = menu_manager.handle_event(event)			
			if action is not None:						#if you click a button
				if action == 'singleplayer':			#if that button is "buttonname"					
					menu_manager.set_current_menu(None)	#do "something"
					player = e.Player(540,400,39,60)   #change where player spawns here
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
					
	screen.fill((140,209,255))#background color
	
	if menu_manager.current_menu_name == None:		
		
		scroll[0] += (player.rect.x-scroll[0]-500)/10 #makes the camera follows the player on x-axis
		scroll[1] += (player.rect.y-scroll[1]-300)/10 #makes the camera follows the player on y-axis
		
		if scroll[0] <= 40: #player can not scroll left if tyhe player is all the way at the beginning.
			scroll[0] = 40
		
		for y in range (3):			#This block generates the map
			for x in range(5):
				target_x = x - 1 + int(round(scroll[0]/384)) #384 is (chunk_size * tile_size)
				target_y = y + int(round(scroll[1]/384))
				target_chunk = str(target_x) + ';' + str(target_y)
				if target_chunk not in game_map:
					game_map[target_chunk] = level.generate_chunk(target_x,target_y)
				for tile in game_map[target_chunk]:
					screen.blit(level.tile_index[tile[1]],(tile[0][0]*48-scroll[0],tile[0][1]*48-scroll[1]))						,

					if tile[1] in [1,2]:
						tile_rects.append(pygame.Rect(tile[0][0]*48,tile[0][1]*48,48,48))
					elif tile[1] in [4,5,6,7]:		#if the tile is a rock tile
						scenery_rects.append(pygame.Rect(tile[0][0]*48-scroll[0],tile[0][1]*48-scroll[1],48,48)) #add the rect to a list
						
				if left_clicked:
				
					player_screen_x = player.rect.center[0] - scroll[0]		#used to calculate x-proximity to wherever clicked 
					player_screen_y = player.rect.center[1] - scroll[1]		#used to calculate y-proximity to wherever clicked 
				
					for rects in scenery_rects:	
						if rects.collidepoint(pos):
							if abs(player_screen_x - rects.center[0]) < 48 and abs(player_screen_y - rects.center[1]) < 48: #if player is within 48 pixels of the scenery items (rocks,etc.)
								player_gui.inv_cells['a1'][1][0] = 'stone' #replace this with all the possible items you can collect
								player_gui.inv_cells['a1'][1][1] += 1
								
							#print(rects) #debugging
							pygame.draw.rect(screen,(255,255,255),rects,width=2) #debugging
							
							left_clicked = False
					
		player.do(screen,scroll,tile_rects,slime,player_gui,menu_manager)#updates and draws player
		
		if player.rect.x <= 39: #Binds the player to the screen. 
			player.rect.x = 39 #Only gets triggered if the screen is no longer scrolling i.e. beginning and end of a level.
		
		slime.do(screen,scroll,tile_rects,player) #updates and draws slime
		player_gui.do(screen) #updates and draws player gui
		
	elif menu_manager.current_menu_name == 'Pause':
		#this is copy & pasted from menu_manager == None section just above, look into finding a way to not repeat it
		for y in range (3):																						#
			for x in range(5):																					#
				target_x = x - 1 + int(round(scroll[0]/384)) 													#
				target_y = y + int(round(scroll[1]/384))														#
				target_chunk = str(target_x) + ';' + str(target_y)												#
				if target_chunk not in game_map:																#
					game_map[target_chunk] = level.generate_chunk(target_x,target_y)							#
				for tile in game_map[target_chunk]:																#
					screen.blit(level.tile_index[tile[1]],(tile[0][0]*48-scroll[0],tile[0][1]*48-scroll[1]))	#
					
		player.draw(screen,scroll)
		slime.draw(screen,scroll)
		player_gui.draw(screen)
		
	if menu_manager.current_menu_name == 'GameOver':
		#tile_rects = game_map.construct_interpreter(screen,scroll)
		player.draw(screen,scroll)
		slime.draw(screen,scroll)
		player_gui.draw(screen)
	
		screen.blit(gameover_overlay,(0,0))
		screen.blit(gameover_img,((WIDTH/2-300),(HEIGHT-500)))
		player = e.Player(WIDTH/2,-500,39,60)
		player_gui =gui.PlayerGui(64,64,25,657,screen)
			
	menu_manager.draw()
	
	pygame.display.update()

	clock.tick(FPS) #limits how often this loop can run