import pygame
from game import Game

pygame.init()

game = Game()
pygame.mixer.music.set_volume(0.2)
music = pygame.mixer.music.load("./Sounds/song_of_time.ogg")
pygame.mixer.music.play(-1)
while game.running:
    game.menu.display_menu()
    game.game_loop()
    game.game_over.game_over()
