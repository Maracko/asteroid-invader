import random
import pygame

'''TODO
IMPLEMENT OTHER FILE FOR DATABASE, NOT USE GLOBAL VARIABLES!!
time.perf_counter for timer?
'''
# CHANGE 1
pygame.init()

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}

win_width = 1200
win_height = 800
window = pygame.display.set_mode((win_width, win_height))
background=pygame.image.load("pictures/background.jpg")
pygame.display.set_caption("Asteroid invader")
clock = pygame.time.Clock()


ASTEROIDTIMER = pygame.USEREVENT + 1 # adds new event to queue named ASTEROIDTIMER, other events could be added with "pygame.USEREVENT + 2" etc.
pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1500), True) #executes ASTEROIDTIMER event for spawning asteroid  every 1 - 3 seconds, added to main loop as well since it only runs once

SHIP_WIDTH = 50
SHIP_HEIGHT = 87
ASTEROID_WIDTH = 55
ASTEROID_HEIGHT = 56
BULLET_WIDTH = 25
BULLET_HEIGHT = 30

ship = pygame.image.load("pictures/ship.png") #sprite

class Ship:

    def __init__(self, x, y, sprite = ship, width = SHIP_WIDTH, height = SHIP_HEIGHT):
        self.x = x 
        self.y = y 
        self.sprite = sprite
        self.width = width
        self.height = height
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hitbox = (self.x, self.y, self.width, self.height) #make a hitbox 
    
    def dShip(self): #draws ship
        window.blit(self.sprite, (self.x , self.y))
        self.hitbox = (self.x, self.y, self.width, self.height) #redraw hitbox every frame
        pygame.draw.rect(window, colors["red"], self.hitbox, 1)

    def cShip(self): #checks if ship has been moved too far in either direction
        if self.x >= win_width  - self.width: #if ship goes too far to right
            self.x = win_width - self.width 
        elif self.x <= 0: #if ship goes too far to left
            self.x = 0
        if self.y >= win_height - self.height  : #if sheep goes too far down
            self.y = win_height - self.height 
        elif self.y <= 0: #if ship goes too far up
            self.y = 0
        return None

playerShip = Ship(win_width / 2 - SHIP_WIDTH / 2, win_height - SHIP_HEIGHT)

asteroid1 = pygame.image.load("pictures/asteroid-medium.png")
asteroid2 = pygame.image.load("pictures/asteroid-medium-mineral.png")
asteroids = [asteroid1, asteroid2]
allAsteroids = [] # list of all asteroid objects

class Asteroid:
    
    def __init__(self, x, y = 50, sprite = random.choice(asteroids), width = ASTEROID_WIDTH, height = ASTEROID_HEIGHT):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hitbox = (self.x + 5, self.y + 5, self.width, self.height) # asteroid hitbox had to be corrected a little bit
        allAsteroids.append(self) #appends every new asteroid to list of all asteroids so we can manipulate them
        
    def dAsteroid(self): #draw asteroid
        window.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 5, self.y + 5, self.width, self.height) 
        pygame.draw.rect(window, colors["red"], self.hitbox, 1)

    def hAsteroid(self): #handle asteroids
        self.y = self.y + asteroid_speed #moving them downwards
        self.dAsteroid()
        if self.y >= win_height + 50: #adding asteroids to be deleted to a list when they get too far off screen
            deletedAsteroids.append(self)

bullet=pygame.image.load("pictures/bullet.png")
allBullets = []

class Bullet:
    def __init__(self, x, y, sprite = bullet, width= BULLET_WIDTH, height = BULLET_HEIGHT):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hitbox = (self.x + 3, self.y , self.width - 5, self.height)
        allBullets.append(self)


    def dBullet(self):
        window.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 3, self.y , self.width - 5, self.height) #bullet hitbox had to be adjusted as well
        pygame.draw.rect(window, colors["red"], self.hitbox, 1)
    
    def hBullet(self): #handle bullets (moving,drawing)
        self.y = bullet.y - bullet_speed
        self.dBullet()
        if self.y <= -50: #adding bullets to be deleted to a list when they get too far off screen
            deletedBullets.append(self)
'''
    def cBullet(self): #bullet collision
        global score
        for asteroid in allAsteroids:
            x_offset = int(self.x - asteroid.x) # if both object1 and object2 are at same position value is 0
            y_offset = int(self.y - asteroid.y)
            colliding = self.mask.overlap(asteroid.mask, (x_offset, y_offset)) # if object1 and objects in list are touching returns true
            if colliding:
                score += 10
                print(score)
'''                
'''
class Timer:
    def __init__(self, start):
        self.start = start
'''
'''
def sCollision(ship, asteroidlist): #ship collision
    global score
    #global collisioncount
    for asteroid in asteroidlist: #for each object in objectlist
        x_offset = int(ship.x - asteroid.x) # if both object1 and object2 are at same position value is 0
        y_offset = int(ship.y - asteroid.y + asteroid_speed)
        colliding = ship.mask.overlap(asteroid.mask, (x_offset, y_offset)) # if object1 and objects in list are touching returns true
        if colliding:
            score += 10
            print(score)
        #    collisioncount += 1
        #    print(f"COLLISION {collisioncount}")
'''
bullet_speed = 7 # speed of bullet trajectory
asteroid_speed = 5 # controls the move speed of asteroids
collisioncount = 0

score = 0
playing = True
colliding = False

while playing:

    deletedAsteroids = []
    deletedBullets = []
    window.blit(background, (0, 0))
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == ASTEROIDTIMER:
            asteroidstartx = random.randrange(ASTEROID_WIDTH, win_width - ASTEROID_WIDTH) # random position on X line when spawning
            newAsteroid = Asteroid(asteroidstartx, 20, random.choice(asteroids))
            newAsteroid.dAsteroid() 
            pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1500), True) #resetting our timer after it's done
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spawnBullet = Bullet(playerShip.x + 13, playerShip.y)

    if pressed[pygame.K_LEFT]: #controls
        playerShip.x -= 10
    if pressed[pygame.K_RIGHT]:
        playerShip.x += 10
    if pressed[pygame.K_UP]:
        playerShip.y -= 10
    if pressed[pygame.K_DOWN]:
        playerShip.y += 10

    for asteroid in allAsteroids: #drawing and deleting asteroids every frame
        asteroid.hAsteroid()

    for bullet in allBullets: # drawing bullets
        bullet.hBullet()

    for deletedasteroid in deletedAsteroids: #delete all the asteroids that have been placed in the deletedasteroids list
        allAsteroids.remove(deletedasteroid)

    for deletedbullet in deletedBullets: #delete all the bullets that have been placed in the deletedbullets list
        allBullets.remove(deletedbullet)

    playerShip.dShip()
    playerShip.cShip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()

'''
def sCollision(asteroidlist): #ship collision with asteroid
    for asteroid in asteroidlist:
        if playerShip.x > asteroid.x and ship.x < asteroid.x + ASTEROID_WIDTH
'''