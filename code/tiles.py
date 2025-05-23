import pygame

from path import ASSET
from support import import_folder

# Standard Tile Parameters
class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

# For tiles that wont move
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

# Specifically for crate tiles
class Crate(StaticTile):
    def __init__(self, size, x, y):
        crate_image = pygame.image.load(
            ASSET('graphics', 'terrain', 'crate.png')
        ).convert_alpha()
        super().__init__(size, x, y, crate_image)

        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

# For animated tiles, standard animation function runs
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

# For coins, to center them on the tile and assign a value
class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y + int(size/2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value

# For Diamonds, center them and give them a value
class Diamond(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y + int(size/2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value

# Animated background and foreground palm trees
class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y-offset
        self.rect.topleft = (x, offset_y)