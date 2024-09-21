import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width, screen
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm, Diamond
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health, change_diamond, change_score, change_lives, stomped_enemies):
        # General Setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # Overworld Connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.create_player(player_layout, change_health)

        # User Interface
        self.change_coins = change_coins
        self.change_diamond = change_diamond
        self.change_score = change_score
        self.change_lives = change_lives
        self.change_health = change_health
        self.count_stomped = stomped_enemies
        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        # Explosion Particle
        self.explosion_sprite = pygame.sprite.Group()

        # Sound Effects
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.1)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.3)
        self.death_sound = pygame.mixer.Sound(
            '../audio/effects/player_death.wav')
        self.death_sound.set_volume(0.7)
        self.level_clear_sound = pygame.mixer.Sound(
            '../audio/effects/level_clear.wav')
        self.level_clear_sound.set_volume(0.15)

        # Death Timer
        self.death_timer = 0
        self.play_sound = True

        # Win Timer
        self.win_timer = 0

        # Music - Initialized from Game_Data
        self.level_music = pygame.mixer.Sound(level_data['music'])
        self.level_music.play(loops=-1)
        self.level_music.set_volume(0.5)

        # Terrain setup for World 1
        if 0 <= self.current_level <= 5:
            terrain_layout = import_csv_layout(level_data['terrain'])
            self.terrain_sprites = self.create_tile_group(
                terrain_layout, 'terrain')
        # Terrtain setup for World 2
        elif 6 <= self.current_level <= 11:
            terrain_layout = import_csv_layout(level_data['sand_terrain'])
            self.terrain_sprites = self.create_tile_group(
                terrain_layout, 'sand_terrain')
        # Terrain setup for World 3
        elif 12 <= self.current_level <= 17:
            terrain_layout = import_csv_layout(level_data['soft_terrain'])
            self.terrain_sprites = self.create_tile_group(
                terrain_layout, 'soft_terrain')
        # Terrain setup for World x
        if 17 < self.current_level < 20:
            terrain_layout = import_csv_layout(level_data['terrain'])
            self.terrain_sprites = self.create_tile_group(
                terrain_layout, 'terrain')

        # Grass Setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crates Setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # Diamonds
        diamond_layout = import_csv_layout(level_data['diamond'])
        self.diamond_sprites = self.create_tile_group(
            diamond_layout, 'diamond')

        # Foreground Palms
        fg_palms_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(
            fg_palms_layout, 'fg palms')

        # Background Palms
        bg_palms_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(
            bg_palms_layout, 'bg palms')

        # Enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(
            constraint_layout, 'constraints')

        # Decorations
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 50)

        # Different Skies depending on the level
        if self.current_level < 6:
            self.sky = Sky(8, 0)
        elif 6 <= self.current_level <= 11:
            self.sky = Sky(8, 1)
        elif 12 <= self.current_level <= 17:
            self.sky = Sky(8, 2)
        else:
            self.sky = Sky(8, 3)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        # Iterate through the csv and determine what tile is being detected
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # Terrain Manager
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            "../graphics/terrain/terrain_tiles.png")
                        tile_surface = (terrain_tile_list[int(val)])
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'sand_terrain':
                        terrain_tile_list = import_cut_graphics(
                            "../graphics/terrain/rock_sand_tiles.png")
                        tile_surface = (terrain_tile_list[int(val)])
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'soft_terrain':
                        terrain_tile_list = import_cut_graphics(
                            "../graphics/terrain/soft_sand_tiles.png")
                        tile_surface = (terrain_tile_list[int(val)])
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    # Grass Manager
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            "../graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    # Crate Manager
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)
                    # Coin Manager
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y,
                                          '../graphics/coins/gold', 5)
                        if val == '1':
                            sprite = Coin(tile_size, x, y,
                                          '../graphics/coins/silver', 1)
                    # Diamond Manager
                    if type == 'diamond':
                        if val == '0':
                            sprite = Diamond(
                                tile_size, x, y, '../graphics/coins/diamond', 1)
                    # Palm Tree Manager
                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y,
                                          '../graphics/terrain/palm_small', 38)
                        if val == '1':
                            sprite = Palm(tile_size, x, y,
                                          '../graphics/terrain/palm_large', 70)
                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y,
                                      '../graphics/terrain/palm_bg', 62)
                    # Enemy Manager
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group

    # Find on the csv layout where there is a player tile, to spanw the player and the goal
    def create_player(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # Where to spawn the player
                if val == '0':
                    self.player_sprite = Player((x, y), self.display_surface,
                                                self.create_jump_particles, change_health)
                    self.player.add(self.player_sprite)
                # Where to spawn the end goal
                if val == '1':
                    hat_surface = pygame.image.load(
                        "../graphics/character/hat.png").convert_alpha()
                    self.hat_sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(self.hat_sprite)

    # Flip the enemy around when they collide with the constraints
    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprites:
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # Creates a jump particle whenever the player jumps
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # Determine the collision logic for horizontal movement
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites(
        ) + self.crates_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    # Determine the collision logic for vertical movement
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites(
        ) + self.crates_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    # Scrolling the map when the player reaches the limits
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # Determine if the player is on the ground or not
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # Find where the player landed and generate a dist sprite
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(
                self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    # Check if the player has fallen off the map
    def check_death(self):
        # Where the detection occurs
        if self.player.sprite.rect.bottom > screen_height + 50:
            self.player_sprite.speed = 0
            self.world_shift = 0
            if self.play_sound:
                self.death_sound.play(loops=1)
                self.play_sound = False
            # Stop playing the level music, and start the timer
            self.level_music.stop()
            self.death_timer += 1
            # Manually stop the death sound
            if self.death_timer > 245:
                self.death_sound.stop()
            # Reset the timer, lose a life, and create the overworld with no new levels
                self.death_timer = 0
                self.change_lives(-1)
                self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            # Disables the players ability to move
            self.player.sprite.level_won = True
            # Teleports the player to the flag, keeping collision to True
            self.player_sprite.collision_rect.midbottom = self.hat_sprite.rect.midbottom
            # Stop the music, play the level clear sound, and run the run_win()
            self.level_music.stop()
            self.level_clear_sound.play(loops=-1)
            self.run_win()

    def run_win(self):
        # Increment the timer
        self.win_timer += 1
        if self.win_timer > 250:
            # When the timer reaches 250, force stop the sound to avoid repitition
            self.level_clear_sound.stop()
        if self.win_timer > 300:
            # When the timer reaches 350, reset it, add points to the score, and health, and rebuild the overworld with a new level
            self.win_timer = 0
            self.change_score(10000)
            self.change_health(20)
            # Rebuilds the overworld, placing the player on the level they just completed and incrementing the new max level by 1
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        # Check for and destroy any coins the player comes into contact with
        collided_coins = pygame.sprite.spritecollide(
            self.player.sprite, self.coin_sprites, True)
        # If a coin has been collided with, play a sound
        if collided_coins:
            self.coin_sound.play()
            # Every coin, adds to total coin count as well as to the score
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.change_score(coin.value * 200)

    def check_diamond_collisions(self):
        # Check for ans destroy any diamond the player comes into contact with
        collided_diamond = pygame.sprite.spritecollide(
            self.player.sprite, self.diamond_sprites, True)
        if collided_diamond:
            # If a diamond has been collided with, play a sound
            self.coin_sound.play()
            for diamond in collided_diamond:
                # Every diamond, adds to total diamonds as well as awards 5000 points to the player
                self.change_diamond(diamond.value)
                self.change_score(diamond.value * 5000)

    def check_enemy_collisions(self):
        # Checks for and destroys any enemy the player defeats
        enemy_collisions = pygame.sprite.spritecollide(
            self.player.sprite, self.enemies_sprites, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                # Set a few checks
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                # Detect if a proper collision has been made2
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -20
                    explosion_sprite = ParticleEffect(
                        enemy.rect.center, 'explosion')
                    self.explosion_sprite.add(explosion_sprite)
                    self.stomp_sound.play()
                    self.change_score(1000)
                    self.count_stomped()
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def draw_arrow(self):
        if self.player.sprite.rect.bottom < 0:
            arrow_drawing = pygame.image.load(
                "../graphics/overworld/arrow.png").convert_alpha()
            arrow_rect = arrow_drawing.get_rect(
                center=(self.player_sprite.rect.centerx, 15))
            screen.blit(arrow_drawing, arrow_rect)

    def exit_level(self):
        # Check for if the Escape key is hit, if it is, remake the overworld, without making a new level avaialable
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and self.player_on_ground:
            self.level_music.stop()
            self.create_overworld(self.current_level, 0)

    def skip_level(self):
        # F This Level Easter Egg
        # Check for if the F, T, and L key are being pressed while on the ground, if so, remake the overworld with the next level available
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and keys[pygame.K_t] and keys[pygame.K_l] and self.player_on_ground:
            self.change_score(-100000)
            self.level_music.stop()
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):
        # Run the whole game
        # Decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        # BG Palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)
        # Dust Particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        # Terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        # Enemy
        self.enemies_sprites.update(self.world_shift)
        self.enemies_sprites.draw(self.display_surface)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.explosion_sprite.update(self.world_shift)
        self.explosion_sprite.draw(self.display_surface)
        # Crate
        self.crates_sprites.draw(self.display_surface)
        self.crates_sprites.update(self.world_shift)
        # Grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)
        # Coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        # Diamonds
        self.diamond_sprites.update(self.world_shift)
        self.diamond_sprites.draw(self.display_surface)
        # FG Palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # Player Sprite
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.player.draw(self.display_surface)
        self.scroll_x()
        self.draw_arrow()
        # Player Goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Overworld Checks
        self.check_death()
        self.check_win()
        self.exit_level()
        self.skip_level()

        # Coins
        self.check_coin_collisions()
        self.check_diamond_collisions()
        self.check_enemy_collisions()
        # Water
        self.water.draw(self.display_surface, self.world_shift)
