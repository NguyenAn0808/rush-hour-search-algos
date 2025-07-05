import pygame
from screens.screen import Screen
from ui.button import Button

class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = [
            Button(260, 200, 200, 50, "Play", self.on_play),
            Button(260, 280, 200, 50, "Settings", self.on_settings),
            Button(260, 360, 200, 50, "Instructions", self.on_instructions),
            Button(260, 440, 200, 50, "Quit", self.on_quit),
        ]
        self.bg_color = (255, 230, 200)

    def render(self):
        self.app.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw(self.app.screen)
        for popup in self.popups:
            popup.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        button.on_click()
                for popup in self.popups:
                    popup.handle_input(event)

    def on_play(self):
        from popups.select_map_popup import SelectMapPopup
        self.popups.append(SelectMapPopup(self.app, self))

    def on_settings(self):
        print("⚙️ Settings clicked")

    def on_instructions(self):
        from screens.instruction_screen import InstructionScreen
        self.app.switch_screen(InstructionScreen(self.app))

    def on_quit(self):
        pygame.quit()
        exit()
