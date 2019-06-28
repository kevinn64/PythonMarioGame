import pygame
import time
import random
from pygame.locals import*
from time import sleep

class Sprite():
    def __init__(self):
        print("sup")
        
    #def isMario: 
    
class Mario(Sprite):
    def __init__(self,model):
            self.model = model;
            self.x = 50
            self.y = 355
            self.h = 95
            self.w = 60
            self.vert_vel = 12
            self.prev_x = 0
            self.prev_y = 0
            self.frame = 0
            self.runcount = 0
            self.images = []
            self.images.append(pygame.image.load("mario1.png"))
            self.images.append(pygame.image.load("mario2.png"))
            self.image = self.images[self.runcount]
            self.rect = self.image.get_rect()
            self.bottom = False

    def does_collide(self, spr1_x, spr1_y, spr1_wid, spr1_hgt, spr2_x, spr2_y, spr2_wid, spr2_hgt):
        if(spr1_x + spr1_wid <= spr2_x): return False
        if(spr1_x >= spr2_x + spr2_wid): return False
        if(spr1_y + spr1_hgt <= spr2_y): return False
        if(spr1_y >= spr2_y + spr2_hgt): return False
        return True
    
    def getOut(self, spr1_x, spr1_y, spr1_wid, spr1_hgt):
        if self.rect.x + self.rect.w >= spr1_x and self.prev_x  + self.rect.w <= spr1_x: #left 
             self.rect.x = spr1_x - self.rect.w - 1
             #print("left")
        elif self.rect.x <= spr1_wid + spr1_x and self.prev_x >= spr1_x + spr1_wid: #right
            self.rect.x = spr1_x + spr1_wid+1
           # print("right")
        elif self.rect.y + self.rect.h >= spr1_y and self.prev_y  + self.rect.h <= spr1_y:  #above
            self.rect.y = spr1_y - self.rect.h
            self.vert_vel = 0
            self.frame = 0
        elif self.rect.y <= spr1_y + spr1_hgt and self.prev_y >= spr1_y + spr1_hgt: #below
            self.rect.y = spr1_y + spr1_hgt
            self.vert_vel = 0
            self.bottom = True;

    
    def update(self):
        #CYCLE THROUGH MARIO IMAGES WHEN HE WALKS 
        if self.runcount % 5 == 0:
            self.image = pygame.image.load("mario1.png")
        if self.runcount % 5 == 1:
            self.image = pygame.image.load("mario2.png")      
        if self.runcount % 5 == 2:
            self.image = pygame.image.load("mario3.png")   
        if self.runcount % 5 == 3:
            self.image = pygame.image.load("mario4.png")   
        if self.runcount % 5 == 4:
            self.image = pygame.image.load("mario5.png")          
            
        #print("MARIOOOOOUPDATEMETHOD")
        if self.vert_vel is None:
            self.vert_vel = 0.0
        self.vert_vel += 1.1
        self.rect.top += self.vert_vel
        #print(self.y)
        if self.rect.top > 355:
            self.vert_vel = 0.0
            self.rect.top = 355
            self.frame = 0
        self.frame += 1    
        
        for b in self.model.sprites: #BRICK COLLISION
            if b.isBrick() or b.isCoinBlock():
                #print(self.prev_x)
                if self.does_collide(self.rect.x,self.rect.y,self.rect.w,self.rect.h,b.rect.x,b.rect.y,b.rect.w,b.rect.h):
                    #print("collides")
                    self.getOut(b.rect.x, b.rect.y, b.rect.w, b.rect.h) 
                    if b.isCoinBlock() and self.bottom:
                        b.count += 1
                        b.addcoin = True
                        self.bottom = False
                        #print(b.count)
        
    def isBrick(self): return False
    def isCoinBlock(self): return False
    def isCoin(self): return False
    def last_location(self):
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        
    def drawImage(self):
        v.screen.blit(self.image,(self.rect.x - self.rect.x, self.rect.y))
    
            
