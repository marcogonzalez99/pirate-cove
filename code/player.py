import pygame
import os

from path import ASSET
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assets()
        # Player Animations
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Dust Particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        self.create_jump_particles = create_jump_particles
        # Player Movement
        self.speed = 8
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -19
        self.collision_rect = pygame.Rect(
            self.rect.topleft, (50, self.rect.height))

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.level_won = False

        # Health Management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 600
        self.hurt_time = 0

        # Audio
        # self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.ogg')
        self.jump_sound = pygame.mixer.Sound(ASSET('audio', 'effects', 'hit.wav'))
        self.hit_sound = pygame.mixer.Sound(ASSET('audio', 'effects', 'hit.wav'))

        self.jump_sound.set_volume(0.25)
        self.hit_sound.set_volume(0.2)

    def import_character_assets(self):
        # Import the graphics for the player
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = ASSET('graphics', 'character', animation)
            self.animations[animation] = import_folder(full_path)


    def import_dust_run_particles(self):
        # Import dust particles for the player
        self.dust_run_particles = import_folder(ASSET('graphics', 'character', 'dust_particles', 'run'))

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def animate(self):
        animation = self.animations[self.status]

        # Loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
        # Move the payer based on input
        keys = pygame.key.get_pressed()
        if not self.level_won:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

            if keys[pygame.K_w] and self.on_ground or keys[pygame.K_SPACE] and self.on_ground or keys[pygame.K_UP] and self.on_ground:
                self.jump()
                self.create_jump_particles(self.rect.midbottom)
        else:
            self.speed = 0
            self.direction.x = 0

    def get_status(self):
        # Determine what state the player is in, to run different player animations
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        # Move character based on gravity
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        # Jumping
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        # If the player takes damage, reduce health,make invincible and play a sound
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-20)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def get_health(self):
        # Earn health upon level competion
        self.change_health(20)

    def invinciblity_timer(self):
        # Set invincibility frames so the player can't take damage
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invinciblity_timer()
        self.wave_value()
