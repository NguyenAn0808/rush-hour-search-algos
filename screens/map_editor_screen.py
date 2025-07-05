import pygame
from screens.screen import Screen
from ui.button import Button
from model import Car, Node
from screens.solver_screen import SolverScreen

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 30

class MapEditorScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cars = []

        self.target_car_placed = False
        self.instructions = "Chọn xe G trước. Nhấn T để xoay ngang/dọc."
        self.current_dir = 'h'
        self.current_car_type = 'G'
        self.car_index = 0

        self.button_solve = Button(500, 600, 180, 40, "SOLVE", self.on_solve)
        self.font = pygame.font.SysFont("Arial", 18)

    def render(self):
        self.app.screen.fill((255, 255, 230))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (200, 200, 200), rect, 1)
                if self.grid[row][col] != '.':
                    color = (255, 100, 100) if self.grid[row][col] == 'G' else (100, 150, 250)
                    pygame.draw.rect(self.app.screen, color, rect)
        self.button_solve.draw(self.app.screen)
        instr = self.font.render(self.instructions, True, (0, 0, 0))
        self.app.screen.blit(instr, (30, 550))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.current_dir = 'v' if self.current_dir == 'h' else 'h'

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    self.place_car(row, col)
                if self.button_solve.is_clicked((x, y)):
                    self.on_solve()

    def place_car(self, row, col):
        size = 2
        coords = []
        try:
            if self.current_dir == 'h':
                for i in range(size):
                    if self.grid[row][col + i] != '.':
                        return
                    coords.append((row, col + i))
            else:
                for i in range(size):
                    if self.grid[row + i][col] != '.':
                        return
                    coords.append((row + i, col))
        except IndexError:
            return

        for r, c in coords:
            self.grid[r][c] = self.current_car_type

        car = Car(id=self.current_car_type, dir=self.current_dir, row=row, col=col, size=size)
        self.cars.append(car)

        if not self.target_car_placed:
            self.target_car_placed = True
            self.current_car_type = chr(ord('A') + self.car_index)
            self.car_index += 1

    def on_solve(self):
        node = Node(self.cars)
        self.app.switch_screen(SolverScreen(self.app, node))