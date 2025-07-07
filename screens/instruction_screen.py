import pygame
from screens.screen import Screen
from screens.solver_screen import SolverScreen 
from ui.button import Button

DESERT_SAND = (210, 180, 140)

class InstructionScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.message = "Welcome to Rush Hour!\nGoal: Move the RED car to the exit.\nCars can move along their horizontal or vertical axes.\nChoose 1 of 4 algorithms for the machine to solve:\n- BFS: Breadth-First Search\n- IDS: Iterative Deepening Search\n- UCS: Uniform Cost Search\n- A*: A* search with heuristic\nIn addition, you can design your own map with Custom mode!\nClick to place the car. Select length, direction, location.\nUse the Pause / Reset / Back buttons while playing."
        self.button_back = Button(20, 600, 100, 40, "Back", self.on_back)
        self.font = pygame.font.SysFont("Arial", 22)

    def render(self):
        self.app.screen.fill(DESERT_SAND)
        lines = self.message.split("\n")
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (0, 0, 0))
            self.app.screen.blit(text, (100, 100 + i * 30))
        self.button_back.draw(self.app.screen)
        
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

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_back.is_clicked(event.pos):
                    self.on_back()

    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    
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
