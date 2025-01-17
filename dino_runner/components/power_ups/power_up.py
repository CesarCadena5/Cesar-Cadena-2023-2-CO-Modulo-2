import random
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH


class PowerUp(Sprite):

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(125, 180)
        self.start_time = 0
        self.counted = False

    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed

        # Si se pone en negativo el self.rect.width, se elimina el obstaculo cuando sale de la pantalla
        if self.rect.x < -self.rect.width:
            power_ups.pop()

    def draw(self, screen):
        if self.type == 'heart':
            screen.blit(self.image, (self.rect.x, 200))
        else:
            screen.blit(self.image, self.rect)
