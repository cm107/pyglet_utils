from __future__ import annotations
from typing import List, Tuple
from pyglet.graphics import Batch
from .frame import Frame
from .grid import Grid
from .render import RenderBox
from .game_obj import GameObject, GameObjectBatch
from .resources import ResourceImage
from common_utils.base.basic import MultiParameterHandler

class PlatformBlock(GameObject):
    def __init__(self, x: int, y: int, res_img: ResourceImage, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformBlockSample'):
        super().__init__(x=x, y=y, res=res_img, frame=frame, grid=grid, renderbox=renderbox, name=name, batch=batch, usage='dynamic')

    @classmethod
    def from_grid_space_coord(
        cls, grid_space_x: int, grid_space_y: int, res_img: ResourceImage, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformBlockSample'
    ) -> PlatformBlock:
        return PlatformBlock(
            x=grid_space_x*grid.tile_width, y=grid_space_y*grid.tile_height,
            res_img=res_img, frame=frame, grid=grid, renderbox=renderbox, batch=batch, name=name
        )

class Platform(
    GameObjectBatch['Platform', 'PlatformBlock'],
    MultiParameterHandler['Platform', 'PlatformBlock']
):
    def __init__(self, frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, blocks: List[PlatformBlock]=None, name: str='PlatformSample0'):
        print(f'type(blocks): {type(blocks)}')
        super().__init__(
            frame=frame, grid=grid, renderbox=renderbox, name=name, batch=batch,
            obj_type=PlatformBlock, game_objects=blocks
        )
        self.blocks = self.obj_list

    def copy(self) -> Platform:
        return Platform(
            frame=self.frame,
            grid=self.grid,
            renderbox=self.renderbox,
            batch=self.batch,
            blocks=self.blocks.copy(),
            name=self.name
        )

    @classmethod
    def from_pos_list(
        cls, pos_list: List[Tuple[int]], res_img_list: List[ResourceImage], frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformSample0'
    ) -> Platform:
        blocks = [
            PlatformBlock(
                x=x, y=y, res_img=res_img_list[i % len(res_img_list)],
                frame=frame, grid=grid, renderbox=renderbox,
                name=f'{name}_Block{i}'
            ) for i, (x, y) in enumerate(pos_list)
        ]
        return Platform(
            frame=frame, grid=grid, renderbox=renderbox, blocks=blocks, batch=batch, name=name
        )

    @classmethod
    def from_grid_space_coords(
        cls, grid_pos_list: List[Tuple[int]], res_img_list: List[ResourceImage], frame: Frame, grid: Grid, renderbox: RenderBox, batch: Batch=None, name: str='PlatformSample0'
    ) -> Platform:
        blocks = [
            PlatformBlock.from_grid_space_coord(
                grid_space_x=grid_space_x, grid_space_y=grid_space_y, res_img=res_img_list[i % len(res_img_list)],
                frame=frame, grid=grid, renderbox=renderbox,
                name=f'{name}_Block{i}'
            ) for i, (grid_space_x, grid_space_y) in enumerate(grid_pos_list)
        ]
        return Platform(
            frame=frame, grid=grid, renderbox=renderbox, blocks=blocks, batch=batch, name=name
        )

    def get_block_names(self) -> List[str]:
        return [block.name for block in self.blocks]

    def add_block(self, x: int, y: int, res_img: ResourceImage):
        new_block = PlatformBlock(
            x=x, y=y, res_img=res_img,
            frame=self.frame, grid=self.grid, renderbox=self.renderbox,
            name=f'{self.name}_Block{len(self.blocks)}'
        )
        self.append(new_block)
    
    def remove_block(self, name: str):
        self.remove(name=name)