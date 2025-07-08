# ui/button.py
import pygame
from ui.sound import SoundManager

class Button:
    def __init__(self, x, y, width, height, label, on_click, app=None, bg_color=(100, 150, 200), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.on_click = on_click
        self.font = pygame.font.SysFont("Arial", 24)
        self.bg_color = bg_color
        self.text_color = text_color
        self.app = app 

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        text = self.font.render(self.label, True, self.text_color)
        screen.blit(text, text.get_rect(center=self.rect.center))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            self.on_click()

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.play_click_sound()
            return True
        return False

    def play_click_sound(self):
        if hasattr(self, 'app') and hasattr(self.app, 'sound'):
            self.app.sound.play_click()
