import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.cloud import Cloud
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.menu import Menu


class Game:
    GAME_SPEED = 20

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.GAME_SPEED
        self.game_speed2 = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.cloud = Cloud(self.game_speed2)
        self.obstacle_manager = ObstacleManager()
        self.menu = Menu('Press any key to start...', self.screen)
        self.running = False
        self.death_count = 0
        self.score = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.obstacle_manager.reset_obstacles()
        self.player.reset_dinosaur()
        self.score = 0
        self.game_speed = self.GAME_SPEED
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.cloud.update()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        if self.score % 1000 > 0 and self.score % 1000 < 499:
            self.screen.fill((255, 255, 255))
        else:
            self.screen.fill((128, 128, 128))

        self.draw_background()

        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.cloud.draw(self.screen)

        self.draw_score()
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

    def show_menu(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        self.menu.reset_screen_color(self.screen)

        if self.death_count == 0:
            self.menu.draw(self.screen)
        else:
            self.menu.update_message('new message')
            self.menu.draw(self.screen)

        self.screen.blit(ICON, (half_screen_width -
                         50, half_screen_height - 140))
        self.menu.update(self)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 2

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)
