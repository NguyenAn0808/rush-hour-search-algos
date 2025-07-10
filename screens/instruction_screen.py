import random
import pygame
from screens.screen import Screen
from screens.solver_screen import SolverScreen 
from ui.button import Button

DESERT_SAND = (210, 180, 140)

class InstructionScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.message = "Welcome to Rush Hour!\nGoal: Move the RED car to the exit.\nCars can move along their horizontal or vertical axes.\nChoose 1 of 4 algorithms for the machine to solve:\n- BFS: Breadth-First Search\n- IDS: Iterative Deepening Search\n- UCS: Uniform Cost Search\n- A*: A* search with heuristic\nDesign your own map with Custom mode!\nClick to place the car. Select length, direction, location.\nUse the Pause / Reset / Back buttons while playing."
        self.button_back = Button(280, 560, 160, 40, "Back", self.on_back, self.app)
        self.font = pygame.font.SysFont("Segoe UI", 20)
        self.sand_surface = pygame.Surface((720, 640), pygame.SRCALPHA)
        self.add_sand_grains()

    def render(self):
        self.draw_background()
        screen_width = self.app.screen.get_width()
        
        # Draw title
        title_font = pygame.font.SysFont("Papyrus", 40, bold=True)
        title_text = title_font.render("Instructions", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 40))
        self.app.screen.blit(title_text, title_rect)

        # White box background
        box_width, box_height = 500, 400
        box_x = (screen_width - box_width) // 2
        box_y = 90
        pygame.draw.rect(self.app.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=16)
        
       
        # Draw multiline message with manual line breaks
        lines = self.message.split('\n')
        for i, line in enumerate(lines):
            rendered_line = self.font.render(line, True, (0, 0, 0))
            self.app.screen.blit(rendered_line, (box_x + 20, box_y + 20 + i * 30))


        self.button_back.draw(self.app.screen)

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


    
    def draw_background(self):
        DESERT_SAND = (210, 180, 140)
        self.app.screen.fill(DESERT_SAND)
        self.app.screen.blit(self.sand_surface, (0, 0))
            
        # Diagonal stripe pattern across the screen
        screen_width, screen_height = 720, 640
        spacing = 100  # spacing between lines
        item_spacing = 80  # spacing between items on each line

        diagonals = range(-screen_height, screen_width, spacing)  # diagonal start x-offsets

        for d, offset in enumerate(diagonals):
            x = offset
            y = 0
            i = 0
            while x < screen_width and y < screen_height:
                if i % 2 == 0:
                    self.draw_cactus(x, y)
                else:
                    self.draw_cone(x, y)
                x += item_spacing
                y += item_spacing
                i += 1

    
    def add_sand_grains(self):
        # Create a surface once if it doesn't exist
        if not hasattr(self, 'sand_surface'):
            self.sand_surface = pygame.Surface((720, 640), pygame.SRCALPHA)

        num_grains = (720 * 640) // 100  # Adjust density here
        for _ in range(num_grains):
            x = random.randint(0, 719)
            y = random.randint(0, 639)

            # Pick a base color variation from DESERT_SAND (single color or list)
            base_color = DESERT_SAND if isinstance(DESERT_SAND, tuple) else random.choice(DESERT_SAND)
            variation = random.randint(-20, 20)
            grain_color = tuple(max(0, min(255, c + variation)) for c in base_color)

            size = random.randint(1, 2)
            pygame.draw.circle(self.sand_surface, grain_color, (x, y), size)

    
