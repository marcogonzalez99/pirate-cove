import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)
        
    # Move the enemies in the map at a select speed
    def move(self):
        self.rect.x += self.speed
    
    # Get the reverse image of the enemy if they are going a positive direction
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
            
    # Reverse the direction of the enemy when they collide with the "collision block"
    def reverse(self):
        self.speed *= -1
        
    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()