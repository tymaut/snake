import pygame
import random
from collections import deque
pygame.init()

winSize = (500,500)
minSize = 20
win = pygame.display.set_mode(winSize)
pygame.display.set_caption("Snake")
score = 0
delay = 60
scoreFont = pygame.font.Font('freesansbold.ttf', 16)

class Coord:
	def __init__(self,x,y):
		self.X = x
		self.Y = y
	def X(self):
		return self.X
	def Y(self):
		return self.Y
	def pos(self):
		return (self.X, self.Y)
	def __eq__(self, other): 
		if(self.X == other.X and self.Y == other.Y):
			return True
		return False

		
class Snake:
#w=1, a=2, s=3, d=4
	def __init__(self):
		self.width = minSize
		self.unit_length = minSize
		self.headColor = (0,255,0)
		self.color = (0,0,255)
		self.speed = minSize
		self.dir = random.randint(1,4)
		self.trail = deque()
		self.start_loc = Coord(240,240)
		self.trail.append(self.start_loc)
		self.gulp = False
	def get_length(self):
		return len(self.trail)
	def get_width(self):
		return self.width
	def get_head_loc(self):
		return self.trail[0]
	def get_speed(self):
		return self.speed
	def get_color(self):
		return self.color
	def get_headColor(self):
		return self.headColor
	def get_trail(self):
		return self.trail
	def set_eaten(self):
		self.gulp = True
	def set_dir(self,s):
		if(abs(self.dir-s)!=2):
			self.dir = s;
	def updateTrail(self,worm):
		global score
		if self.dir == 1:
			newLoc = Coord(self.trail[0].X,self.trail[0].Y-self.speed)
			if(newLoc.Y < 0):
				newLoc.Y = winSize[1]-self.speed
		if self.dir == 3:
			newLoc = Coord(self.trail[0].X,self.trail[0].Y+self.speed)
			if(newLoc.Y >= winSize[1]):
				newLoc.Y = 0
		if self.dir == 2:
			newLoc = Coord(self.trail[0].X-self.speed,self.trail[0].Y)
			if(newLoc.X < 0):
				newLoc.X = winSize[0]-self.speed			
		if self.dir == 4:
			newLoc = Coord(self.trail[0].X+self.speed,self.trail[0].Y)
			if(newLoc.X >= winSize[0]):
				newLoc.X = 0			
		if(self.check_clash_worm(newLoc,worm)):
			self.gulp = True
			score += 1
		if(not self.gulp):
			self.trail.rotate(1)
			self.trail.popleft()
		self.trail.appendleft(newLoc)
		if(self.gulp):
			worm.gulped(self)
			self.gulp = False
			
	def get_im_rect(self,index):
		return(self.trail[index].X, self.trail[index].Y,self.width, self.unit_length)
		
	def check_clash_head(self,other):
		if(other.get_loc() == self.get_head_loc()):
			return True
		return False
	
	def check_clash_worm(self,newLoc,worm):
		rect1 = pygame.Rect(newLoc.X,newLoc.Y,self.width,self.unit_length)
		rect2 = pygame.Rect(worm.get_loc().X-worm.get_radius(), worm.get_loc().Y-worm.get_radius(),worm.get_radius()*2, worm.get_radius()*2)
		if(rect1.colliderect(rect2)):
			return True
		return False
		
	def check_clash_self(self):
		for i in range(1,self.get_length()):
			if(self.get_head_loc() == snake.trail[i]):
				return True
		return False
		
	def check_clash_body(self,other):
		for i in range(0,self.get_length()):
			rect1 = pygame.Rect(self.trail[i].X,self.trail[i].Y,self.width,self.unit_length)
			rect2 = pygame.Rect(other.get_loc().X-other.get_radius(), other.get_loc().Y-other.get_radius(),
			other.get_radius()*2, other.get_radius()*2)
			if(rect1.colliderect(rect2)):
				return True
		return False

class Worm:
	def __init__(self):
		self.radius = 10
		self.color = (255,0,0)
		self.loc = Coord(0,0)
		self.respawn()
	def get_radius(self):
		return self.radius
	def get_loc(self):
		return self.loc
	def get_pos(self):
		return self.loc.pos()
	def get_color(self):
		return self.color
	def gulped(self,snake):
		while(True):
			self.respawn()
			clash = snake.check_clash_body(self)
			if(not clash):
				break
	def respawn(self):
		self.loc.X = random.randint(1,winSize[0]/self.radius-1)*self.radius
		self.loc.Y = random.randint(1,winSize[1]/self.radius-1)*self.radius
		
snake = Snake()
worm = Worm()

run = True

def keyControl():
	global run
	for event in pygame.event.get():
		if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
			run = False
		elif (event.type==pygame.KEYDOWN):
			if (event.key == pygame.K_w):
				snake.set_dir(1)
			elif (event.key == pygame.K_s):
				snake.set_dir(3)
			elif (event.key == pygame.K_a):
				snake.set_dir(2)
			elif (event.key == pygame.K_d):
				snake.set_dir(4)
			elif (event.key == pygame.K_SPACE):
				snake.set_eaten()

def print_worm():
	pygame.draw.circle(win,worm.color,worm.get_pos(),worm.get_radius())
	
def print_snake():
	for i in range(0,len(snake.get_trail())):
		color = snake.get_color()
		if(i == 0):
			color = snake.get_headColor()
		pygame.draw.rect(win,color,snake.get_im_rect(i))
	snake.updateTrail(worm)
	
def print_score():
	scoreTextsurface = scoreFont.render(str(score), False, (255, 0, 0))
	win.blit(scoreTextsurface,(100,0))
	speedTextsurface = scoreFont.render(str(delay), False, (255, 0, 0))
	win.blit(speedTextsurface,(winSize[0]-200,0))
	
while(run):
	delay = 80 if 80-int(score/4)<=40 else 80-int(score/4)
	pygame.time.delay(delay)
	win.fill((0,0,0))
	keyControl()
	print_worm()
	print_snake()	
	if(snake.check_clash_self()):
		score = 0
		delay = 60
		snake = Snake()
	print_score()
	pygame.display.update()
pygame.quit()