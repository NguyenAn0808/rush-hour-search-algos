import pygame
import os
from screens.screen import Screen

# Constants
GRID_SIZE = 8
CELL_SIZE = 64
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 60

# Load player animation frames per direction
def load_directional_frames():
    directions = ["up", "down", "left", "right"]
    frames = {}
    for direction in directions:
        frames[direction] = []
        for i in range(4):
            path = os.path.join("assets", direction, f"{i}.png")
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
            frames[direction].append(img)
    return frames

class SolverWumpus(Screen):
    def __init__(self, app=None):
        super().__init__(app)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wumpus Solver - Animated Agent")
        self.clock = pygame.time.Clock()
        self.running = True

        self.agent_frames = load_directional_frames()
        self.agent_frame_index = 0
        self.agent_anim_timer = 0
        self.agent_pos = [0, 0]  # (x, y) in grid
        self.agent_pix_pos = [0, SCREEN_HEIGHT - CELL_SIZE]  # (x, y) in pixels
        self.agent_direction = "right"  # Current facing direction
        self.move_requested = False
        self.move_delay = 8  # frames between continuous moves
        self.move_timer = 0

    def update_agent_animation(self):
        if self.move_requested:
            self.agent_anim_timer += 1
            if self.agent_anim_timer >= 10:
                self.agent_frame_index = (self.agent_frame_index + 1) % len(self.agent_frames[self.agent_direction])
                self.agent_anim_timer = 0
        else:
            self.agent_frame_index = 0  # idle frame

    def move_agent(self, dx, dy):
        new_x = self.agent_pos[0] + dx
        new_y = self.agent_pos[1] + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.agent_pos[0] = new_x
            self.agent_pos[1] = new_y
            self.agent_pix_pos[0] = self.agent_pos[0] * CELL_SIZE
            self.agent_pix_pos[1] = SCREEN_HEIGHT - ((self.agent_pos[1] + 1) * CELL_SIZE)

    def draw_grid(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (40, 40, 40), rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def render(self):
        self.draw_grid()
        self.update_agent_animation()
        frame = self.agent_frames[self.agent_direction][self.agent_frame_index]
        self.screen.blit(frame, self.agent_pix_pos)
        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.move_requested = False

        if keys[pygame.K_UP]:
            self.agent_direction = "up"
            dy = 1
        elif keys[pygame.K_DOWN]:
            self.agent_direction = "down"
            dy = -1
        elif keys[pygame.K_LEFT]:
            self.agent_direction = "left"
            dx = -1
        elif keys[pygame.K_RIGHT]:
            self.agent_direction = "right"
            dx = 1

        if dx != 0 or dy != 0:
            self.move_requested = True
            self.move_timer += 1
            if self.move_timer >= self.move_delay:
                self.move_agent(dx, dy)
                self.move_timer = 0
        else:
            self.move_timer = self.move_delay  # prevent auto-move until key is re-pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_input()
            self.render()

        pygame.quit()
