import pygame
# How many tiles high the screen will be
vertical_tile_number = 16
# How large each tile is
tile_size = 64
# Get the Screen Height and Width
screen_height = vertical_tile_number * tile_size
screen_width = 1920

screen = pygame.display.set_mode((screen_width, screen_height))
