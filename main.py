import pygame as pg


def _draw_grid_lines(display):
    for ii in range(10):
        start = end = screen_pad + ii * cell_side_length
        # Horizontal lines
        pg.draw.line(
            display,
            line_color,
            (screen_pad, start),
            (screen_side_length - screen_pad, end),
        )
        # Vertical lines
        pg.draw.line(
            display,
            line_color,
            (start, screen_pad),
            (end, screen_side_length - screen_pad),
        )


cell_side_length = 60
screen_pad = 30
screen_side_length = screen_pad * 2 + cell_side_length * 9
line_color = (255, 255, 255)

pg.init()
display = pg.display.set_mode((screen_side_length, screen_side_length))
_draw_grid_lines(display=display)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            run = False
    pg.display.update()
pg.quit()
