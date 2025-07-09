import time
import pygame
from screens.screen import Screen
from ui.button import Button
from solution import BFS, IDS, UCS, AStar
from popups.victory_popup import VictoryPopup
from popups.nosolution_popup import NoSolutionPopup

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 60

# Colors
DESERT_SAND = (210, 180, 140)
GRID_BORDER = (70, 130, 180)
GRID_BACKGROUND = (176, 196, 222)
EXIT_ARROW = (255, 255, 255) 

class SolverScreen(Screen): 
    def __init__(self, app, initial_node, level_number=""):
        super().__init__(app)
        self.node = initial_node
        self.level_number = level_number
        self.step = 0
        self.solution_path = []
        self.solver = None
        self.state = 'idle'  # states: idle, solving, paused, finished
        self.stats = None
        self.timer = 0
        self.step_delay = 0.7  # seconds between steps
        self.victory_popup_shown = False
        self.animation_done = False
        self.animate_goal = False
        self.goal_anim_step = 0
        self.goal_anim_timer = 0
        self.goal_anim_delay = 0.3  # seconds between frames


        self.btn_bfs = Button(40, 580, 100, 40, "BFS", lambda: self.solve(BFS), self.app)
        self.btn_ids = Button(170, 580, 100, 40, "IDS", lambda: self.solve(IDS), self.app)
        self.btn_ucs = Button(300, 580, 100, 40, "UCS", lambda: self.solve(UCS), self.app)
        self.btn_astar = Button(430, 580, 100, 40, "A*", lambda: self.solve(AStar), self.app)
        self.button_back = Button(580, 30, 100, 40, "Back", self.on_back, self.app)
        self.button_pause = Button(580, 80, 100, 40, "Pause", self.on_pause, self.app)
        self.button_reset = Button(580, 130, 100, 40, "Reset", self.on_reset, self.app)
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def render(self):
        self.draw_background()
        self.draw_blue_striped_border()

        title_text = self.font.render(f"{self.level_number}", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.app.screen.get_width() // 2, 20))
        self.app.screen.blit(title_text, title_rect)
        # Animate step-by-step solving
        if self.state == 'solving' and self.solution_path:
            if time.time() - self.timer > self.step_delay:
                self.timer = time.time()
                if self.step < len(self.solution_path) - 1:
                    self.step += 1
                elif self.step == len(self.solution_path) - 1:
                    self.state = 'goal_animating'
                    self.goal_animation_start = time.time()
                    self.goal_animation_duration = 1  # 1 second
                    self.step = len(self.solution_path) - 1

        if self.state == 'goal_animating':
            current_node = self.solution_path[-1]
            self.draw_board_with_goal_animation(current_node)

            if time.time() - self.goal_animation_start >= self.goal_animation_duration:
                 self.state = 'finished'
                 self.animation_done = True

        else:
            current_node = self.solution_path[self.step] if self.solution_path else self.node
            self.draw_board(current_node)

        # Step count and Total cost
        self.draw_step_info(current_node)


        # Draw control buttons
        for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar, self.button_back, self.button_pause, self.button_reset]:
            btn.draw(self.app.screen)

        # Draw final stats 
        if self.state == 'finished' and self.stats:
            # self.draw_stats()
            if self.state == 'finished' and self.stats:

                # Chỉ hiện popup nếu animation_done là True
                if self.animation_done and not self.victory_popup_shown:
                    popup = VictoryPopup(self.app, self)
                    self.popups.append(popup)
                    self.victory_popup_shown = True

        # Luôn vẽ các popup
        for popup in self.popups:
            if popup.visible:
                popup.draw()
    

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar, self.button_back, self.button_pause, self.button_reset]:
                    if btn.is_clicked(event.pos):
                        btn.on_click()
            for popup in self.popups:
                if popup.visible:
                    popup.handle_event(event)

    def draw_board(self, node):
        board = node.state
        
        # Car color cache
        if not hasattr(self, 'car_colors'):
            self.car_colors = {}

        color_palette = [
            (100, 150, 250),  # blue
            (255, 200, 0),    # yellow
            (0, 200, 100),    # green
            (255, 105, 180),  # pink
            (138, 43, 226),   # purple
            (255, 165, 0),    # orange
            (60, 179, 113),   # medium sea green
            (255, 255, 255),  # white
            (0, 206, 209),    # turquoise
            (186, 85, 211),   # medium orchid
        ]
        color_index = 0

        for i in range(2, 8):
            for j in range(2, 8):
                val = board[i][j]
                rect = pygame.Rect(MARGIN + (j - 2) * CELL_SIZE, MARGIN + (i - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (220, 220, 220), rect, 1)

                if val != '-':
                    if val == 'G':
                        color = (255, 100, 100)  # Red goal car
                    else:
                        if val not in self.car_colors:
                            self.car_colors[val] = color_palette[color_index % len(color_palette)]
                            color_index += 1
                        color = self.car_colors[val]

                    pygame.draw.rect(self.app.screen, color, rect)

    def draw_board_with_goal_animation(self, node):
        board = node.state
        red_car_offset = int((time.time() - self.goal_animation_start) * CELL_SIZE)  # move smoothly

        for i in range(2, 8):
            for j in range(2, 8):
                val = board[i][j]
                rect = pygame.Rect(MARGIN + (j - 2) * CELL_SIZE, MARGIN + (i - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (220, 220, 220), rect, 1)

                if val != '-':
                    if val == 'G':
                        # animate red car movement to the right
                        rect.x += red_car_offset
                        pygame.draw.rect(self.app.screen, (255, 100, 100), rect)
                    else:
                        color = self.car_colors.get(val, (100, 150, 250))
                        pygame.draw.rect(self.app.screen, color, rect)



    def draw_background(self):
        # Desert background with decorative elements
        self.app.screen.fill(DESERT_SAND)
        # Road to the right
        pygame.draw.rect(self.app.screen, (230, 230, 230), (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + 2 * CELL_SIZE, 100, CELL_SIZE))

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



    def draw_blue_striped_border(self):
        stripe_size = CELL_SIZE // 4
        grid_left = MARGIN
        grid_top = MARGIN
        grid_right = grid_left + GRID_SIZE * CELL_SIZE
        grid_bottom = grid_top + GRID_SIZE * CELL_SIZE
        exit_row = 2  # red car is always on row 2
        exit_y = grid_top + exit_row * CELL_SIZE
        stripe_colors = [(80, 180, 255), (255, 255, 255)]

        # ─ Top border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left + i, grid_top - stripe_size, stripe_size, stripe_size))

        # ─ Bottom border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left + i, grid_bottom, stripe_size, stripe_size))

        # │ Left border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left - stripe_size, grid_top + i, stripe_size, stripe_size))

        # │ Right border — skip exit row
        for row in range(GRID_SIZE):
            if row == exit_row:
                continue
            y_start = grid_top + row * CELL_SIZE
            for i in range(0, CELL_SIZE, stripe_size):
                color = stripe_colors[(i // stripe_size) % 2]
                pygame.draw.rect(self.app.screen, color, (grid_right, y_start + i, stripe_size, stripe_size))

        # ➤ Exit tunnel side walls (top and bottom only — aligned to grid)
        tunnel_length = CELL_SIZE
        for i in range(0, tunnel_length, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            # Top edge of exit tunnel
            pygame.draw.rect(self.app.screen, color, (grid_right + i, exit_y - 20, stripe_size, stripe_size))
            # Bottom edge of exit tunnel
            pygame.draw.rect(self.app.screen, color, (grid_right + i, exit_y + CELL_SIZE - stripe_size + 20, stripe_size, stripe_size))


    def draw_step_info(self, current_node):
        font = pygame.font.SysFont("Arial", 22)
        step_text = f"Step: {self.step}/{len(self.solution_path)-1 if self.solution_path else 0}"
        cost_text = f"Total Cost: {current_node.cost}"

        step_surface = font.render(step_text, True, (0, 0, 0))
        cost_surface = font.render(cost_text, True, (0, 0, 0))

        # Calculate background rectangle dimensions
        max_width = max(step_surface.get_width(), cost_surface.get_width())
        total_height = step_surface.get_height() + cost_surface.get_height() + 10  # 10px spacing
        
        # Add padding
        padding = 15
        rect_width = max_width + (padding * 2)
        rect_height = total_height + (padding * 2)
        
        # Background 
        pygame.draw.rect(self.app.screen, (240, 248, 255), 
                        (570, 420, rect_width, rect_height), border_radius=10)
        
        # Draw text on top of background
        self.app.screen.blit(step_surface, (580, 430))
        self.app.screen.blit(cost_surface, (580, 450))

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

    def solve(self, solver_class):
        self.victory_popup_shown = False
        solver = solver_class(self.node)

        start = time.time()
        goal_node = solver.solve()
        end = time.time()

        if goal_node:
            self.solution_path = list(solver.find_path(goal_node))
            self.step = 0
            self.timer = time.time()
            self.state = 'solving'


            # Collect stats from the solver instance
            self.stats = {
                "Steps": solver.step_count,
                "Time": round(end - start, 3),
                "Nodes": solver.number_expanded_nodes,
                "Memory": solver.memory_usage,
                "Cost": solver.total_cost
            }
            print("Found solution!")

        else:
            self.state = 'finished'
            self.stats = {"Message": "No solution found"}
            print("No solution.")
            
             # Hiển thị popup khi không có lời giải
            popup = NoSolutionPopup(self.app, self)
            self.popups.append(popup)

    
    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    def on_pause(self):
        if self.state == 'solving':
            self.state = 'paused'
            self.button_pause.label = "Resume"
        elif self.state == 'paused':
            self.state = 'solving'
            self.timer = time.time()
            self.button_pause.label = "Pause"

    def on_reset(self):
        self.step = 0
        self.state = 'idle'
        self.solution_path = []
        self.stats = None
        self.button_pause.label = "Pause"
        self.popups.clear()
        self.victory_popup_shown = False
        self.animation_done = False  # reset lại trạng thái animation


    def draw_stats(self):
        font = pygame.font.SysFont("Arial", 18)
        y = 370

        for key, val in self.stats.items():
            text = font.render(f"{key}: {val}", True, (0, 0, 0))
            self.app.screen.blit(text, (600, y))
            y += 25
        