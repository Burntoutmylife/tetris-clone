import pygame as pg
import sys
import random

# == Constants ==
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
CELL_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE


player_score = 0
tetri_slow = 1
tetri_fast = 2
tetri_rotate = 0

# == Colors ==
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# == Functions ==
def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pg.draw.line(surface, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pg.draw.line(surface, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

def draw_side_panel(surface, player_score):
    pg.draw.rect(surface, (30, 30, 30), (SCREEN_WIDTH, 0, 100, SCREEN_HEIGHT))
    font = pg.font.SysFont('consolas', 20)

    # "Next" label
    next_label = font.render('Next:', True, WHITE)
    surface.blit(next_label, (SCREEN_WIDTH + 10, 20))

    # "Score" label
    score_label = font.render(f'Score: {player_score}', True, WHITE)
    surface.blit(score_label, (SCREEN_WIDTH + 10, 100))

# == Mainloop ==
def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH + 100, SCREEN_HEIGHT))  # +100 for side panel
    pg.display.set_caption("Tetris Layout")
    clock = pg.time.Clock()

    started = False



    # == Gameloop ==
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if not started and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                started = True

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_w, pg.K_UP]:
                    tetri_slow = 0.5
                if event.key in [pg.K_s, pg.K_DOWN]:
                    tetri_fast = 0.5
                if event.key in [pg.K_a, pg.K_d, pg.K_LEFT, pg.K_RIGHT]:
                    tetri_rotate = 0.5

            if event.type == pg.KEYUP:
                if event.key in [pg.K_w, pg.K_UP]:
                    tetri_slow = 1
                if event.key in [pg.K_s, pg.K_DOWN]:
                    tetri_fast = 2
                if event.key in [pg.K_a, pg.K_d, pg.K_LEFT, pg.K_RIGHT]:
                    tetri_rotate = 0

        screen.fill(BLACK)
        draw_grid(screen)
        draw_side_panel(screen, player_score)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

