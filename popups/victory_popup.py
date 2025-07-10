import pygame
import time

class VictoryPopup:
    def __init__(self, app, solver_screen, parent_screen=None):
        self.app = app
        self.solver_screen = solver_screen
        self.parent_screen = parent_screen  
        self.visible = True
        self.width = 400
        self.height = 180  
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(app.screen.get_width() // 2, app.screen.get_height() // 2))

        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.instruction_font = pygame.font.SysFont("Arial", 20, italic=True)
        self.close_font = pygame.font.SysFont("Arial", 24)

        # Nút (X) để đóng popup
        self.close_button_rect = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)

        # Hiệu ứng fade-in
        self.start_time = time.time()
        self.animation_duration = 1.0  # 1 giây

    def draw(self):
        if not self.visible:
            return

        # Tạo hiệu ứng mờ dần xuất hiện
        elapsed = time.time() - self.start_time
        alpha = min(255, int((elapsed / self.animation_duration) * 255))
        self.surface.fill((220, 240, 250, alpha))  # nền xanh nhạt

        # Dòng tiêu đề Victory
        title = self.title_font.render("Victory!", True, (0, 128, 0))
        self.surface.blit(title, title.get_rect(center=(self.width // 2, 60)))

        # Dòng hướng dẫn ở dưới
        instruction = self.instruction_font.render("Close the popup to continue!", True, (80, 80, 80))
        self.surface.blit(instruction, instruction.get_rect(center=(self.width // 2, 120)))

        # Nút (X) đóng ở góc
        pygame.draw.rect(self.surface, (200, 50, 50), self.close_button_rect.move(-self.rect.left, -self.rect.top), border_radius=8)
        close_text = self.close_font.render("X", True, (255, 255, 255))
        self.surface.blit(close_text, close_text.get_rect(center=self.close_button_rect.move(-self.rect.left, -self.rect.top).center))

        # Vẽ popup ra màn hình chính
        self.app.screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                if self in self.solver_screen.popups:
                    self.solver_screen.popups.remove(self)
