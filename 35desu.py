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
test_enemy_sprite = pygame.image.load('enemy1.png').convert()
plyrsprite = pygame.image.load('bcirno.png').convert()
cirnoshot = pygame.image.load('cirshot.png').convert()

#define classes
class Enemy(pygame.sprite.Sprite):
	def __init__(self, image, posx, posy, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(test_enemy_sprite.get_size(), test_enemy_sprite)
		self.rect = self.image.get_rect()
		self.position = (posx, posy)
		self.speed = speed

class Bullet(pygame.sprite.Sprite):
	def __init__(self, image, posx, posy, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(cirnoshot)
		self.rect = self.image.get_rect()
		self.position = (posx, posy)
		self.speed = speed

def displayStartMenu(selection):
	'''displays the start menu'''
	pygame.draw.rect(screen, BLACK, (0, 0, 400, 400))
	#determine selection
	if selection == 0:
		pygame.draw.rect(screen, BLUE, (45, 300, 80, 30), 5)
	else:
		pygame.draw.rect(screen, BLUE, (270, 300, 80, 30), 5)
	#display the buttons
	menuText = textfont.render('START', False, GREEN)
	screen.blit(menuText,(50, 300))
	menuText = textfont.render('EXIT', False, RED)
	screen.blit(menuText, (275, 300))

def displayGame(playerposition, firetrue):
	pygame.draw.rect(screen, BLACK, (0, 0, 400, 400))
	#pygame.draw.rect(screen, WHITE, (0, 10, 400, 30))
	displayGameScreen() # display background of play area
	displayGameUI() # display sidebars for menu
	displayPlayer(playerposition)
	#displayGameScreen(playerposition)
	routine("fairy", 1)
	if firetrue == True:
		firebullet("bullet", playerposition, 8.5)
	drawbullets(bullets)
	showEnemies()
	displayGrid()

def displayGameUI():
	#displays the sidebars, will display menu information too eventually
	pygame.draw.rect(screen, GREY, (0, 0, 50, 400))
	#print("box: " + str(i))
	pygame.draw.rect(screen, GREY, (350, 0, 50, 400))

def displayPlayer(playerposition):
	#displays the player
	screen.blit(plyrsprite, (playerposition))

def displayGrid():
	#displays the debug grid
	for i in range(0, 9):
		pygame.draw.line(screen, BLUE, (0 + (i * 50), 0), ((0 + (i * 50)), 400), 2)
		pygame.draw.line(screen, BLUE, (0, (i * 50)), (400, (i * 50)), 2)

def displayGameScreen():
	#fills the play field background
	gameScreen.fill(OFFWHITE)
	screen.blit(gameScreen, (50, 25))

def firebullet(image, position, speed):
	bullet = Bullet(cirnoshot, position[0] + 11, position[1] - 2, 8.5)
	bullets.append(bullet)

def updatebullets(bullets):
	#updates new bullet positions
	#returns list of bullets in updated positions
	newbullets = []
	for i in range(0, len(bullets)):
		if(bullets[i][0][1] > 0):
			newbullets.append(((bullets[i][0][0], bullets[i][0][1] - bullets[i][1]), bullets[i][1]))
	return newbullets

def drawbullets(bullets):
	#draws the bullets to the screen
	for bullet in bullets:
		screen.blit(bullet)
	print("drew bullets")

def spawnFairy(position):
	fairy = Enemy(test_enemy_sprite, position[0], position[1], 0)
	#print("a fairy has spawned")
	return fairy

def routine(fairy, number):
	print("running routine")
	#flist = []
	runroutine = number
	if runroutine == 1:
		fairylist.append(spawnFairy((60, 30)))
		fairylist.append(spawnFairy((150, 40)))
		fairylist.append(spawnFairy((200, 30)))
	else:
		pass # no routine running
	#return flist
def showEnemies(enemy_list):
	#displays all enemies in the list
	for enemy in enemy_list:
		screen.blit(enemy.image, enemy.position)
	print("showed enemies")

def check_collision(bullets, enemies):
	local_score = 0
	for bullet in bullets:
		for enemy in enemies:
			if (pygame.sprite.collide_rect(bullet, enemy)):
				bullets.remove(bullet)
				enemies.remove(enemy)
				local_score += 1
	return local_score


#main loop
'''global vars'''
done = False
clock = pygame.time.Clock()
clicked = 0
selection = 0
selected = False
mauspos = (205, 305) #holds tuple for player position
state = "starting"
position = 0
fire = False
playerspeed = 6
points = 0
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
		points += check_collision(bullets, fairylist)
		bullets = updatebullets(bullets) # updates new bullet positions
		print(f"score: {points}")
		#displayCursor(mauspos)
		if selected == True:
			#lets you pause and return to main screen
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
