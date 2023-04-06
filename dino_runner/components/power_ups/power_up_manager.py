import pygame
import random

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.heart import Heart


class PowerUpManager:

    def __init__(self):
        self.power_ups = []
        self.when_appears = random.randint(150, 250)
        self.duration = random.randint(3, 5)

    def generate_power_ups(self):
        power_up_type = random.randint(0, 1)
        power_up = Shield() if power_up_type == 0 else Heart()
        self.when_appears += random.randint(150, 250)
        self.power_ups.append(power_up)

    def update(self, game):
        print(self.when_appears)
        if len(self.power_ups) == 0 and self.when_appears == game.score.count:
            self.generate_power_ups()

        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect) and power_up.type != 'heart':
                power_up.start_time = pygame.time.get_ticks()
                game.player.type = power_up.type
                game.player.has_power_up = True
                game.player.power_time_up = power_up.start_time + \
                    (self.duration * 1000)
                self.power_ups.remove(power_up)
            elif game.player.dino_rect.colliderect(power_up.rect) and power_up.type == 'heart' and not power_up.counted:
                game.player.heart += 1
                power_up.counted = True

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups = []
        self.when_appears = random.randint(150, 250)
