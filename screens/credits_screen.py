import pygame
from screens.screen import Screen
from ui.button import Button

class CreditsScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.font_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI", 20)
        self.btn_back = Button(280, 560, 160, 40, "Back", self.on_back, self.app)

    def render(self):
        self.draw_background()
        screen_width = self.app.screen.get_width()
        
        # Draw title
        title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
        title_text = title_font.render("Credits", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 40))
        self.app.screen.blit(title_text, title_rect)

        # White box background
        box_width, box_height = 500, 260
        box_x = (screen_width - box_width) // 2
        box_y = 90
        pygame.draw.rect(self.app.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=16)

        # Draw game name
        name_font = pygame.font.SysFont("Segoe UI", 24)
        rush_hour_text = name_font.render("Rush Hour", True, (0, 0, 0))
        self.app.screen.blit(rush_hour_text, rush_hour_text.get_rect(center=(screen_width // 2, box_y + 30)))

        # Developer label
        dev_font = pygame.font.SysFont("Segoe UI", 20)
        dev_label = dev_font.render("Developed by:", True, (0, 0, 0))
        self.app.screen.blit(dev_label, dev_label.get_rect(center=(screen_width // 2, box_y + 70)))

        # Developer names (centered inside the box)
        devs = [
            "23127102 - Lê Quang Phúc",
            "23127148 - Ân Tiến Nguyên An",
            "23127307 - Nguyễn Phạm Minh Thư",
            "23127442 - Trầm Hữu Nhân"
        ]
        y = box_y + 110
        for dev in devs:
            dev_text = dev_font.render(dev, True, (0, 0, 0))
            self.app.screen.blit(dev_text, dev_text.get_rect(center=(screen_width // 2, y)))
            y += 30
        self.btn_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_back.is_clicked(event.pos):
                    self.on_back()

    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    def draw_background(self):
        DESERT_SAND = (210, 180, 140)
        self.app.screen.fill(DESERT_SAND)

        # Cactus Positions (corners and side gaps)
        cactus_positions = [
            (611, 374),
            (672, 550),
            (2, 49),
            (2, 285), 
            (481, 587),
            (3, 472)
        ]

        for x, y in cactus_positions:
            self.draw_cactus(x, y)

        # Traffic Cones near entrance/exit and bottom
        cone_positions = [
            (135, 20),
            (15, 164),
            (422, 594),
            (688, 486),
            (642, 324),
            (695, 213),
            (78, 603)
        ]

        for x, y in cone_positions:
            self.draw_cone(x, y)

    
    def draw_cactus(self, x, y):
        # Main stem
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 8, y, 14, 50), border_radius=4)

        # Left arm
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x - 2, y + 15, 10, 20), border_radius=4)
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 2, y + 25, 10, 10), border_radius=4)

        # Right arm
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 20, y + 20, 10, 20), border_radius=4)
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 18, y + 30, 10, 10), border_radius=4)

        # Cactus base shadow
        pygame.draw.ellipse(self.app.screen, (0, 100, 0), (x + 4, y + 48, 20, 6))


    def draw_cone(self, x, y):
        # Cone base
        pygame.draw.rect(self.app.screen, (255, 140, 0), (x, y + 20, 14, 6))  # base
        pygame.draw.polygon(self.app.screen, (255, 140, 0), [(x + 7, y), (x, y + 20), (x + 14, y + 20)])  # cone
        pygame.draw.rect(self.app.screen, (255, 255, 255), (x + 3, y + 10, 8, 4))  # stripe

