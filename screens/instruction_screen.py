import pygame
from screens.screen import Screen
from ui.button import Button

class InstructionScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.message = "Welcome to Rush Hour!\nGoal: Move the RED car out of the board."
        self.button_back = Button(20, 600, 100, 40, "Back", self.on_back)
        self.font = pygame.font.SysFont("Arial", 22)

    def render(self):
        self.app.screen.fill((230, 250, 250))
        lines = self.message.split("\n")
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (0, 0, 0))
            self.app.screen.blit(text, (50, 100 + i * 30))
        self.button_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_back.is_clicked(event.pos):
                    self.on_back()

    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))
