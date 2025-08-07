from Settings import *
from Classes import *
import pygame as pg
import sys
import random


# == Mainloop ==
def main():
    pg.init()
    pg.display.set_caption("Tetris Layout")
    clock = pg.time.Clock()
    started = False
    rotate_pressed = False  # For rotation keys
    last_rotate_time = 0  # For timer-based rotation cooldown
    ROTATE_DELAY_MS = 100  # milliseconds
    game = Game()
    screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_PANEL_WIDTH, SCREEN_HEIGHT), pg.SCALED)
    font = pg.font.SysFont('consolas', 40)

    # == Gameloop ==
    # No slow fall needed
    while True:
        now = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not started:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    started = True
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        game.tetromino_move(-1, 0)
                    if event.key == pg.K_d:
                        game.tetromino_move(1, 0)
                    if event.key == pg.K_w and not rotate_pressed:
                        if now - last_rotate_time >= ROTATE_DELAY_MS:
                            game.current_piece.rotate()
                            last_rotate_time = now
                            rotate_pressed = True
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        rotate_pressed = False

        # No need for frame-based rotate_cooldown; timer-based now
        screen.fill(BLACK, rect=pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # No need to fill the side panel here; SidePanel.draw handles it
        if not started:
            # Draw menu
            menu_text = font.render('Press ENTER to Start', True, WHITE)
            text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(menu_text, text_rect)
        else:
            keys = pg.key.get_pressed()
            # S for continuous down
            if keys[pg.K_s]:
                game.tetromino_move(0, 1)
            game.update()
            game.draw(screen)
            # Draw the side panel after filling its background
            game.side_panel.draw(screen, game.score, game.next_piece)
        pg.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

