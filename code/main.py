import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        # Game Attributes
        self.max_level = 0
        # Player Attributes
        self.current_health = 100
        self.max_health = 100
        self.coins = 0
        self.total_coins = 0
        self.diamonds = 0
        self.score = 0
        self.enemies_stomped = 0
        self.lives = 4

        # Tutorial Logic
        self.can_press = True
        self.run_frame = 1
        self.jump_frame = 1
        self.silver_coin_frame = 0
        self.gold_coin_frame = 0
        self.diamond_frame = 1
        self.enemy_frame = 1
        # Audio
        self.overworld_music = pygame.mixer.Sound(
            '../audio/main_overworld.ogg')
        self.overworld_music.set_volume(0.4)

        self.game_over_music = pygame.mixer.Sound('../audio/game_over.ogg')
        self.game_over_music.set_volume(1)

        self.main_menu_music = pygame.mixer.Sound('../audio/main.ogg')
        self.main_menu_music.set_volume(0.5)

        self.credits_music = pygame.mixer.Sound('../audio/credits.ogg')
        self.credits_music.set_volume(0.7)

        self.tutorial_music = pygame.mixer.Sound('../audio/tutorial.ogg')
        self.tutorial_music.set_volume(0.2)

        # Zero Health Variables
        self.zero_health_timer = 0
        self.death_sound = pygame.mixer.Sound(
            '../audio/effects/player_death.wav')
        self.death_sound.set_volume(0.7)
        self.play_sound = True

        # Overworld Creation
        self.overworld = Overworld(
            0, self.max_level, screen, self.create_level)
        self.status = 'main_menu'
        self.main_menu_music.play(loops=-1)
        # User interface
        self.ui = UI(screen, self.lives)
        # Game Font
        self.game_font = pygame.font.Font('../graphics/Pixeltype.ttf', 45)
        self.tutorial_font = pygame.font.Font('../graphics/Pixeltype.ttf', 75)

    # Creates the current level, bringing in the ability to receate the overworld, manage health, coins, diamonds, score, lives and enemies stomped
    def create_level(self, current_level):
        self.overworld_music.stop()
        self.level = Level(current_level, screen, self.create_overworld,
                           self.change_coins, self.change_health, self.change_diamond, self.change_score, self.change_lives, self.count_stomped_enemies)
        # Switch status to 'level'
        self.status = 'level'

    # Creates the overworld, bringing in the ability to create levels, and switch the status to 'overworld'
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_music.play(loops=-1)

    # Keeps track of how many coins the player has collected in total and in current life
    def change_coins(self, amount):
        self.total_coins += amount
        self.coins += amount

    # Keeps track of how many diamonds the player has collected
    def change_diamond(self, count):
        self.diamonds += count

    # Keeps track of the player's score
    def change_score(self, count):
        self.score += count

    # Keeps track of how many enemies the player has killed
    def count_stomped_enemies(self):
        self.enemies_stomped += 1

    # Keeps track of how many lives the player has
    def change_lives(self, count):
        self.lives += count

    # When the player collects 100 coins, reset the count and give the player an extra life
    def extra_health(self):
        if self.coins >= 100:
            self.lives += 1
            self.coins = 0

    # Give the player health, only if their health is below 80%
    def change_health(self, amount):
        if amount > 0:
            if self.current_health <= self.max_health - 20:
                self.current_health += amount
        else:
            self.current_health += amount

    # Calculator for the final scene, takes all the stats and converts to dollars
    def total_money_earned(self):
        self.total_money = ((self.score * 10) + (self.total_coins * 10000) +
                            (self.diamonds * 500000) + (self.enemies_stomped * 10000))
        self.grade(self.total_money)
        return self.total_money

    # Grade calculator, assigns a grade depending on how much money was earned
    def grade(self, total):
        if total < 10000000:
            self.grade_earned = "F"
        if 10000000 < total < 15000000:
            self.grade_earned = "D"
        if 15000000 < total < 20000000:
            self.grade_earned = "C"
        if 20000000 < total < 25000000:
            self.grade_earned = "B"
        if 25000000 < total < 30000000:
            self.grade_earned = "A"
        if 30000000 < total < 35000000:
            self.grade_earned = "A+"
        if 35000000 < total:
            self.grade_earned = "S"

    # Game over check
    def check_game_over(self):
        # If the user has run out of lives, switch the state to gameover
        if self.lives == 0:
            self.status = 'gameover'
            self.overworld_music.stop()
            self.game_over_music.play()
            self.game_over()
        elif self.lives == 0 and self.current_health <= 0:
            self.status = 'gameover'
            self.overworld_music.stop()
            self.game_over_music.play()
            self.game_over()

    def check_zero_health(self):
        if self.lives == 0:
            self.status = 'gameover'
            self.overworld_music.stop()
            self.game_over_music.play()
            self.game_over()
        if self.current_health <= 0:
            self.level.level_music.stop()
            self.level.player_sprite.collision_rect.left = self.level.hat_sprite.rect.top + screen_width
            self.level.player_sprite.speed = 0
            self.level.player_sprite.gravity = 0
            if self.play_sound:
                self.death_sound.play(loops=1)
                self.play_sound = False
            self.zero_health_timer += 1
            if self.zero_health_timer > 245:
                self.change_lives(-1)
                self.death_sound.stop()
                self.current_health = 100
                self.zero_health_timer = 0
                self.overworld = Overworld(
                    self.max_level, self.max_level, screen, self.create_level)
                self.status = 'overworld'
                self.overworld_music.play(loops=-1)
                self.play_sound = True

    # Restarts the game from scratch

    def restart_game(self):
        # Fresh state of the game
        self.current_health = 100
        self.coins = 0
        self.total_coins = 0
        self.diamonds = 0
        self.score = 0
        self.enemies_stomped = 0
        self.lives = 6
        # Level Checkpoints if the player gets a game over and chooses to restart
        # Player starts at the beginning of the farthest world completed
        if self.max_level < 6:
            self.max_level = 0
        elif 6 < self.max_level < 11:
            self.max_level = 6
        elif 12 < self.max_level <= 17:
            self.max_level = 12
        elif 18 < self.max_level:
            self.max_level = 18
        self.overworld_music.play(loops=-1)
        self.overworld = Overworld(
            self.max_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    # Checks to see if the game has been completed
    def check_completion(self):
        if self.max_level == 20:
            self.status = "end_game"
            self.credits_music.play(loops=-1)

    # Game Over State
    def game_over(self):
        # Display all the game over assets
        bg = pygame.image.load(
            '../graphics/overworld/main_menu.png').convert_alpha()
        screen.blit(bg, (0, 0))

        game_over_photo_1 = pygame.image.load(
            '../graphics/overworld/game_over_1.png').convert_alpha()

        game_over_photo_2 = pygame.image.load(
            '../graphics/overworld/game_over_2.png').convert_alpha()

        game_over_1_rect = game_over_photo_1.get_rect(
            center=(screen_width/2, screen_height/2 - 75))
        screen.blit(game_over_photo_1, game_over_1_rect)

        game_over_2_rect = game_over_photo_2.get_rect(
            center=(screen_width/2, screen_height/2 + 100))
        screen.blit(game_over_photo_2, game_over_2_rect)

        # Restart the game when the player gets a game over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_over_music.stop()
            self.restart_game()

    # Main Menu state
    def main_menu(self):
        bg = pygame.image.load(
            '../graphics/overworld/main_menu.png').convert_alpha()
        screen.blit(bg, (0, 0))

        intro_photo_1 = pygame.image.load(
            '../graphics/overworld/main_menu_1.png').convert_alpha()

        intro_photo_2 = pygame.image.load(
            '../graphics/overworld/main_menu_2.png').convert_alpha()

        intro_1_rect = intro_photo_1.get_rect(
            center=(screen_width/2, screen_height/2 - 75))
        screen.blit(intro_photo_1, intro_1_rect)

        intro_2_rect = intro_photo_2.get_rect(
            center=(screen_width/2, screen_height/2 + 125))
        screen.blit(intro_photo_2, intro_2_rect)

        # Launch the tutorial from the main menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_press:
            self.main_menu_music.stop()
            self.tutorial_music.play(loops=-1)
            self.status = 'tutorial'
            self.can_press = False

    # Tutorial State
    def tutorial(self):
        # To Prevent the player from accidentally Advancing
        self.can_press = True
        # Fill the Screen
        screen.fill((30, 30, 30))
        # Increment Frames
        self.run_frame += 0.15
        if self.run_frame > 6:
            self.run_frame = 1
        self.jump_frame += 0.15
        if self.jump_frame > 3:
            self.jump_frame = 1
        self.silver_coin_frame += 0.15
        if self.silver_coin_frame > 3:
            self.silver_coin_frame = 0
        self.gold_coin_frame += 0.15
        if self.gold_coin_frame > 3:
            self.gold_coin_frame = 0
        self.diamond_frame += 0.15
        if self.diamond_frame > 5:
            self.diamond_frame = 1
        self.enemy_frame += 0.15
        if self.enemy_frame > 6:
            self.enemy_frame = 1
        # Tutorial Info Here
        tut_text = self.tutorial_font.render(
            "How to Play", False, 'white')
        tut_text_rect = tut_text.get_rect(
            center=(screen_width/2, 100))
        screen.blit(tut_text, tut_text_rect)

        # Move
        move_text = self.game_font.render(
            "Press D/Right and A/Left To Move", False, 'white')
        move_text_rect = move_text.get_rect(
            center=(screen_width/4, 200))
        screen.blit(move_text, move_text_rect)
        # Move Image
        move_image = pygame.image.load(
            f'../graphics/character/run/{int(self.run_frame)}.png')
        move_image_rect = move_image.get_rect(
            center=(screen_width/4, 275))
        screen.blit(move_image, move_image_rect)

        # Jump
        jump_text = self.game_font.render(
            "Press W/Space/Up to Jump", False, 'white')
        jump_text_rect = jump_text.get_rect(
            center=(screen_width - screen_width/4, 200))
        screen.blit(jump_text, jump_text_rect)
        # Jump Image
        jump_image = pygame.image.load(
            f'../graphics/character/jump/{int(self.jump_frame)}.png')
        jump_image_rect = jump_image.get_rect(
            center=(screen_width - screen_width/4, 275))
        screen.blit(jump_image, jump_image_rect)

        # Coins
        coin_tut_text = self.game_font.render(
            "Collect Coins for Points ", False, 'white')
        coin_tut_text_rect = coin_tut_text.get_rect(
            center=(screen_width/4, 400))
        screen.blit(coin_tut_text, coin_tut_text_rect)
        # Coin Image
        coin_image = pygame.image.load(
            f'../graphics/coins/silver/{int(self.silver_coin_frame)}.png')
        coin_image_rect = coin_image.get_rect(
            center=(screen_width/4 + 100, 475))
        screen.blit(coin_image, coin_image_rect)
        coin_2_image = pygame.image.load(
            f'../graphics/coins/gold/{int(self.gold_coin_frame)}.png')
        coin_2_image_rect = coin_2_image.get_rect(
            center=(screen_width/4 - 100, 475))
        screen.blit(coin_2_image, coin_2_image_rect)
        # Coin Value Texts
        silver_value_text = self.game_font.render(
            "+200 Points", False, 'white')
        silver_value_text_rect = silver_value_text.get_rect(
            center=(screen_width/4 + 100, 525))
        screen.blit(silver_value_text, silver_value_text_rect)
        gold_value_text = self.game_font.render(
            "+1000 Points ", False, 'white')
        gold_value_text_rect = gold_value_text.get_rect(
            center=(screen_width/4 - 100, 525))
        screen.blit(gold_value_text, gold_value_text_rect)

        # Diamonds
        diamond_tut_text = self.game_font.render(
            "Collect Diamonds for Points", False, 'white')
        diamond_tut_text_rect = diamond_tut_text.get_rect(
            center=(screen_width - screen_width/4, 400))
        screen.blit(diamond_tut_text, diamond_tut_text_rect)
        # Diamond Image
        diamond_image = pygame.image.load(
            f'../graphics/coins/diamond/{int(self.diamond_frame)}.png')
        diamond_image_rect = diamond_image.get_rect(
            center=(screen_width - screen_width/4, 475))
        screen.blit(diamond_image, diamond_image_rect)
        # Diamond Value Text
        diamond_value_text = self.game_font.render(
            "+5000 Points ", False, 'white')
        diamond_value_text_rect = diamond_value_text.get_rect(
            center=(screen_width - screen_width/4, 525))
        screen.blit(diamond_value_text, diamond_value_text_rect)

        # Hat
        hat_text = self.game_font.render(
            "Reach the Hat to Complete The Level", False, 'white')
        hat_text_rect = hat_text.get_rect(
            center=(screen_width/4, 600))
        screen.blit(hat_text, hat_text_rect)
        # Hat Image
        hat_image = pygame.image.load('../graphics/overworld/hat.png')
        hat_image_rect = hat_image.get_rect(
            center=(screen_width/4, 675))
        screen.blit(hat_image, hat_image_rect)
        # Hat Value Text
        hat_value_text = self.game_font.render(
            "+10000 Points ", False, 'white')
        hat_value_text_rect = hat_value_text.get_rect(
            center=(screen_width/4, 725))
        screen.blit(hat_value_text, hat_value_text_rect)

        # Objective Text
        obj_text = self.game_font.render(
            "Earn the Most Money, by collecting as many points as possible", False, 'white')
        obj_text_rect = obj_text.get_rect(
            center=(screen_width/2, 800))
        screen.blit(obj_text, obj_text_rect)

        # Enemies
        enemy_text = self.game_font.render(
            "Stomp on Enemies to Kill Them", False, 'white')
        enemy_text_rect = enemy_text.get_rect(
            center=(screen_width - screen_width/4, 600))
        screen.blit(enemy_text, enemy_text_rect)
        # Enemy Image
        enemy_image = pygame.image.load(
            f'../graphics/enemy/run/{int(self.enemy_frame)}.png')
        enemy_image_rect = enemy_image.get_rect(
            center=(screen_width - screen_width/4, 675))
        screen.blit(enemy_image, enemy_image_rect)
        # Enemy Value Text
        enemy_value_text = self.game_font.render(
            "+1000 Points ", False, 'white')
        enemy_value_text_rect = enemy_value_text.get_rect(
            center=(screen_width - screen_width/4, 725))
        screen.blit(enemy_value_text, enemy_value_text_rect)

        # Tell the player how to continue
        continue_text = self.tutorial_font.render(
            "Press W to Start", False, 'white')
        continue_text_rect = continue_text.get_rect(
            center=(screen_width/2, 900))
        screen.blit(continue_text, continue_text_rect)
        # Launch the game from the main menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.can_press:
            self.can_press = False
            self.tutorial_music.stop()
            self.restart_game()

    # Credits State
    def end_game(self):
        screen.fill((30, 30, 30))
        # Thank you Font
        end_text = self.game_font.render(
            "Thank You for Playing", False, 'white')
        end_text_rect = end_text.get_rect(
            center=(screen_width/2, screen_height/2 - 400))
        screen.blit(end_text, end_text_rect)

        # Display the final score
        score_text = self.game_font.render(
            f"Total Score: {self.score:,}", False, 'white')
        score_text_rect = score_text.get_rect(
            center=(screen_width/2, screen_height/2 - 350))
        screen.blit(score_text, score_text_rect)

        # Display Total Coins Collected
        coin_text = self.game_font.render(
            f"Total Coins Collected: {self.total_coins}", False, 'white')
        coin_text_rect = coin_text.get_rect(
            center=(screen_width/2, screen_height/2 - 300))
        screen.blit(coin_text, coin_text_rect)

        # Display Total Diamonds Collected
        self.end_text = self.game_font.render(
            f"Total Diamonds Collected: {self.diamonds}", False, 'white')
        self.end_text_rect = self.end_text.get_rect(
            center=(screen_width/2, screen_height/2 - 250))
        screen.blit(self.end_text, self.end_text_rect)

        # Display Total NUmver of Enemies Stomped On
        self.end_text = self.game_font.render(
            f"Total Enemies Stomped On: {self.enemies_stomped}", False, 'white')
        self.end_text_rect = self.end_text.get_rect(
            center=(screen_width/2, screen_height/2 - 200))
        screen.blit(self.end_text, self.end_text_rect)

        # Display the Title for Money Stolen
        self.money_text = self.game_font.render(
            f"Money Stolen", False, 'white')
        self.money_text_rect = self.money_text.get_rect(
            center=(screen_width/2, screen_height/2))
        screen.blit(self.money_text, self.money_text_rect)

        # Calculate and display how much money the SCORE awarded the player
        self.money_score_text = self.game_font.render(
            f"Score: {self.score} x $10 = ${self.score * 10:,}", False, 'white')
        self.money_score_text_rect = self.money_score_text.get_rect(
            center=(screen_width/2, screen_height/2 + 50))
        screen.blit(self.money_score_text, self.money_score_text_rect)

        # Calculate and display how much money the COINS awarded the player
        self.money_coins_text = self.game_font.render(
            f"Coins: {self.total_coins} x $10,000 = ${self.total_coins * 10000:,}", False, 'white')
        self.money_coins_text_rect = self.money_coins_text.get_rect(
            center=(screen_width/2, screen_height/2 + 100))
        screen.blit(self.money_coins_text, self.money_coins_text_rect)

        # Calculate and display how much money the DIAMONDS awarded the player
        self.money_diamonds_text = self.game_font.render(
            f"Diamonds: {self.diamonds} x $500,000 = ${self.diamonds * 500000:,}", False, 'white')
        self.money_diamonds_text_rect = self.money_diamonds_text.get_rect(
            center=(screen_width/2, screen_height/2+150))
        screen.blit(self.money_diamonds_text, self.money_diamonds_text_rect)

        # Calculate and display how much money the ENEMIES awarded the player
        self.money_enemies_text = self.game_font.render(
            f"Stolen From Enemies: {self.enemies_stomped} x $10,000 = ${self.enemies_stomped * 10000:,}", False, 'white')
        self.money_enemies_text_rect = self.money_enemies_text.get_rect(
            center=(screen_width/2, screen_height/2+200))
        screen.blit(self.money_enemies_text, self.money_enemies_text_rect)

        # Calculate and display the total amount of money earned
        self.money_total_text = self.game_font.render(
            f"Total: ${self.total_money_earned():,}", False, 'white')
        self.money_total_text_rect = self.money_total_text.get_rect(
            center=(screen_width/2, screen_height/2+250))
        screen.blit(self.money_total_text, self.money_total_text_rect)

        # Calculate and display the grade awarded to the player
        self.grade_text = self.game_font.render(
            f"Grade: {self.grade_earned}", False, 'white')
        self.grade_text_rect = self.grade_text.get_rect(
            center=(screen_width/2, screen_height/2+350))
        screen.blit(self.grade_text, self.grade_text_rect)

    # Run the game depending on the state
    def run(self):
        # Running the main menu
        if self.status == 'main_menu':
            self.main_menu()
        elif self.status == 'tutorial':
            self.tutorial()
        # Running the overworld
        elif self.status == 'overworld':
            self.overworld.run()
        # Running the Final Scene of the Game
        elif self.status == 'end_game':
            self.overworld_music.stop()
            self.end_game()
        # Running the Game Over Screen
        elif self.status == 'gameover':
            self.game_over()
        # Running the Level
        else:
            self.level.run()
            self.extra_health()
            self.check_zero_health()
            self.check_game_over()
            self.check_completion()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_score(self.score)
            self.ui.display_lives(self.lives)
            self.ui.show_coins(self.coins)
            self.ui.show_diamonds(self.diamonds)


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode(
    (screen_width, screen_height))
pygame.display.set_caption("Pirate's Cove")
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Hide the mouse, run the whole game
    pygame.mouse.set_visible(False)
    game.run()

    pygame.display.update()
    clock.tick(74)
