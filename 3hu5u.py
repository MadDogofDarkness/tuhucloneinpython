import pygame
import random

#define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
OFFWHITE = (245, 245, 245)
GREY = (100, 100, 100)

#define layers
#background = 0
#objects = 1
#npcs = 2
#items = 3
#player = 4
#menus = 5
#overlay = 6

#init pygame modules
pygame.init()
pygame.font.init()

#set screen size
size = [400, 400]
pygame.display.set_caption("testgame")
screen = pygame.display.set_mode(size)
icron = pygame.image.load('smile.bmp').convert()
pygame.display.set_icon(icron)
#init font
textfont = pygame.font.SysFont('Comic Sans MS', 20)
#test setup gameplay screen
gameScreen = pygame.Surface((300, 350))
gridScreen = pygame.Surface((400, 400))

#import images
plyrsprite = pygame.image.load('bcirno.png').convert()
cirnoshot = pygame.image.load('cirshot.png').convert()

def displayStartMenu(selection):
	'''displays the start menu'''
	pygame.draw.rect(screen, BLACK, (0, 0, 400, 400))
	if selection == 0:
		pygame.draw.rect(screen, BLUE, (45, 300, 80, 30), 5)
	else:
		pygame.draw.rect(screen, BLUE, (270, 300, 80, 30), 5)
	menuText = textfont.render('START', False, GREEN)
	screen.blit(menuText,(50, 300))
	menuText = textfont.render('EXIT', False, RED)
	screen.blit(menuText, (275, 300))

def displayGame(playerposition, firetrue):
	pygame.draw.rect(screen, BLACK, (0, 0, 400, 400))
	#pygame.draw.rect(screen, WHITE, (0, 10, 400, 30))
	displayGameScreen(playerposition)
	displayGameUI()
	displayCursor(playerposition)
	#displayGameScreen(playerposition)
	routine("fairy", 1)
	if firetrue == True:
		firebullet("bullet", playerposition, 8.5)
	drawbullets(bullets)
	displayGrid()

def displayGameUI():
	pygame.draw.rect(screen, GREY, (0, 0, 50, 400))
	#print("box: " + str(i))
	pygame.draw.rect(screen, GREY, (350, 0, 50, 400))

def displayCursor(playerposition):
	screen.blit(plyrsprite, (playerposition))

def displayGrid():
	for i in range(0, 9):
		pygame.draw.line(screen, BLUE, (0 + (i * 50), 0), ((0 + (i * 50)), 400), 2)
		pygame.draw.line(screen, BLUE, (0, (i * 50)), (400, (i * 50)), 2)

def displayGameScreen(playerPosition):
	#box1
	gameScreen.fill(OFFWHITE)
	#pygame.draw.rect(gameScreen, RED, ((50 + playerPosition), (50 + playerPosition), 100 + (0.5 * playerPosition), 100 + (0.5 * playerPosition)))
	#pygame.draw.rect(gameScreen, GREY, ((0), (75), (100), (250)))
	#pygame.draw.rect(gameScreen, GREY, ((300), (75), (100), (250)))
	screen.blit(gameScreen, (50, 25))

def firebullet(image, position, speed):
	fireingposition = (position[0] + 11, position[1] - 2)
	bullets.append((fireingposition, speed))

def updatebullets(bullets, list_of_targets):
	newbullets = []
	for i in range(0, len(bullets)):
		if(bullets[i][0][1] > 0):
			newbullets.append(((bullets[i][0][0], bullets[i][0][1] - bullets[i][1]), bullets[i][1]))
	return newbullets

def drawbullets(bullets):
	for i in range(0, len(bullets)):
		#print(str(bullets[i]))
		screen.blit(cirnoshot, bullets[i][0])

def spawnFairy(position):
	fairy = pygame.draw.circle(screen, GREEN, position, 10)
	print("a fairy has spawned")
	return fairy

def routine(fairy, number):
	print("running routine")
	flist = []
	runroutine = number
	if runroutine == 1:
		flist.append(spawnFairy((60, 30)))
		flist.append(spawnFairy((150, 40)))
		flist.append(spawnFairy((200, 30)))
	else:
		pass # no routine running
	return flist

#main loop
'''global vars'''
done = False
clock = pygame.time.Clock()
clicked = 0
selection = 0
selected = False
mauspos = (205, 305)
state = "running"
position = 0
fire = False
playerspeed = 6
bullets = []
fairylist = []
'''end global vars'''

while not done:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			state = "closing"
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mauspos = pygame.mouse.get_pos()
			#clicked = 1
			print("selection: " + str(selection) + " state " + state + " selected " + str(selected) + str(mauspos))
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				selected = True
			else:
				if selection == 1:
					selection = 0
				elif selection == 0:
					selection = 1
	#wipe screen
	screen.fill(WHITE)
	#process movement
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_a]:
		mauspos = (mauspos[0] - playerspeed, mauspos[1])
	if keys_pressed[pygame.K_d]:
		mauspos = (mauspos[0] + playerspeed, mauspos[1])
	if keys_pressed[pygame.K_w]:
		mauspos = (mauspos[0], mauspos[1] - playerspeed)
	if keys_pressed[pygame.K_s]:
		mauspos = (mauspos[0], mauspos[1] + playerspeed)
	if keys_pressed[pygame.K_SPACE]:
		fire = True
	if keys_pressed[pygame.K_SPACE] == False:
		fire = False
	else:
		pass #donothing
	#handleborders
	if mauspos[0] < 51:
		mauspos = (52, mauspos[1])
	elif mauspos[0] > 327:
		mauspos = (325, mauspos[1])
	elif mauspos[1] < 25:
		mauspos = (mauspos[0], 27)
	elif mauspos[1] > 343:
		mauspos = (mauspos[0], 341)
	else:
		pass #donothing
	#handlestates
	if state == "closing":
		done = True
		print(str(bullets))
	elif state == "starting":
		displayStartMenu(selection)
		if selected == True:
			if selection == 1:
				state = "closing"
			elif selection == 0:
				state = "running"
			else:
				pass # do nothing broh
			selected = False
	elif state == "running":
		displayGame(mauspos, fire)
		bullets = updatebullets(bullets, fairylist)
		#displayCursor(mauspos)
		if selected == True:
			state = "starting"
			selected = False
	else:
		pass # invalid state
	
	
	#print("clicked: " + str(clicked) + " " + str(mauspos))
	
	#clicked = 0
	#print(str(firebullet))
	#firebullet = False
	pygame.display.flip()
	
	pygame.time.wait(100)
