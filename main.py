import pygame
import os
import time
import sys

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
bg = pygame.image.load(os.path.join('assets','background-black.png'))


