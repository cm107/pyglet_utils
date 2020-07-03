from __future__ import annotations
from typing import List, Tuple, cast
from pyglet.image import AbstractImage
from pyglet.graphics import Batch
from .frame import Frame
from .game_obj import GameObject
from .grid import Grid

class PlatformBlock(GameObject):
    def __init__(self, x: int, y: int, img: AbstractImage, frame: Frame, batch: Batch=None, name: str='PlatformBlock1'):
        super().__init__(x=x, y=y, img=img, frame=frame, name=name, batch=batch, usage='dynamic')

    @classmethod
    def from_grid_space_coord(
        cls, grid_space_x: int, grid_space_y: int, grid: Grid, img: AbstractImage, frame: Frame, batch: Batch=None, name: str='PlatformBlock1'
    ) -> PlatformBlock:
        return PlatformBlock(
            x=grid_space_x*grid.tile_width, y=grid_space_y*grid.tile_height,
            img=img, frame=frame, batch=batch, name=name
        )

class Platform:
    def __init__(self, frame: Frame, blocks: List[PlatformBlock]=None, batch: Batch=None, name: str='Platform1'):
        self.batch = batch if batch is not None else Batch()
        self.blocks = blocks if blocks is not None else []
        self.frame = frame
        self.name = name

    @classmethod
    def from_pos_list(
        cls, pos_list: List[Tuple[int]], img_list: List[AbstractImage], frame: Frame, batch: Batch=None, name: str='Platform1'
    ) -> Platform:
        blocks = [
            PlatformBlock(
                x=x, y=y, img=img_list[i % len(img_list)],
                frame=frame, batch=batch,
                name=f'{name}_Block{i}'
            ) for i, (x, y) in enumerate(pos_list)
        ]
        return Platform(
            frame=frame, blocks=blocks, batch=batch, name=name
        )

    @classmethod
    def from_grid_space_coords(
        cls, grid_pos_list: List[Tuple[int]], grid: Grid, img_list: List[AbstractImage], frame: Frame, batch: Batch=None, name: str='Platform1'
    ) -> Platform:
        blocks = [
            PlatformBlock.from_grid_space_coord(
                grid_space_x=grid_space_x, grid_space_y=grid_space_y, grid=grid, img=img_list[i % len(img_list)],
                frame=frame, batch=batch,
                name=f'{name}_Block{i}'
            ) for i, (grid_space_x, grid_space_y) in enumerate(grid_pos_list)
        ]
        return Platform(
            frame=frame, blocks=blocks, batch=batch, name=name
        )

    @property
    def x(self) -> int:
        return min([block.x for block in self.blocks])

    @x.setter
    def x(self, x: int):
        dx = x - self.x
        for block in self.blocks:
            block.x += dx

    @property
    def y(self) -> int:
        return min([block.y for block in self.blocks])

    @y.setter
    def y(self, y: int):
        dy = y - self.y
        for block in self.blocks:
            block.y += dy

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def x_left(self) -> int:
        return min([block.x_left for block in self.blocks])

    @x_left.setter
    def x_left(self, x_left: int):
        dx = x_left - self.x_left
        for block in self.blocks:
            block.x += dx

    @property
    def x_right(self) -> int:
        return max([block.x_right for block in self.blocks])

    @x_right.setter
    def x_right(self, x_right: int):
        dx = x_right - self.x_right
        for block in self.blocks:
            block.x += dx

    @property
    def y_bottom(self) -> int:
        return min([block.y_bottom for block in self.blocks])

    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        dy = y_bottom - self.y_bottom
        for block in self.blocks:
            block.y += dy

    @property
    def y_top(self) -> int:
        return max([block.y_top for block in self.blocks])

    @y_top.setter
    def y_top(self, y_top: int):
        dy = y_top - self.y_top
        for block in self.blocks:
            block.y += dy

    @property
    def width(self) -> int:
        return self.x_right - self.x_left
    
    @property
    def height(self) -> int:
        return self.y_top - self.y_bottom

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def draw(self):
        self.batch.draw()