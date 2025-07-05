import pygame
from screens.screen import Screen
from ui.button import Button
from solution import BFS, IDS, UCS, AStar

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 30

class SolverScreen(Screen):
    def __init__(self, app, initial_node):
        super().__init__(app)
        self.node = initial_node
        self.step = 0
        self.solution_path = []
        self.solver = None

        self.btn_bfs = Button(50, 620, 100, 40, "BFS", lambda: self.solve(BFS))
        self.btn_ids = Button(160, 620, 100, 40, "IDS", lambda: self.solve(IDS))
        self.btn_ucs = Button(270, 620, 100, 40, "UCS", lambda: self.solve(UCS))
        self.btn_astar = Button(380, 620, 100, 40, "A*", lambda: self.solve(AStar))

        self.font = pygame.font.SysFont("Arial", 18)

    def render(self):
        self.app.screen.fill((250, 240, 255))
        if self.solution_path:
            self.draw_board(self.solution_path[self.step])
        else:
            self.draw_board(self.node)

        for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar]:
            btn.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar]:
                    if btn.is_clicked(event.pos):
                        btn.on_click()

    def draw_board(self, node):
        board = node.state
        for i in range(2, 8):
            for j in range(2, 8):
                val = board[i][j]
                rect = pygame.Rect(MARGIN + (j - 2) * CELL_SIZE, MARGIN + (i - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (220, 220, 220), rect, 1)
                if val != '-':
                    color = (255, 100, 100) if val == 'G' else (100, 150, 250)
                    pygame.draw.rect(self.app.screen, color, rect)

    def solve(self, solver_class):
        solver = solver_class
        result = solver.solve(self.node)
        if isinstance(result, list):
            self.solution_path = result
            self.step = 0
            print("✅ Found solution!")
        else:
            print("❌ No solution.")