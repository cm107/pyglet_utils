from typing import Any

from logger import logger
from common_utils.check_utils import check_type, check_value
from .tile import Tile
from math import floor

class Grid:
    def __init__(self, width: int, height: int):
        check_type(width, valid_type_list=[int])
        check_type(height, valid_type_list=[int])
        self.width = width
        self.height = height
        self.grid = [[None for column in range(width)] for row in range(height)]
    
    def set_value(self, x: int, y: int, value, x_scale: float=1.0, y_scale: float=1.0):
        self.grid[floor(x/x_scale)][floor(y/y_scale)] = value
    
    def get_value(self, x: int, y: int, x_scale: float=1.0, y_scale: float=1.0) -> Any:
        return self.grid[floor(x/x_scale)][floor(y/y_scale)]

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

class VisualGrid(Grid):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.tile_shape = None

    def set_value(self, x: int, y: int, tile: Tile, x_scale: float=1.0, y_scale: float=1.0):
        if self.tile_shape is None:
            self.tile_shape = tile.shape
        elif tile.shape != self.tile_shape:
            logger.error(f'tile.shape == {tile.shape} != {self.tile_shape} == self.tile_shape')
            raise Exception
        super().set_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale, value=tile)
    
    def get_value(self, x: int, y: int, x_scale: float=1.0, y_scale: float=1.0) -> Tile:
        return super().get_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale)

class CollisionGrid(Grid):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
    
    def set_value(self, x: int, y: int, collision: int, x_scale: float=1.0, y_scale: float=1.0):
        check_value(collision, valid_value_list=[0, 1])
        super().set_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale, value=collision)
    
    def get_value(self, x: int, y: int, x_scale: float=1.0, y_scale: float=1.0) -> int:
        return super().get_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale)

class TileMap:
    def __init__(self, visual_grid: VisualGrid, collision_grid: CollisionGrid):
        check_type(visual_grid, valid_type_list=[VisualGrid])
        check_type(collision_grid, valid_type_list=[CollisionGrid])
        if visual_grid.shape != collision_grid.shape:
            logger.error(f'visual_grid.shape == {visual_grid.shape} != {collision_grid.shape} == collision_grid.shape')
            raise Exception
        self.visual_grid = visual_grid
        self.collision_grid = collision_grid
    
    def set_value(self, x: int, y: int, tile: Tile=None, collision: int=None, x_scale: float=1.0, y_scale: float=1.0):
        if tile:
            self.visual_grid.set_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale, tile=tile)
        if collision:
            self.collision_grid.set_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale, collision=collision)

    def get_value(self, x: int, y: int, x_scale: float=1.0, y_scale: float=1.0) -> (Tile, int):
        return (self.visual_grid.get_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale), self.collision_grid.get_value(x=x, y=y, x_scale=x_scale, y_scale=y_scale))