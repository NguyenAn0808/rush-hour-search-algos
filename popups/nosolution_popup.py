import pygame
import time

class NoSolutionPopup:
    def __init__(self, app, parent_screen=None):
        self.app = app
        self.parent_screen = parent_screen
        self.visible = True
        self.width = 400
        self.height = 200
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(app.screen.get_width() // 2, app.screen.get_height() // 2))

        self.title_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.close_font = pygame.font.SysFont("Arial", 24)

        # Close button (X)
        self.close_button_rect = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)

        # Animation
        self.start_time = time.time()
        self.animation_duration = 1.0  # seconds for fade-in

    def draw(self):
        if not self.visible:
            return

        # Fade-in effect
        elapsed = time.time() - self.start_time
        alpha = min(255, int((elapsed / self.animation_duration) * 255))
        self.surface.fill((220, 240, 250, alpha))

        # Message
        message = self.title_font.render("No solution is found!", True, (200, 0, 0))
        self.surface.blit(message, message.get_rect(center=(self.width // 2, self.height // 2)))

        # Close button (X)
        pygame.draw.rect(self.surface, (200, 50, 50), self.close_button_rect.move(-self.rect.left, -self.rect.top), border_radius=8)
        close_text = self.close_font.render("X", True, (255, 255, 255))
        self.surface.blit(close_text, close_text.get_rect(center=self.close_button_rect.move(-self.rect.left, -self.rect.top).center))

        # Blit popup to main screen
        self.app.screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                if self.parent_screen and hasattr(self.parent_screen, "popups"):
                    self.parent_screen.popups.remove(self)
