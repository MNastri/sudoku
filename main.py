import pygame as pg
import requests

from pygame import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
    K_KP5,
    K_KP6,
    K_KP7,
    K_KP8,
    K_KP9,
)


class Cell:
    def __init__(self, pos, num, display, font):
        self.original = num != 0
        self.hovered = False
        self.selected = False
        self.pos = pos
        self.num = num
        self.display = display
        self.font = font
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.display.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(str(self.num), True, self.get_color())

    def get_color(self):
        if self.original:
            return line_color
        if self.num == 0 and self.hovered and self.selected:
            return (0, 0, 127)
        if self.num == 0 and self.hovered and not self.selected:
            return (0, 127, 0)
        if self.num == 0 and not self.hovered and self.selected:
            return (127, 0, 0)
        if self.num == 0 and not self.hovered and not self.selected:
            return (127, 127, 127)
        if self.hovered and self.selected:
            return (255, 0, 0)
        if self.hovered and not self.selected:
            return (0, 255, 0)
        if not self.hovered and self.selected:
            return (0, 0, 255)
        if not self.hovered and not self.selected:
            return number_color

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect(
            center=(
                scr_pad + self.pos[1] * cell_length + cell_length // 2,
                scr_pad + self.pos[0] * cell_length + cell_length // 2,
            )
        )

    def clear_cell(self):
        self.rend = number_font.render(str(self.num), True, bg_color)
        self.display.blit(self.rend, self.rect)

    def remove_num(self):
        self.clear_cell()
        self.num = 0

    def set_num(self, num):
        self.remove_num()
        self.num = num
        self.draw()


class Board:
    def __init__(self, board_cells, display):
        self.display = display
        self.cells = self.get_cells(board_cells=board_cells)
        self.selected_cell = None

    def draw_grid_lines(self):
        for ii in range(10):
            wdt = 4 if ii % 3 == 0 else 2
            start = end = scr_pad + ii * cell_length
            # Horizontal line
            pg.draw.line(
                self.display,
                line_color,
                (scr_pad, start),
                (scr_length - scr_pad, end),
                wdt,
            )
            # Vertical line
            pg.draw.line(
                self.display,
                line_color,
                (start, scr_pad),
                (end, scr_length - scr_pad),
                wdt,
            )

    def get_cells(self, board_cells):
        cells = []
        for line_num, line in enumerate(board_cells):
            for col_num, num in enumerate(line):
                cell = Cell((line_num, col_num), num, self.display, number_font)
                cells.append(cell)
        return cells

    def mouse_click(self, mx, my):
        if self.selected_cell:
            self.selected_cell.selected = False
        lin, col = (my - scr_pad) // cell_length, (mx - scr_pad) // cell_length
        self.selected_cell = self.cells[9 * lin + col]
        self.selected_cell.selected = True

    def set_num(self, num):
        if self.selected_cell and not self.selected_cell.original:
            self.selected_cell.set_num(num=num)

    def remove_num(self):
        if self.selected_cell and not self.selected_cell.original:
            self.selected_cell.remove_num()

    def update(self):
        for cell in self.cells:
            cell.clear_cell()
            cell.draw()


def _get_board():
    uri = "https://sugoku.herokuapp.com/board?difficulty=easy"
    response = requests.get(uri)
    return response.json()["board"]


cell_length = 60
scr_pad = 30
scr_length = scr_pad * 2 + cell_length * 9
line_color = (255, 255, 255)
number_color = (0, 0, 200)
font_size = cell_length
bg_color = (20, 20, 20)
font = "Garamond"

key_numbers = [
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
    K_KP5,
    K_KP6,
    K_KP7,
    K_KP8,
    K_KP9,
]

pg.init()
display = pg.display.set_mode((scr_length, scr_length))
display.fill(bg_color)
number_font = pg.font.SysFont(font, font_size)
pg.display.set_caption("Sudoku")
downloaded_board = _get_board()
board = Board(board_cells=downloaded_board, display=display)
board.draw_grid_lines()
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            run = False
        elif event.type == pg.MOUSEBUTTONUP:
            m_x, m_y = pg.mouse.get_pos()
            if (scr_pad < m_x < scr_length - scr_pad) and (
                scr_pad < m_y < scr_length - scr_pad
            ):
                board.mouse_click(mx=m_x, my=m_y)
        elif event.type == pg.KEYDOWN and event.key in key_numbers:
            num = key_numbers.index(event.key) % 9 + 1
            board.set_num(num=num)
        elif event.type == pg.KEYDOWN and (
            event.key == pg.K_0 or event.key == pg.K_KP0 or event.key == pg.K_DELETE
        ):
            board.remove_num()
        board.update()
    pg.display.update()
pg.quit()
