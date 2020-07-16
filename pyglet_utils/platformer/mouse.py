from typing import cast
from .grid import Grid
from .frame import Frame
from ..lib.shapes import Rectangle

class Mouse:
    def __init__(self, grid: Grid, frame: Frame):
        self.grid = grid
        self.frame = frame
        self.cursor_select_rectangle = cast(Rectangle, None)

        self._x, self._y = None, None
        self._dx, self._dy = None, None
    
    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
        self._x = x
    
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def dx(self) -> int:
        return self._dx
    
    @dx.setter
    def dx(self, dx: int):
        self._dx = dx
    
    @property
    def dy(self) -> int:
        return self._dy

    @dy.setter
    def dy(self, dy: int):
        self._dy = dy

    def enter_window(self, x: int, y: int):
        self.x, self.y = x, y
    
    def leave_window(self):
        self.x, self.y = None, None
        self.dx, self.dy = None, None
        self.cursor_select_rectangle = None
    
    def move(self, x: int, y: int, dx: int, dy: int):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy

    def update_cursor_rect(self):
        if self.x is not None and self.y is not None:
            space_x, space_y = self.grid.camera_coord_to_grid_space(camera_x=self.x, camera_y=self.y, frame=self.frame)
            rect_x = self.grid.tile_width * space_x + self.grid.grid_origin_x - self.frame.x
            rect_y = self.grid.tile_height * space_y + self.grid.grid_origin_y - self.frame.y
            if self.cursor_select_rectangle is None:
                self.cursor_select_rectangle = Rectangle(
                    x=rect_x, y=rect_y,
                    width=self.grid.tile_width, height=self.grid.tile_height,
                    color=(100,255,20), transparency=130
                )
            else:
                self.cursor_select_rectangle.move_to(x=rect_x, y=rect_y)

    def draw(self):
        if self.cursor_select_rectangle is not None:
            self.cursor_select_rectangle.draw()