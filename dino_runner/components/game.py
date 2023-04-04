import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.cloud import Cloud
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.player = Dinosaur()
        self.cloud = Cloud(self.game_speed)
        self.font = pygame.font.SysFont("gillsans", 20)
        self.obstacle_manager = ObstacleManager()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.cloud.update()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.cloud.draw(self.screen)

        self.score()
        # Actualiza la pantalla
        pygame.display.update()

        # Este actualiza el contenido de la pantalla, pero se usa cuando pygame usa banderas
        # pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        # Acá pone una primera imagen, que es la que arranca en X:0 y Y:380, si se quita, empieza en blanco el fondo del piso un pedazo
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        # Acá, despues de que termine de mostrar la primera imagen, se concatena esta segunda, por eso se suma el tamaño
        # de la imagen + el x_pos_bg, por eso si se comenta la linea anterior, esta segunda imagen sale cuando el img_width se cumpla
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        # Acá se verifica en negativo, para que la imagen vaya hacia atrás. El image_width se pasa a negativo -2024 y el x_pos_bg también
        if self.x_pos_bg <= -image_width:
            # Cuando ya el x_pos_bg se cumpla, se le pega otra imagen y se reinicia el x_pos_bg a 0
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        # Acá se pasa a negativo el x_pos_bg
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1

        score = self.font.render(
            "Score: " + str(self.points), True, (0, 0, 255))
        score_rect = score.get_rect()
        score_rect.center = (900, 40)
        self.screen.blit(score, score_rect)
