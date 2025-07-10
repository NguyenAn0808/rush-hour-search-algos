import pygame
from screens.screen import Screen
from ui.button import Button
from model import Car, Node
from screens.solver_screen import SolverScreen
from ui.sprites import CarSprite

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 30

CAR_COLORS = {
    'G': (255, 100, 100),
    'A': (100, 150, 250),
    'B': (0, 200, 100),
    'C': (255, 200, 0),
    'D': (138, 43, 226),
    'E': (255, 105, 180),
}

class MapEditorScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cars = []

        self.target_car_placed = False
        self.instructions = "Choose the location of target car in the third row."
        self.selected_color = 'G'
        self.current_dir = 'h'
        self.car_length = 2
        self.car_id_to_color = {'G': (255, 100, 100),
                                'A': (100, 150, 250),
                                'B': (0, 200, 100),
                                'C': (255, 200, 0),
                                'D': (138, 43, 226),
                                'E': (255, 105, 180),
                            }
        self.ok_button = Button(580, 500, 100, 40, "OK", self.place_car, self.app)
        self.solve_button = Button(580, 560, 100, 40, "Complete", self.on_solve, self.app)
        self.font = pygame.font.SysFont("impact", 20)

        self.color_buttons = []
        self.available_colors = ['A', 'B', 'C', 'D', 'E']
        for i, color_id in enumerate(self.available_colors):
            btn = Button(580, 50 + i * 50, 40, 40, '', lambda c=color_id: self.select_color(c), bg_color=CAR_COLORS[color_id])
            self.color_buttons.append(btn)

        self.toggle_dir_button = Button(580, 320, 100, 30, "Dir: H", self.toggle_direction, self.app)
        self.length_button = Button(580, 360, 100, 30, "Len: 2", self.toggle_length, self.app)

        self.selected_cell = None

    def select_color(self, color_id):
        self.selected_color = color_id

    def toggle_direction(self):
        self.current_dir = 'v' if self.current_dir == 'h' else 'h'
        self.toggle_dir_button.label = f"Dir: {'V' if self.current_dir == 'v' else 'H'}"

    def toggle_length(self):
        self.car_length = 3 if self.car_length == 2 else 2
        self.length_button.label = f"Len: {self.car_length}"

    def render(self):
        self.app.screen.fill((255, 255, 230))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (200, 200, 200), rect, 1)

        for car in self.cars:
            self.draw_car_sprite(self.app.screen, car)
                
        # Highlight selected cell
        if self.selected_cell:
            row, col = self.selected_cell
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.app.screen, (0, 255, 0), rect, 3)

        for btn in self.color_buttons:
            btn.draw(self.app.screen)

        self.toggle_dir_button.draw(self.app.screen)
        self.length_button.draw(self.app.screen)
        self.ok_button.draw(self.app.screen)
        self.solve_button.draw(self.app.screen)

        instr = self.font.render(self.instructions, True, (0, 0, 0))
        self.app.screen.blit(instr, (MARGIN, 560))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    self.selected_cell = (row, col)

                for btn in self.color_buttons + [self.ok_button, self.solve_button, self.toggle_dir_button, self.length_button]:
                    if btn.is_clicked(event.pos):
                        btn.on_click()

    def place_car(self):
        if not self.selected_cell:
            self.instructions = "Choose a cell to put the car!"
            return

        row, col = self.selected_cell
        size = 2 if not self.target_car_placed else self.car_length
        car_id = 'G' if not self.target_car_placed else self.selected_color
        dir = 'h' if not self.target_car_placed else self.current_dir

        #Phúc sửa phần này để check logic cho target car
        if not self.target_car_placed:
            if row != 2:
                self.instructions = "Target car must be on the third row!"
                return
            if dir != 'h':
                self.instructions = "Target car must be horizontal!"
                return
            if size != 2:
                self.instructions = "Target car must be length 2!"
                return
            
        coords = []
        try:
            if dir == 'h':
                for i in range(size):
                    if self.grid[row][col + i] != '.':
                        self.instructions = "Overlapping with another car!"
                        return
                    coords.append((row, col + i))
            else:
                for i in range(size):
                    if self.grid[row + i][col] != '.':
                        self.instructions = "Overlapping with another car!"
                        return
                    coords.append((row + i, col))
        except IndexError:
            self.instructions = "Out of bounds!"
            return

        for r, c in coords:
            self.grid[r][c] = car_id

        self.car_id_to_color[car_id] = CAR_COLORS.get(car_id, (150, 150, 150))
        self.cars.append(Car(id=car_id, dir=dir, row=row + 2, col=col + 2, size=size))

        if not self.target_car_placed:
            self.target_car_placed = True
            self.instructions = "Select a color, direction, length, then click a cell to place a new car."
        else:
            # Xóa nút màu đã chọn khỏi danh sách
            self.available_colors.remove(self.selected_color)
            self.color_buttons = [
               Button(580, 50 + i * 50, 40, 40, '', lambda c=color_id: self.select_color(c), self.app, bg_color=CAR_COLORS[color_id])
               for i, color_id in enumerate(self.available_colors)
            ]
            if self.available_colors:
                self.selected_color = self.available_colors[0]
            else:
                self.selected_color = None
                self.instructions = "There is no color to pick!"

    def on_solve(self):
        if not self.target_car_placed:
            self.instructions = "Put the target car first!"
            return
        node = Node(self.cars)
        print(self.cars)
        self.app.switch_screen(SolverScreen(self.app, node, "Custom Map", car_colors=self.car_id_to_color))

    
    def draw_car_sprite(self, screen, car):
        x_px = MARGIN + (car.col - 2) * CELL_SIZE
        y_px = MARGIN + (car.row - 2) * CELL_SIZE
        color = CAR_COLORS.get(car.id, (100, 100, 100))

        sprite_map = {
            (100, 150, 250): {2: "assets/cars/car_8.png", 3: "assets/cars/truck_7.png"},   # Blue
            (0, 200, 100):   {2: "assets/cars/car_7.png", 3: "assets/cars/truck_6.png"},   # Green
            (255, 200, 0):   {2: "assets/cars/car_5.png", 3: "assets/cars/truck_8.png"},   # Yellow
            (138, 43, 226):  {2: "assets/cars/car_4.png", 3: "assets/cars/truck_1.png"},   # Purple
            (255, 105, 180): {2: "assets/cars/car_12.png", 3: "assets/cars/truck_12.png"}, # Pink
            (255, 100, 100): {2: "assets/cars/car_0.png"}  # Red goal car (G)
        }

        sprite_paths = sprite_map.get(color)
        if sprite_paths and car.size in sprite_paths:
            path = sprite_paths[car.size]
            key = (path, car.dir)
            if not hasattr(self, 'car_sprites'):
                self.car_sprites = {}
            if key not in self.car_sprites:
                self.car_sprites[key] = CarSprite(path, car.size, car.dir, CELL_SIZE)
            self.car_sprites[key].draw_car(screen, x_px, y_px)
        else:
            # fallback rectangle
            width = CELL_SIZE * (car.size if car.dir == 'h' else 1)
            height = CELL_SIZE * (car.size if car.dir == 'v' else 1)
            pygame.draw.rect(screen, color, pygame.Rect(x_px, y_px, width, height), border_radius=10)