import pygame as pg
import requests


def _draw_grid_lines(display):
    for ii in range(10):
        wdt = 4 if ii % 3 == 0 else 2
        start = end = scr_pad + ii * cell_length
        # Horizontal lines
        pg.draw.line(
            display, line_color, (scr_pad, start), (scr_length - scr_pad, end), wdt
        )
        # Vertical lines
        pg.draw.line(
            display, line_color, (start, scr_pad), (end, scr_length - scr_pad), wdt
        )


def _get_board():
    uri = "https://sugoku.herokuapp.com/board?difficulty=easy"
    response = requests.get(uri)
    return response.json()["board"]


def _draw_numbers(board, font, display):
    for line_num, line in enumerate(board):
        for column_num, num in enumerate(line):
            if num == 0:
                continue
            img = font.render(str(num), True, number_color)
            img_rect = img.get_rect(
                center=(
                    scr_pad + column_num * cell_length + cell_length // 2,
                    scr_pad + line_num * cell_length + cell_length // 2,
                )
            )
            display.blit(img, img_rect)


cell_length = 60
scr_pad = 30
scr_length = scr_pad * 2 + cell_length * 9
line_color = (255, 255, 255)
number_color = (0, 0, 200)
font_size = cell_length
bg_color = (10, 10, 10)

pg.init()
display = pg.display.set_mode((scr_length, scr_length))
display.fill(bg_color)
number_font = pg.font.SysFont("Garamond", font_size)
pg.display.set_caption("Sudoku")
_draw_grid_lines(display=display)
board = _get_board()
_draw_numbers(board=board, font=number_font, display=display)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            run = False
    pg.display.update()
pg.quit()
