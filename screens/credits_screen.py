import pygame
from screens.screen import Screen
from ui.button import Button

class CreditsScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.font_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_body = pygame.font.SysFont("Arial", 20)
        self.btn_back = Button(280, 560, 160, 40, "Back", self.on_back)

    def render(self):
        self.draw_background()

        title = self.font_title.render("Credits", True, (0, 0, 0))
        self.app.screen.blit(title, (self.app.screen.get_width() // 2 - title.get_width() // 2, 20))

        lines = [
            "Rush Hour",
            "",
            "Developed by:",
            "23127102 - Lê Quang Phúc ",
            "23127148 - Ân Tiến Nguyên An",
            "23127307 - Nguyễn Phạm Minh Thư",
            "23127442 - Trầm Hữu Nhân",
        ]

        y = 80
        for line in lines:
            text = self.font_body.render(line, True, (30, 30, 30))
            self.app.screen.blit(text, (40, y))
            y += 28

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

