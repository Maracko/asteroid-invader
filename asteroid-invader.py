import random
import pygame
import time
import os
import sys
from config import *

pygame.init()

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow":(255,255, 0)
}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

uifont = pygame.font.SysFont('Segoe UI', 24)
icon = pygame.image.load(resource_path("pictures/icon.png"))

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
background = pygame.image.load(resource_path("pictures/background.jpg"))
pygame.display.set_caption("Asteroid invader")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

ship = pygame.image.load(resource_path("pictures/ship.png")) #sprite

ASTEROIDTIMER = pygame.USEREVENT + 1 # adds new event to queue named ASTEROIDTIMER, other events could be added with "pygame.USEREVENT + 2" etc.

'''
#MUSIC CREDITS#
Solar System by Kraftamt (c) copyright 2020 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/Karstenholymoly/61117 Ft: Wired Ant
Moments in Space by spinmeister (c) copyright 2007 Licensed under a Creative Commons Attribution (3.0) license. http://dig.ccmixter.org/files/spinmeister/12093 Ft: DJ Rkod
'''

songs = ["music/Karstenholymoly-Solar_System.mp3","music/spinmeister-Moments_in_Space_2.mp3"]
currently_playing_song = None # sets the song that is playing, at start it is none
END_MUSIC = pygame.USEREVENT + 2 #creating an event for when music ends
pygame.mixer.music.set_endevent(END_MUSIC) #setting that event to happen every time a song ends

def play_music():
    '''Will play a random song from the list of songs that is not the currently playing one'''
    global currently_playing_song, songs
    next_song = random.choice(songs)
    while next_song == currently_playing_song:
        next_song = random.choice(songs)
    currently_playing_song = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()

play_music()

###sound effects###
asteroid_hit = pygame.mixer.Sound('music/asteroid-hit.wav')
asteroid_hit.set_volume(0.2)
ship_damage = pygame.mixer.Sound('music/ship-damage.wav')
ship_damage.set_volume(0.5)
asteroid_miss = pygame.mixer.Sound('music/missed-asteroid.wav')
asteroid_miss.set_volume(0.5)

class Ship:

    def __init__(self, x, y, sprite = ship, width = SHIP_WIDTH, height = SHIP_HEIGHT):
        self.x = x 
        self.y = y 
        self.sprite = sprite
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x + 4, self.y + 2, self.width, self.height) #make a hitbox, adjust as needed with different sprites
        self.last_fire_time = time.perf_counter() #for delaying bullet fire
        self.last_collide_time = time.perf_counter()
    
    def dShip(self): #draws ship
        window.blit(self.sprite, (self.x , self.y))
        self.hitbox = pygame.Rect(self.x + 4, self.y + 2, self.width, self.height) #redraw hitbox every frame
        #pygame.draw.rect(window, colors["red"], self.hitbox, 2) #-> draw hitbox for debugging

    def hShip(self): #checks if ship has been moved too far in either direction
        if self.x >= WIN_WIDTH  - self.width: #if ship goes too far to right
            self.x = WIN_WIDTH - self.width 
        elif self.x <= 0: #if ship goes too far to left
            self.x = 0
        if self.y >= WIN_HEIGHT - self.height  : #if sheep goes too far down
            self.y = WIN_HEIGHT - self.height 
        elif self.y <= 0: #if ship goes too far up
            self.y = 0
        return None
    

playerShip = Ship(WIN_WIDTH / 2 - SHIP_WIDTH / 2, WIN_HEIGHT - SHIP_HEIGHT)

asteroid1 = pygame.image.load(resource_path("pictures/asteroid-medium.png"))
asteroid2 = pygame.image.load(resource_path("pictures/asteroid-medium-mineral.png"))
asteroids = [asteroid1, asteroid2]
allAsteroids = [] # list of all asteroid objects

