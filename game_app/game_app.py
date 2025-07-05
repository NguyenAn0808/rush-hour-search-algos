import pygame
from screens.menu_screen import MenuScreen

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 720))
        pygame.display.set_caption("Rush Hour")
        self.clock = pygame.time.Clock()
        self.current_screen = MenuScreen(self)

    def run(self):
        while True:
            self.current_screen.handle_input()
            self.current_screen.render()
            pygame.display.flip()
            self.clock.tick(60)

    def switch_screen(self, new_screen):
        self.current_screen = new_screen
