import random
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type, 'bird')
        self.rect.y = 0
        self.index = 0
        self.bird_height()

    def bird_height(self):
        height_bird = random.randint(0, 2)
        if height_bird == 0:
            self.rect.y = 305
        elif height_bird == 1:
            self.rect.y = 240
        else:
            self.rect.y = 220