class Asteroid:
    
    def __init__(self, x, y = 50, sprite = random.choice(asteroids), width = ASTEROID_WIDTH, height = ASTEROID_HEIGHT):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x + 6, self.y + 6, self.width - 4, self.height) # asteroid hitbox had to be corrected a little bit
        allAsteroids.append(self) #appends every new asteroid to list of all asteroids so we can manipulate them
        
    def dAsteroid(self): #draw asteroid
        window.blit(self.sprite, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x + 6, self.y + 6, self.width - 4, self.height) 
        #pygame.draw.rect(window, colors["red"], self.hitbox, 1) #-> draw hitbox for debugging

    def hAsteroid(self): #handle asteroids
        global health
        self.y = self.y + ASTEROID_SPEED #moving them downwards
        self.dAsteroid()
        if self.y >= WIN_HEIGHT + 10: #adding asteroids to be deleted to a list when they get too far off screen
            deletedAsteroids.append(self)
            health -=10
            asteroid_miss.play()

    def hit(self): #when bullet hits asteroid
        global score
        if level == 1:
            score += 15
            asteroid_hit.play()
        if level == 2:
            score += 20
            asteroid_hit.play()
        if level == 3:
            score += 30
            asteroid_hit.play()

bullet=pygame.image.load(resource_path("pictures/bullet.png"))
allBullets = []

class Bullet:
    def __init__(self, x, y, sprite = bullet, width= BULLET_WIDTH, height = BULLET_HEIGHT):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, self.width - 9, self.height)
        allBullets.append(self)

    def dBullet(self):
        window.blit(self.sprite, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, self.width - 9, self.height) #bullet hitbox had to be adjusted as well
        #pygame.draw.rect(window, colors["red"], self.hitbox, 1) #-> draw hitbox for debugging
    
    def hBullet(self): #handle bullets (moving,drawing)
        self.y = self.y - BULLET_SPEED
        self.dBullet()
        if self.y <= -50: #adding bullets to be deleted to a list when they get too far off screen
            deletedBullets.append(self)


def text_objects(text, font):
    textSurface = font.render(text, True, colors["white"])
    return textSurface, textSurface.get_rect()

def message_display(text):
    large_text = pygame.font.SysFont('Segoe UI', 35)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = ((WIN_WIDTH / 2), (WIN_HEIGHT / 2))
    window.blit(text_surface, text_rect)

def draw_ui():
        hp_ui = uifont.render("HP: " + str(health), True, colors["green"]) #creates object that stores our UI/Font
        score_ui = uifont.render("SCORE: " + str(score), True, colors["white"])
        high_score_ui = uifont.render("HIGH SCORE: " + str(high_score), True, colors["white"]) 
        level_ui = uifont.render("LEVEL: " + str(level), True, colors["white"]) 
        window.blit(hp_ui, (40, 20)) #renders the UI
        window.blit(score_ui, (WIN_WIDTH - 230, 20))
        window.blit(high_score_ui, (WIN_WIDTH - 230, 50))
        window.blit(level_ui, (WIN_WIDTH - 230, 80))

