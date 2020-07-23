from __future__ import annotations
from typing import List, Tuple, cast
from pyglet.image import AbstractImage
from pyglet.graphics import Batch
from .frame import Frame
from .grid import Grid
from .render import RenderBox
from .game_obj import GameObject, GameObjectBatch
from common_utils.base.basic import MultiParameterHandler

class PlatformBlock(GameObject):
    def __init__(self, x: int, y: int, img: AbstractImage, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformBlockSample'):
        super().__init__(x=x, y=y, img=img, frame=frame, grid=grid, renderbox=renderbox, name=name, batch=batch, usage='dynamic')

    @classmethod
    def from_grid_space_coord(
        cls, grid_space_x: int, grid_space_y: int, img: AbstractImage, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformBlockSample'
    ) -> PlatformBlock:
        return PlatformBlock(
            x=grid_space_x*grid.tile_width, y=grid_space_y*grid.tile_height,
            img=img, frame=frame, grid=grid, renderbox=renderbox, batch=batch, name=name
        )

class Platform(
    GameObjectBatch['Platform', 'PlatformBlock'],
    MultiParameterHandler['Platform', 'PlatformBlock']
):
    def __init__(self, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, blocks: List[PlatformBlock]=None, name: str='PlatformSample0'):
        super().__init__(
            frame=frame, grid=grid, renderbox=renderbox, name=name, batch=batch,
            obj_type=PlatformBlock, game_objects=blocks
        )
        self.blocks = self.obj_list

    @classmethod
    def from_pos_list(
        cls, pos_list: List[Tuple[int]], img_list: List[AbstractImage], frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformSample0'
    ) -> Platform:
        blocks = [
            PlatformBlock(
                x=x, y=y, img=img_list[i % len(img_list)],
                frame=frame, grid=grid, renderbox=renderbox,
                name=f'{name}_Block{i}'
            ) for i, (x, y) in enumerate(pos_list)
        ]
        return Platform(
            frame=frame, grid=grid, renderbox=renderbox, blocks=blocks, batch=batch, name=name
        )

    @classmethod
    def from_grid_space_coords(
        cls, grid_pos_list: List[Tuple[int]], img_list: List[AbstractImage], frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformSample0'
    ) -> Platform:
        blocks = [
            PlatformBlock.from_grid_space_coord(
                grid_space_x=grid_space_x, grid_space_y=grid_space_y, img=img_list[i % len(img_list)],
                frame=frame, grid=grid, renderbox=renderbox,
                name=f'{name}_Block{i}'
            ) for i, (grid_space_x, grid_space_y) in enumerate(grid_pos_list)
        ]
        return Platform(
            frame=frame, grid=grid, renderbox=renderbox, blocks=blocks, batch=batch, name=name
        )

    def get_block_names(self) -> List[str]:
        return [block.name for block in self.blocks]

    def add_block(self, x: int, y: int, img: AbstractImage):
        new_block = PlatformBlock(
            x=x, y=y, img=img,
            frame=self.frame, grid=self.grid, renderbox=self.renderbox,
            name=f'{self.name}_Block{len(self.blocks)}'
        )
        self.append(new_block)
    
    def remove_block(self, name: str):
        self.remove(name=name)