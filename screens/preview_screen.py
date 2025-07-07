import pygame
from screens.screen import Screen
from ui.button import Button
from screens.solver_screen import SolverScreen

class PreviewLevelScreen(Screen):
    def __init__(self, app, node, level_name="Preview"):
        super().__init__(app)
        self.node = node
        self.level_name = level_name

        self.font = pygame.font.SysFont("Arial", 26, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 18)

        self.button_start = Button(250, 540, 100, 40, "Start", self.on_start)
        self.button_back = Button(370, 540, 100, 40, "Back", self.on_back)

        print(f"[DEBUG] Preview screen loaded for {level_name}")

    def render(self):
        self.app.screen.fill((245, 235, 215))

        # Draw title
        title_text = self.font.render(f"Preview: {self.level_name}", True, (0, 0, 0))
        self.app.screen.blit(title_text, (self.app.screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Draw preview board (reuse from SolverScreen)
        from screens.solver_screen import SolverScreen
        SolverScreen.draw_board(self, self.node)

        # Buttons
        self.button_start.draw(self.app.screen)
        self.button_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_start.is_clicked(event.pos):
                    self.on_start()
                elif self.button_back.is_clicked(event.pos):
                    self.on_back()

    def on_start(self):
        self.app.switch_screen(SolverScreen(self.app, self.node, self.level_name))

    def on_back(self):
        from popups.select_level_popup import SelectLevelPopup
        self.parent.popups.append(SelectLevelPopup(self.app, self.parent))
        self.app.switch_screen(self.parent)  # go back to previous
