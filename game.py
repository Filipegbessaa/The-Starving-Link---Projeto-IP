import pygame
from menu import *
from hunger import Hunger
from Classe_player import Player, all_sprites
from score import Score
from food import Food
from game_over import Game_over
from bullets import Bullets
from enemy import Enemy
import constants


class Game:
    def __init__(self):

        # Atributo booleano que recebe a informação se o jogo está rodando
        self.running = True

        # Atributo booleano que recebe a informação se o jogo está sendo jogado
        self.playing = False

        # Tecla de iniciar o jogo ainda não foi apertada
        self.start_key = False

        self.game_display = pygame.Surface(
            (constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)
        )

        # Nome do jogo mostrado no topo da programa
        self.caption = pygame.display.set_caption(constants.GAME_CAPTION)

        # Clock do jogo
        self.clock = pygame.time.Clock()

        # Tela do jogo
        self.window = pygame.display.set_mode(
            ((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT))
        )
        self.run_game_display = False

        # Fonte padrão do pygame para usar na start menu
        self.font_name = pygame.font.get_default_font()

        # Imagem do cenário do jogo
        self.scenario_img = pygame.image.load("hirule.png")

        # Cria instâncias das classes

        self.score = Score(self.window, 0, constants.DISPLAY_WIDTH - 20, 20)
        self.hunger = Hunger(self.window)
        self.menu = Menu(self)
        self.game_over = Game_over(self)
        self.player = Player(
            constants.BLACK,
            self.hunger,
            self,
            self.game_over,
        )

        self.enemies = [Enemy(700, 600, 5, self.window)]  # Lista de inimigos na tela
        self.food_list = []  # Lista de comidas na tela

    # Método do loop do jogo. (Esse código antes ficava no projeto.py)
    def game_loop(self):

        if self.menu.run_display:
            # Checa se o jogo foi fechado ou se o enter foi apertado
            self.check_events()
            # Checa se o enter foi apertado no menu, e se sim, self.playing é setado pra True e self.menu.run_display é setado para false,
            # e assim o menu some da tela e o loop do jogo é iniciado
            self.menu.check_if_game_started()
        if self.playing:
            hunger = Hunger(self.window)
            Food.start_spawn()  # Inicia o spawn de comidas
            while not self.player.dead:
                dt = self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.player.dead = True
                        self.running = False
                        self.playing = False
                        self.menu.run_display = False
                    if (
                        event.type == Food.FOOD_SPAWN_EVENT
                    ):  # Spawna uma comida caso o evento seja chamado
                        Food.random_spawn(
                            [],
                            constants.DISPLAY_WIDTH,
                            constants.DISPLAY_HEIGHT,
                            self.window,
                        )
                self.player.shoot()
                self.player.check_hunger()
                self.player.check_lives()
                self.display_game(dt)

    # Checa se o jogo foi fechado ou se o enter foi apertado
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True
                    self.run_game_display = True

    # Escreve na tela
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_display.blit(text_surface, text_rect)

    def display_game(self, dt):
        if self.run_game_display:
            # Cenário mostrado na tela
            self.window.blit(self.scenario_img, (0, 0))
            # Player mostrado na tela
            self.player.update(dt)
            # Score mostrado na tela
            self.score.update(0)
            # Barra de fome mostrado na tela
            self.hunger.update(dt)
            # Mostrar vidas na tela
            self.player.draw_lives(
                self.window,
                constants.HUNGER_LIVES_X,
                constants.LIVES_Y,
                self.player.lives,
                self.player.lives_img,
            )
            all_sprites.update()
            # Atualiza a imagem de todas as comidas
            for food in self.food_list:
                food.update()
            # Atualiza o inimigo
            for enemy in self.enemies:
                enemy.update(self.player.coordenadas(), [] + self.enemies)
            all_sprites.draw(self.window)
            pygame.display.update()

    def retry(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over.run_display = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.hunger._curr_hungry = 100
                    self.player.lives = 5
                    self.player.dead = False
                    self.playing = True
                    self.run_game_display = True
                    self.game_over.run_display = False

                    self.player.rect.centerx = constants.DISPLAY_WIDTH / 2
                    self.player.rect.bottom = constants.DISPLAY_HEIGHT / 2

                    # TODO mandar o player pro centro da tela
                    # TODO fazer os inimigos sumirem da tela