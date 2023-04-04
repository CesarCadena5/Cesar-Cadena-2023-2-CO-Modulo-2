import random
from dino_runner.components.obstacles.obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, image, type_cactus):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.cactus_height(type_cactus)

    def cactus_height(self, type_cactus):
        if type_cactus == '1':
            self.rect.y = 300
