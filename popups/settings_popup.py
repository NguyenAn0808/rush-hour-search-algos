import pygame
from ui.button import Button
from ui.icon_button import IconButton
from screens.menu_screen import MenuScreen

class SettingsPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.message = "Settings"
        self.volume = 50

        self.btn_close = Button(300, 430, 120, 40, "Close", self.on_close)
        # self.btn_sound = IconButton()

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, (240, 240, 240), (180, 180, 360, 320), border_radius=12)
        pygame.draw.rect(screen, (100, 150, 200), (180, 180, 360, 40), border_radius=12)

        # Title
        title_text = self.font.render(self.message, True, (255, 255, 255))
        screen.blit(title_text, (290, 185))

        # Volume Control
        vol_label = self.small_font.render(f"Volume: {self.volume}", True, (0, 0, 0))
        screen.blit(vol_label, (240, 190 + 40))

        self.btn_close.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in [self.btn_close]:
                if btn.is_clicked(event.pos):
                    btn.on_click()

    def on_close(self):
        if hasattr(self.parent, "popups") and self in self.parent.popups:
            self.parent.popups.remove(self)
