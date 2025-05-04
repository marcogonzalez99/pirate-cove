import pygame
import psutil
import os

DEBUG_PERF = False  # 🔁 Toggle ON/OFF here


class DebugHUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.process = psutil.Process(os.getpid())

    def draw(self, surface, clock, game):
        if DEBUG_PERF:
            y = 10
            info = [
                f'FPS: {int(clock.get_fps())}',
                f'Memory: {self.process.memory_info().rss // 1024**2} MB',
            ]

            if hasattr(game, "level"):
                level = game.level
                groups = {
                    'Enemies': level.enemies_sprites,
                    'Crates': level.crates_sprites,
                    'FG Palms': level.fg_palm_sprites,
                    'BG Palms': level.bg_palm_sprites,
                    'Coins': level.coin_sprites,
                    'Diamonds': level.diamond_sprites,
                    'Explosions': level.explosion_sprite,
                    'Dust': level.dust_sprite,
                }
                for name, group in groups.items():
                    if isinstance(group, pygame.sprite.Group):
                        info.append(f'{name}: {len(group)}')

            for line in info:
                text = self.font.render(line, True, 'white')
                surface.blit(text, (10, y))
                y += 20