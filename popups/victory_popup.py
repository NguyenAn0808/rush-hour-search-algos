import pygame
import time

class VictoryPopup:
    def __init__(self, app, solver_screen, parent_screen=None):
        self.app = app
        self.solver_screen = solver_screen
        self.parent_screen = parent_screen  
        self.visible = True
        self.width = 400
        self.height = 300
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(app.screen.get_width() // 2, app.screen.get_height() // 2))

        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 20)
        self.close_font = pygame.font.SysFont("Arial", 24)

        # Close button (X)
        self.close_button_rect = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)

        # Animation
        self.start_time = time.time()
        self.animation_duration = 1.0  # fade-in 1 second

    def draw(self):
        if not self.visible:
            return

        # Fade-in alpha
        elapsed = time.time() - self.start_time
        alpha = min(255, int((elapsed / self.animation_duration) * 255))
        self.surface.fill((255, 255, 255, alpha))  # white bg with transparency

        # Title
        title = self.title_font.render("Victory!", True, (0, 128, 0))
        self.surface.blit(title, title.get_rect(center=(self.width // 2, 40)))

        # Stats
        stats = self.solver_screen.stats or {}
        lines = [
            f"Steps: {stats.get('Steps', 'N/A')}",
            f"Nodes Expanded: {stats.get('Nodes', 'N/A')}",
            f"Memory Used: {stats.get('Memory', 'N/A')} KB",
            f"Time: {stats.get('Time', 'N/A')}s",
            f"Cost: {stats.get('Cost', 'N/A')}",
        ]

        for i, line in enumerate(lines):
            text = self.text_font.render(line, True, (0, 0, 0))
            self.surface.blit(text, (40, 90 + i * 30))

        # Draw (X) close button
        pygame.draw.rect(self.surface, (200, 50, 50), self.close_button_rect.move(-self.rect.left, -self.rect.top), border_radius=8)
        close_text = self.close_font.render("X", True, (255, 255, 255))
        self.surface.blit(close_text, close_text.get_rect(center=self.close_button_rect.move(-self.rect.left, -self.rect.top).center))

        # Blit to main screen
        self.app.screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                self.solver_screen.popups.remove(self)

