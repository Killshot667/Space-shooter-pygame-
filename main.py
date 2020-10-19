import pygame
import os
import time
import sys
import random

pygame.init()
pygame.font.init()

WIDTH = 750
HEIGHT = 750

# setting the screen
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))

# load enemy spaceships 
red_small_ship = pygame.image.load(os.path.join('assets','pixel_ship_red_small.png'))
green_small_ship = pygame.image.load(os.path.join('assets','pixel_ship_green_small.png'))
blue_small_ship = pygame.image.load(os.path.join('assets','pixel_ship_blue_small.png'))

# load player ship
main_ship = pygame.image.load(os.path.join('assets','pixel_ship_yellow.png'))

# load lasers
red_laser = pygame.image.load(os.path.join('assets','pixel_laser_red.png'))
blue_laser = pygame.image.load(os.path.join('assets','pixel_laser_blue.png'))
green_laser = pygame.image.load(os.path.join('assets','pixel_laser_green.png'))
yellow_laser = pygame.image.load(os.path.join('assets','pixel_laser_yellow.png'))

# load background
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets','background-black.png')),(WIDTH,HEIGHT))

# let the music begin :)
bulletSound = pygame.mixer.Sound(os.path.join('assets','bullet.wav'))
hitSound = pygame.mixer.Sound(os.path.join('assets','hit.wav'))

music = pygame.mixer.music.load(os.path.join('assets','music.mp3'))
pygame.mixer.music.play(-1)

class Laser:
    def __init__(self,x,y,img):
        self.x = x;
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img,(self.x,self.y))
    def move(self,vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30 # half a second as fps is 60
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.cool_down = 0
        self.lasers = []
        self.ship_img = None
        self.laser_img = None

    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_height(self):
        return self.ship_img.get_height()
    
    def get_width(self):
        return self.ship_img.get_width()

    def cooldown(self):
        if self.cool_down >= self.COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1
    
    def move_laser(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = main_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        hitSound.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.healthbar()
    
    def healthbar(self):
        pygame.draw.rect(WIN,(255,0,0),(self.x,self.y + 10 + self.get_height(), self.get_width(), 10));
        pygame.draw.rect(WIN,(0,255,0),(self.x,self.y + 10 + self.get_height(),int(self.get_width()*(self.health/self.max_health)), 10));

class Enemy(Ship):
    color_map = {"red": (red_small_ship,red_laser),"blue": (blue_small_ship,blue_laser),"green": (green_small_ship,green_laser)}
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img = self.color_map[color][0]
        self.laser_img = self.color_map[color][1]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel
        
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60 # frames per second
    level = 0
    lives = 5
    enemies = []
    enemy_vel = 1
    wave_length = 5
    lost = False
    lost_cnt = 0
    player_vel = 5
    laser_vel = 4
    player = Player(325,600)
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 70)
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(bg,(0,0))
        level_label = main_font.render(f"LEVEL: {level}",1,(255,255,255))
        lives_label = main_font.render(f"LIVES: {lives}",1,(255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw(WIN)
            
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost :(",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, 350))
        
        pygame.display.update()

    while run:
        clock.tick(FPS) # setting the fps

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_cnt += 1
        
        if lost:
            if lost_cnt > FPS*3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 7
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 50), random.randrange(-1500, -100), random.choice(["red","green","blue"]))
                enemies.append(enemy)             
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x - player_vel > 0: # move left
            player.x -= player_vel
        if keys[pygame.K_s] and player.y + player.get_height() + player_vel + 21 < HEIGHT: # move down
            player.y += player_vel
        if keys[pygame.K_d] and player.x + player.get_width() - player_vel < WIDTH: # move right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # move up
            player.y -= player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            bulletSound.play()

        
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel,player)

            if random.randrange(0, 60*3) == 1:
                enemy.shoot()
            
            if collide(enemy,player):
                enemies.remove(enemy)
                player.health -= 10
                hitSound.play()
            elif enemy.y > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        
        player.move_laser(-laser_vel,enemies)

def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicsans",75)
    while run:
        WIN.blit(bg,(0,0))
        title_label = title_font.render("Click anywhere to start", 1, (3,2,255))
        WIN.blit(title_label,(WIDTH/2 - title_label.get_width()/2,350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()


    pygame.quit() 

main_menu()