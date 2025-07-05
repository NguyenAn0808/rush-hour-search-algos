import pygame
from ui.button import Button
from screens.map_editor_screen import MapEditorScreen
from popups.select_level_popup import SelectLevelPopup

class SelectMapPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.message = "Chọn kiểu bản đồ"
        self.font = pygame.font.SysFont("Arial", 22)

        self.btn_custom = Button(250, 300, 200, 50, "Custom", self.on_custom)
        self.btn_default = Button(250, 370, 200, 50, "Default", self.on_default)

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), (200, 250, 320, 200), border_radius=10)
        text = self.font.render(self.message, True, (0, 0, 0))
        screen.blit(text, (270, 260))
        self.btn_custom.draw(screen)
        self.btn_default.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_custom.is_clicked(event.pos):
                self.on_custom()
            elif self.btn_default.is_clicked(event.pos):
                self.on_default()

    def on_custom(self):
        self.app.switch_screen(MapEditorScreen(self.app))

    def on_default(self):
        self.parent.popups.append(SelectLevelPopup(self.app, self.parent))
