import pygame as pg
import random
import sys
from Settings import *





class Grid:
    def __init__(self, cell_size, width, height):
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = pg.Rect(self.x + x * self.cell_size, self.y + y * self.cell_size, self.cell_size, self.cell_size)
                color = (30, 30, 30) if self.grid[y][x] == 0 else WHITE
                pg.draw.rect(surface, color, rect, 0 if self.grid[y][x] else 1)

class SidePanel:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, surface, score, next_piece):
        # Always fill the side panel area before drawing labels to prevent flicker
        pg.draw.rect(surface, (30, 30, 30), (SCREEN_WIDTH, 0, self.width, self.height))
        font = pg.font.SysFont('consolas', 20)
        next_label = font.render('Next:', True, WHITE)
        surface.blit(next_label, (SCREEN_WIDTH + 10, 20))
        score_label = font.render(f'Score: {score}', True, WHITE)
        surface.blit(score_label, (SCREEN_WIDTH + 10, 400))
        # Optionally draw next_piece preview here




class Tetromino:
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]],  # Z
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 0, 1], [1, 1, 1]],  # L
    ]
    COLORS = [
        (0, 255, 255),  # Cyan (I)
        (255, 255, 0),  # Yellow (O)
        (128, 0, 128),  # Purple (T)
        (0, 255, 0),    # Green (S)
        (255, 0, 0),    # Red (Z)
        (0, 0, 255),    # Blue (J)
        (255, 165, 0),  # Orange (L)
    ]

    def __init__(self, cell_size):
        self.type = random.randint(0, len(self.SHAPES) - 1)
        self.base_shape = self.SHAPES[self.type]
        self.rotations = self.generate_rotations(self.base_shape)
        self.rotation_index = 0
        self.shape = self.rotations[self.rotation_index]
        self.color = self.COLORS[self.type]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.cell_size = cell_size

    def generate_rotations(self, shape):
        # Generate all 4 possible rotations for a tetromino
        rotations = [shape]
        for _ in range(3):
            shape = [list(row) for row in zip(*shape[::-1])]
            if not any(self.shapes_equal(shape, r) for r in rotations):
                rotations.append(shape)
        return rotations

    def shapes_equal(self, s1, s2):
        return len(s1) == len(s2) and all(row1 == row2 for row1, row2 in zip(s1, s2))

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.shape = self.rotations[self.rotation_index]

    def draw(self, surface):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pg.Rect((self.x + x) * self.cell_size, (self.y + y) * self.cell_size, self.cell_size, self.cell_size)
                    pg.draw.rect(surface, self.color, rect)
                    pg.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.grid = Grid(CELL_SIZE, GRID_WIDTH, GRID_HEIGHT)
        self.side_panel = SidePanel(SIDE_PANEL_WIDTH, SCREEN_HEIGHT)
        self.score = 0
        self.current_piece = Tetromino(CELL_SIZE)
        self.next_piece = Tetromino(CELL_SIZE)
        self.gravity_counter = 0
        self.base_gravity_speed = 8  # Lower is faster (frames per drop)
        self.slow_gravity_speed = 20  # Higher is slower (frames per drop)

    def draw(self, surface):
        self.grid.draw(surface)
        self.current_piece.draw(surface)
        # Do not draw the side panel here; let the main loop handle it after filling the side panel area

    def tetromino_move(self, dx, dy):
        # Calculate new position
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        shape = self.current_piece.shape
        shape_width = len(shape[0])
        shape_height = len(shape)
        # Check horizontal boundaries
        if new_x < 0 or new_x + shape_width > GRID_WIDTH:
            return
        # Check vertical boundaries (for manual down movement)
        if new_y < 0 or new_y + shape_height > GRID_HEIGHT:
            return
        self.current_piece.x = new_x
        self.current_piece.y = new_y
        
    def collision(self):
        # Check for collisions with the grid and boundaries
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_piece.x + x
                    grid_y = self.current_piece.y + y
                    if (grid_x < 0 or grid_x >= GRID_WIDTH or
                        grid_y < 0 or grid_y >= GRID_HEIGHT or
                        self.grid.grid[grid_y][grid_x]):
                        return True
        return False
    
    def lock_piece(self):
        # Lock the current piece into the grid
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_piece.x + x
                    grid_y = self.current_piece.y + y
                    self.grid.grid[grid_y][grid_x] = 1
        self.score += 10

    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(CELL_SIZE)
        if self.collision():
            # Game over condition
            print("Game Over")
            pg.quit()
            sys.exit()

    def update(self, slow_fall=False):
        self.gravity_counter += 1
        gravity_speed = self.slow_gravity_speed if slow_fall else self.base_gravity_speed
        if self.gravity_counter >= gravity_speed:
            self.current_piece.y += 1
            if self.collision():
                self.current_piece.y -= 1
                self.lock_piece()
                self.spawn_new_piece()
            self.gravity_counter = 0
        # Here you would implement collision, locking, line clear, etc.

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.tetromino_move(-1, 0)
            if self.collision():
                self.tetromino_move(1, 0)
        if keys[pg.K_RIGHT]:
            self.tetromino_move(1, 0)
            if self.collision():
                self.tetromino_move(-1, 0)
        if keys[pg.K_DOWN]:
            self.tetromino_move(0, 1)
            if self.collision():
                self.tetromino_move(0, -1)
        if keys[pg.K_UP]:
            # Rotate the piece
            original_shape = self.current_piece.shape
            self.current_piece.shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
            if self.collision():
                self.current_piece.shape = original_shape
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        # Draw the updated game state
        screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_PANEL_WIDTH, SCREEN_HEIGHT))
        screen.fill(BLACK)
        self.draw(screen)
        pg.display.flip()
def main():
    pg.init()
    pg.display.set_caption("Tetris Layout")
    clock = pg.time.Clock()
    started = False
    game = Game()

    # == Gameloop ==
    while True:
        screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_PANEL_WIDTH, SCREEN_HEIGHT))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not started and event.type == pg.KEYDOWN and event.key == pg.K_w:
                started = True
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_w, pg.K_UP]:
                    game.gravity_speed = 15  # Speed up gravity
                if event.key in [pg.K_s, pg.K_DOWN]:
                    game.gravity_speed = 60  # Slow down gravity
                if event.key in [pg.K_a, pg.K_d, pg.K_LEFT, pg.K_RIGHT]:
                    game.gravity_speed = 30  # Reset to normal speed
            if event.type == pg.KEYUP:
                if event.key in [pg.K_w, pg.K_UP]:
                    game.gravity_speed = 30
                if event.key in [pg.K_s, pg.K_DOWN]:
                    game.gravity_speed = 30
                if event.key in [pg.K_a, pg.K_d, pg.K_LEFT, pg.K_RIGHT]:
                    game.gravity_speed = 30

        screen.fill(BLACK)
        game.update()
        game.draw(screen)
        pg.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()