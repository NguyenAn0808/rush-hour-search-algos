# ui/button.py
import pygame

class Button:
    def __init__(self, x, y, width, height, label, on_click, bg_color=(100, 150, 200), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.on_click = on_click
        self.font = pygame.font.SysFont("Arial", 24)
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        text = self.font.render(self.label, True, self.text_color)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            self.on_click()

