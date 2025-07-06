import pygame
import time
from abc import ABC
from screens.screen import Screen  
from screens.menu_screen import MenuScreen

class LoadingScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.start_time = time.time()
        self.duration = 3.0  # seconds to show loading screen
        self.font = pygame.font.SysFont("Arial", 36)


    def render(self):
        screen = self.app.screen
        screen.fill((30, 30, 60))  # initial background 

        # Render "Loading..." centered
        loading_text = self.font.render("Rush Hour - Loading...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(360, 360))
        self.app.screen.blit(loading_text, text_rect)

        # Calculate progress
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)  # clamp to 1.0

        # Draw loading bar background
        bar_x = 160
        bar_y = 400
        bar_width = 400
        bar_height = 30
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Draw filled portion
        fill_width = int(bar_width * progress)
        pygame.draw.rect(screen, (0, 200, 100), (bar_x, bar_y, fill_width, bar_height))

        # Optional: Draw border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def handle_input(self):
        # Auto transition after delay
        if time.time() - self.start_time > self.duration:
            self.app.switch_screen(MenuScreen(self.app))
