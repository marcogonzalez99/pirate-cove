import pygame
import os

from csv import reader
from os import walk
from path import ASSET
from settings import tile_size

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)
    return cut_tiles

def import_folder(path):
    surface_list = []

    if not os.path.exists(path):
        print(f"[import_folder ERROR] Folder not found: {path}")
        return []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = os.path.join(path, image)
            try:
                image_surface = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surface)
            except Exception as e:
                print(f"[import_folder ERROR] Could not load {full_path}: {e}")
    return surface_list
