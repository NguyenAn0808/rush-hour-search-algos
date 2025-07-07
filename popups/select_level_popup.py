import pygame
from ui.button import Button
from screens.solver_screen import SolverScreen
from model.load_map import load_map_level

class SelectLevelPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.message = "Chọn level để chơi"
        self.font = pygame.font.SysFont("Arial", 22)

        self.buttons = []
        for i in range(10):
            x = 220 + (i % 5) * 60
            y = 320 + (i // 5) * 60
            level_num = i + 1

            def make_callback(level):
                return lambda: self.select_level(level)

            self.buttons.append(
                Button(x, y, 50, 40, str(level_num), make_callback(level_num))
            )

        self.btn_back = Button(280, 450, 120, 40, "Back", self.on_back)

        print("[DEBUG] SelectLevelPopup created")

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), (180, 280, 360, 240), border_radius=10)
        text = self.font.render(self.message, True, (0, 0, 0))
        screen.blit(text, (260, 290))
        for btn in self.buttons:
            btn.draw(screen)
        self.btn_back.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn.is_clicked(event.pos):
                    btn.on_click()
            if self.btn_back.is_clicked(event.pos):
                self.btn_back.on_click()

    def select_level(self, level):
        print(f"[DEBUG] select_level called with level = {level}")
        from screens.preview_screen import PreviewLevelScreen
        node = load_map_level(level)
        level_name = f"Level {level}"
        self.app.switch_screen(PreviewLevelScreen(self.app, node, level_name))


    def on_back(self):
        self.parent.popups.remove(self)