def main_menu():

    menu_font = pygame.font.SysFont('Segoe UI', 48)
    run = True

    while run:

        pressed = pygame.key.get_pressed()
        window.blit(background, (0,0))
        title = menu_font.render("Press enter to begin...", 1, colors["white"])
        window.blit(title, (WIN_WIDTH/2 - title.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pressed[pygame.K_RETURN]:
                main()

def set_level(): #increasing difficulty
    global score, level, ASTEROID_SPEED
    if score >= 0 and score <= 300:
        level = 1
        ASTEROID_SPEED = 5
        return 1
    elif score > 300 and score <= 700:
        level = 2
        ASTEROID_SPEED = 6
        return 2
    elif score > 600 and score <= 900:
        level = 3
        ASTEROID_SPEED = 7
        return 3


def main():

    global health, score, high_score, allAsteroids, allBullets, playerShip, deletedBullets, deletedAsteroids, ASTEROIDTIMER, level
    pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1500), True) #executes ASTEROIDTIMER event for spawning asteroid  every 1 - 3 seconds, added to main loop as well since it only runs once
    playing = True

    while playing:

        deletedAsteroids = []
        deletedBullets = []
        window.blit(background, (0, 0))
        events = pygame.event.get()
        pressed = pygame.key.get_pressed()


        for event in events:
            if event.type == pygame.QUIT:
                message_display("Thank you for playing")
                pygame.mixer.music.fadeout(500)
                pygame.display.update()
                time.sleep(2)
                pygame.quit()
            if event.type == ASTEROIDTIMER:
                if level == 1:
                    asteroidstartx = random.randrange(ASTEROID_WIDTH, WIN_WIDTH - ASTEROID_WIDTH) # random position on X line when spawning
                    newAsteroid = Asteroid(asteroidstartx, 20, random.choice(asteroids))
                    newAsteroid.dAsteroid() 
                    pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1500), True)
                if level == 2:
                    asteroidstartx = random.randrange(ASTEROID_WIDTH, WIN_WIDTH - ASTEROID_WIDTH) # random position on X line when spawning
                    newAsteroid = Asteroid(asteroidstartx, 20, random.choice(asteroids))
                    newAsteroid.dAsteroid() 
                    pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1250), True)
                if level == 3:
                    asteroidstartx = random.randrange(ASTEROID_WIDTH, WIN_WIDTH - ASTEROID_WIDTH) # random position on X line when spawning
                    newAsteroid = Asteroid(asteroidstartx, 20, random.choice(asteroids))
                    newAsteroid.dAsteroid() 
                    pygame.time.set_timer(ASTEROIDTIMER, random.randint(750, 1000), True)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if (time.perf_counter() - playerShip.last_fire_time) > BULLET_DELAY: #timer for firing bullets, BULLET_DELAY is in seconds
                    playerShip.last_fire_time = time.perf_counter()
                    spawnBullet = Bullet(playerShip.x + 20 , playerShip.y)
            if event.type == END_MUSIC: #when music ends, chooses another song
                play_music()
            
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: #controls
            playerShip.x -= 8
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            playerShip.x += 8
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            playerShip.y -= 8
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            playerShip.y += 8

        for asteroid in allAsteroids: 
            asteroid.hAsteroid() #drawing and deleting asteroids every frame
            if asteroid.hitbox.colliderect(playerShip.hitbox):
                if (time.perf_counter() - playerShip.last_collide_time) > HIT_DELAY: #prevents very fast collision detection
                    playerShip.last_collide_time = time.perf_counter()
                    ship_damage.play()
                    health -= 10

        for deletedasteroid in deletedAsteroids: #delete all the asteroids that have been placed in the deletedasteroids list
            allAsteroids.remove(deletedasteroid)

        for bullet in allBullets:
            bullet.hBullet()
            for asteroid in allAsteroids: 
                if bullet.hitbox.colliderect(asteroid.hitbox): #utilizing our hitboxes to detect collision between bullets and asteroids
                #if bullet.hitbox[1] - bullet.hitbox[3] < asteroid.hitbox[1] + asteroid.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > asteroid.hitbox[1]: -> ###now obsolete, used before I discovered .colliderect###
                #   if bullet.hitbox[0] + bullet.hitbox[2] > asteroid.hitbox[0] and bullet.hitbox[0] - bullet.hitbox[2]  < asteroid.hitbox[0] + asteroid.hitbox[2] / 2:
                    asteroid.hit()
                    allAsteroids.remove(asteroid)
                    allBullets.remove(bullet)

        for deletedbullet in deletedBullets: #delete all the bullets that have been placed in the deletedbullets list
            allBullets.remove(deletedbullet)

        if health == 0:
            message_display("Game over, your score: " + str(score))
            pygame.mixer.music.fadeout(500) #fades out our music on game over (also bc of END_MUSIC event also new song starts on new game)
            if score >= high_score:
                high_score = score
            score = 0
            allAsteroids = []
            allBullets = []
            playerShip = Ship(WIN_WIDTH / 2 - SHIP_WIDTH / 2, WIN_HEIGHT - SHIP_HEIGHT)
            pygame.display.update()
            time.sleep(2)
            health = 100

        draw_ui()
        playerShip.dShip()
        playerShip.hShip()
        set_level()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
    
