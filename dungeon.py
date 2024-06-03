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
pygame.display.set_icon(pygame.image.load(os.path.join('ui','gameicon.png')))
clock = pygame.time.Clock() #starts clock

pygame.mixer.music.load(os.path.join(music_folder,'ambient.mp3')) #load sounds
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

player_dmg_sound = pygame.mixer.Sound(os.path.join(soundfx_folder,'playerdmg.wav'))
scroll = [0,0]

player = e.Player(WIDTH/2,HEIGHT/5,39,60)#Instantiates player
slime = e.Slime(WIDTH/3,HEIGHT/5,32,32)#Instantiates Slime

menu = gui.Menu(WIDTH,HEIGHT)#Instantiates menu class
player_gui = gui.PlayerGui(64,64,25,657)#Instantiates player gui

mob_rects = []	
mob_rects.append(slime.rect)

main_menu = True

running = True #game loop
while running:
	clock.tick(FPS) #limits how often this loop can run
	screen.fill((140,209,255)) #background color		

	if main_menu == True:
		menu.type = 'main'
		menu.do(screen,HEIGHT)
				
	elif main_menu == False:
		scroll[0] += (player.rect.x-scroll[0]-500)/10 #makes the camera follows the player on x-axis
		scroll[1] += (player.rect.y-scroll[1]-300)/10 #makes the camera follows the player on y-axis
		
		tile_rects = level.drawMap(screen,scroll) #draws the tiles on the screen
		mouse_pos = pygame.mouse.get_pos() #get mouse position to do stuff
		
		player.do(screen,scroll,player_gui,tile_rects,slime)#updates and draws player
		slime.do(screen,scroll,tile_rects,player) #updates and draws slime
		
		player_gui.update(screen,menu,mouse_pos) #updates and draws hitpoints bar, player's hotbar, and inventory
		menu.do(screen,HEIGHT)#updates and draws pause menu. Will also handle main menu.

	pygame.display.update()

pygame.quit()