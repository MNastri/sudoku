import pygame as pg
import requests


class Cell:
    def __init__(self, pos, num, display):
        self.original = num != 0
        self.hovered = False
        self.selected = False
        self.pos = pos
        self.num = num
        self.display = display
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.display.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = number_font.render(str(self.num), True, self.get_color())

    def get_color(self):
        if self.original:
            return line_color
        if self.num == 0:
            # return bg_color
            return (127, 127, 127)
        if self.hovered and self.selected:
            return (255, 0, 0)
        if self.hovered and not self.selected:
            return (0, 255, 0)
        if not self.hovered and self.selected:
            return (0, 0, 255)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect(
            center=(
                scr_pad + self.pos[1] * cell_length + cell_length // 2,
                scr_pad + self.pos[0] * cell_length + cell_length // 2,
            )
        )


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


def _draw_numbers(board, display):
    cells = []
    for line_num, line in enumerate(board):
        for column_num, num in enumerate(line):
            cell = Cell((line_num, column_num), num, display)
            cells.append(cell)
    return cells


cell_length = 60
scr_pad = 30
scr_length = scr_pad * 2 + cell_length * 9
line_color = (255, 255, 255)
number_color = (0, 0, 200)
font_size = cell_length
bg_color = (20, 20, 20)
font = "Garamond"

pg.init()
display = pg.display.set_mode((scr_length, scr_length))
display.fill(bg_color)
number_font = pg.font.SysFont(font, font_size)
pg.display.set_caption("Sudoku")
_draw_grid_lines(display=display)
board = _get_board()
_draw_numbers(board=board, display=display)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            run = False
    pg.display.update()
pg.quit()