class Brick(Sprite):
    def __init__(self,model,x,y,w,h):
        self.model = model
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load("brix.png")
        self.image = pygame.transform.scale(self.image,(self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    def update(self):
        pass
    def isBrick(self): return True
    def isCoinBlock(self): return False
    def isCoin(self): return False
    def last_location(self): pass
    def drawImage(self):
        v.screen.blit(self.image,(self.rect.x - self.model.mario.rect.x, self.rect.y))

class CoinBlock(Sprite):
    def __init__(self,model,x,y,w,h):
        self.model = model
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.count = 0
        self.imagecount = 0
        self.dead = False
        self.addcoin = False     
        self.images = []
        self.images.append(pygame.image.load("block1.png"))
        self.images.append(pygame.image.load("block2.png"))
        self.image = self.images[self.imagecount]
        self.rect = self.image.get_rect(topleft=(self.x,self.y))

    def drawImage(self):
        if self.dead == False:
            #self.imagecount = 0
            v.screen.blit(self.images[0],(self.rect.x - self.model.mario.rect.x, self.rect.y))
        if self.dead == True:
            #self.imagecount = 1
            v.screen.blit(self.images[1],(self.rect.x - self.model.mario.rect.x, self.rect.y))
        
    def update(self):
        if self.count == 5:
            self.dead = True
        if self.addcoin == True:
            if self.count < 6:
                self.model.addCoin(self.x,self.y)
            self.addcoin = False
    def last_location(self): pass
    def isBrick(self): return False
    def isCoinBlock(self): return True
    def isCoin(self): return False

class Coin():
    def __init__(self,model,x,y):
        self.model = model
        self.x = x
        self.y = y
        self.w = 75
        self.h = 75
        self.hvel = 0
        self.vvel = 0
        self.coindead = False
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect(topleft=(self.x,self.y))

    def last_location(self): pass
    def isBrick(self): return False
    def isCoinBlock(self): return False
    def isCoin(self): return True

    def update(self):
        self.vvel += 3.14159
        self.rect.y += self.vvel
        self.rect.y -= 30.14
        
        self.rect.x += self.hvel
        
        if self.rect.y > 5000:
            self.coindead = True
    def drawImage(self):
         v.screen.blit(self.image,(self.rect.x - self.model.mario.rect.x, self.rect.y))

class Model():
	def __init__(self):
		#self.dest_x = 0
		#self.dest_y = 0
		self.sprites = []
		self.mario = Mario(self)
		self.sprites.append(self.mario)
		self.brick1 = Brick(self,110,190,100,100)
		self.sprites.append(self.brick1)
		self.brick2 = Brick(self,300,190,100,100)
		self.sprites.append(self.brick2)
                self.brick3 = Brick(self,500,380,100,100)
		self.sprites.append(self.brick3)	
		self.coinblock1 = CoinBlock(self,700,200,100,100)
		self.sprites.append(self.coinblock1)
		self.coinblock2 = CoinBlock(self, 500, 140, 100,100)
		self.sprites.append(self.coinblock2)
                self.coinblock3 = CoinBlock(self, 900, 180, 100,100)
		self.sprites.append(self.coinblock3)
		#self.sprites.append("OBJECT2");
		#print(self.sprites)
		
	def addCoin(self,x,y):
            self.rand = random.randint(-5,20)
            self.c = Coin(self,x,y)
            self.c.hvel = self.rand
            self.sprites.append(self.c)
    
	def update(self):
                #print("hey")
                #print(len(self.sprites))
                
                #i=0
                #while i < len(self.sprites): #update sprites
                   ## print(self.sprites[i])
                    #self.sprites[i].update()
                    #i += 1
                for s in self.sprites:
                    s.update()
                #x = 0;
                #for x in len(self.sprites):
                    #print("hey");


class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
                self.model = model
		#for x in model.sprites:
                    #print(model.mario.x)
		#self.turtle_image = pygame.image.load("mario1.png")
		#self.model.mario.rect = self.turtle_image.get_rect(x=(self.model.mario.x),y=(self.model.mario.y))
		#BACKGROUND IMAGE
                self.background = pygame.image.load("background.png")
                
                #BRICK FLOOR
                self.floor = pygame.image.load("brix.png")
                self.floor = pygame.transform.scale(self.floor,(999,100))
                
	def update(self):    
		self.screen.blit(self.background,self.background.get_rect())
                rect = self.floor.get_rect()
                rect = rect.move((0,450))
		self.screen.blit(self.floor,rect)
		#self.screen.blit(self.model.mario.image, self.model.mario.rect)
		
		for sprite in self.model.sprites:
                    sprite.drawImage()
                    #self.screen.blit(sprite.image,sprite.rect)
		#pygame.display.flip()
		pygame.display.update()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
                for sprite in self.model.sprites:
                    sprite.last_location()
            
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			#elif event.type == pygame.MOUSEBUTTONUP:
				#self.model.set_dest(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.rect.x -= 10
			self.model.mario.runcount += 1
			#print(self.model.mario.rect.x)
		if keys[K_RIGHT]:
			self.model.mario.rect.x += 10
			self.model.mario.runcount += 1
			#print(self.model.mario.runcount)
                if keys[K_SPACE]:
                    if self.model.mario.frame < 5:
                        if self.model.mario.vert_vel == 0: #CONDITION KEEPS HIM FROM JUMP-FLYING
                            self.model.mario.vert_vel = -16


print("Use the arrow keys to move, space to jump. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.02)
print("Goodbye")