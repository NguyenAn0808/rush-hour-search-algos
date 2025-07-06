import pygame
from screens.menu_screen import MenuScreen
from screens.loading_screen import LoadingScreen

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 640))
        pygame.display.set_caption("Rush Hour")
        pygame.display.set_icon(pygame.image.load("assets/logo.png"))
        self.clock = pygame.time.Clock()
        self.current_screen = LoadingScreen(self)

    def run(self):
        while True:
            self.current_screen.handle_input()
            self.current_screen.render()
            pygame.display.flip()
            self.clock.tick(60)

    def switch_screen(self, new_screen):
        self.current_screen = new_screen
