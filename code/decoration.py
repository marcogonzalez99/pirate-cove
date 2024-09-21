import pygame
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint


class Sky:
    def __init__(self, horizon, world, style='level'):
        self.world = world
        # Based on the current world the player is on, the sky will be a different
        # color
        if world == 0:
            self.top = pygame.image.load(
                '../graphics/decoration/sky/world_1_sky_top.png').convert_alpha()
            self.bottom = pygame.image.load(
                '../graphics/decoration/sky/world_1_sky_bottom.png').convert_alpha()
            self.middle = pygame.image.load(
                '../graphics/decoration/sky/world_1_sky_middle.png').convert_alpha()
        if world == 1:
            self.top = pygame.image.load(
                '../graphics/decoration/sky/world_2_sky_top.png').convert_alpha()
            self.bottom = pygame.image.load(
                '../graphics/decoration/sky/world_2_sky_bottom.png').convert_alpha()
            self.middle = pygame.image.load(
                '../graphics/decoration/sky/world_2_sky_middle.png').convert_alpha()
        if world == 2:
            self.top = pygame.image.load(
                '../graphics/decoration/sky/world_3_sky_top.png').convert_alpha()
            self.bottom = pygame.image.load(
                '../graphics/decoration/sky/world_3_sky_bottom.png').convert_alpha()
            self.middle = pygame.image.load(
                '../graphics/decoration/sky/world_3_sky_middle.png').convert_alpha()
        if world == 3:
            self.top = pygame.image.load(
                '../graphics/decoration/sky/world_x_sky_top.png').convert_alpha()
            self.bottom = pygame.image.load(
                '../graphics/decoration/sky/world_x_sky_bottom.png').convert_alpha()
            self.middle = pygame.image.load(
                '../graphics/decoration/sky/world_x_sky_middle.png').convert_alpha()

        self.horizon = horizon

        # Stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(
            self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(
            self.middle, (screen_width, tile_size))

        self.style = style
        # Setting the sky for the overworld, randomly placing palm trees and clouds around
        if self.style == 'overworld':
            if self.world == 0:
                palm_surface = import_folder(
                    '../graphics/overworld/palms/world_1')
                self.palms = []

                for surface in [choice(palm_surface) for image in range(10)]:
                    x = randint(0, screen_width)
                    y = (self.horizon * tile_size) + randint(50, 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.palms.append((surface, rect))

                clouds_surface = import_folder(
                    '../graphics/overworld/clouds/world_1')
                self.clouds = []

                for surface in [choice(clouds_surface) for image in range(15)]:
                    x = randint(0, screen_width)
                    y = randint(0, (self.horizon * tile_size) - 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.clouds.append((surface, rect))
            if self.world == 1:
                palm_surface = import_folder(
                    '../graphics/overworld/palms/world_2')
                self.palms = []

                for surface in [choice(palm_surface) for image in range(10)]:
                    x = randint(0, screen_width)
                    y = (self.horizon * tile_size) + randint(50, 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.palms.append((surface, rect))

                clouds_surface = import_folder(
                    '../graphics/overworld/clouds/world_2')
                self.clouds = []

                for surface in [choice(clouds_surface) for image in range(15)]:
                    x = randint(0, screen_width)
                    y = randint(0, (self.horizon * tile_size) - 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.clouds.append((surface, rect))
            if self.world == 2:
                palm_surface = import_folder(
                    '../graphics/overworld/palms/world_3')
                self.palms = []

                for surface in [choice(palm_surface) for image in range(10)]:
                    x = randint(0, screen_width)
                    y = (self.horizon * tile_size) + randint(50, 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.palms.append((surface, rect))

                clouds_surface = import_folder(
                    '../graphics/overworld/clouds/world_3')
                self.clouds = []

                for surface in [choice(clouds_surface) for image in range(15)]:
                    x = randint(0, screen_width)
                    y = randint(0, (self.horizon * tile_size) - 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.clouds.append((surface, rect))
            if self.world == 3:
                palm_surface = import_folder(
                    '../graphics/overworld/palms/world_x')
                self.palms = []

                for surface in [choice(palm_surface) for image in range(10)]:
                    x = randint(0, screen_width)
                    y = (self.horizon * tile_size) + randint(50, 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.palms.append((surface, rect))

                clouds_surface = import_folder(
                    '../graphics/overworld/clouds/world_x')
                self.clouds = []

                for surface in [choice(clouds_surface) for image in range(10)]:
                    x = randint(0, screen_width)
                    y = randint(0, (self.horizon * tile_size) - 100)
                    rect = surface.get_rect(midbottom=(x, y))
                    self.clouds.append((surface, rect))

    def draw(self, surface):
        # Drawing the sky
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])

# This draws the water at the bottom of the screen of every level


class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int(
            (level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, '../graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surface_list = import_folder('../graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        # Randomly place the clouds around the level
        for cloud in range(cloud_number):
            cloud = choice(cloud_surface_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
