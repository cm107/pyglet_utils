from __future__ import annotations

from pyglet.window import Window

from logger import logger
from common_utils.check_utils import check_type, check_value

from ...base.position import BasePosition
from ...base.basic import BasicObject

class WorldPosition(BasePosition['WorldPosition']):
    def __init__(self, x: int, y: int):
        super().__init__()
        check_type(x, valid_type_list=[int])
        check_type(y, valid_type_list=[int])
        self.x = x
        self.y = y

    @classmethod
    def origin(cls) -> WorldPosition:
        return WorldPosition(x=0, y=0)

class CameraPosition(BasePosition['CameraPosition']):
    def __init__(self, x: int, y: int, window: Window):
        super().__init__()
        check_type(x, valid_type_list=[int])
        check_type(y, valid_type_list=[int])
        check_type(window, valid_type_list=[Window])
        self.x = x
        self.y = y
        self.window = window
        self._check_in_frame()

    @classmethod
    def origin(cls, window: Window) -> CameraPosition:
        return CameraPosition(x=int(window.width/2), y=int(window.height/2), window=window)

    def _check_in_frame(self):
        out_of_bounds = False
        if self.x < 0:
            logger.error(f'Out Of Bounds: Left')
            out_of_bounds = True
        elif self.x >= self.window.width:
            logger.error(f'Out Of Bounds: Right')
            out_of_bounds = True
        if self.y < 0:
            logger.error(f'Out Of Bounds: Bottom')
            out_of_bounds = True
        elif self.y >= self.window.height:
            logger.error(f'Out Of Bounds: Top')
            out_of_bounds = True

        if out_of_bounds:
            raise Exception

class Position(BasicObject['Position']):
    def __init__(self, world_pos: WorldPosition, camera_pos: CameraPosition):
        check_type(world_pos, valid_type_list=[WorldPosition])
        check_type(camera_pos, valid_type_list=[CameraPosition])
        self.world_pos = world_pos
        self.camera_pos = camera_pos
    
    @classmethod
    def origin(cls, window: Window) -> Position:
        return Position(world_pos=WorldPosition.origin(), camera_pos=CameraPosition.origin(window=window))

    def move(self, dx: int, dy: int, mode: str='both'):
        check_value(mode, valid_value_list=['world', 'camera', 'both'])
        if mode == 'world':
            self.world_pos.move(dx=dx, dy=dx)
        elif mode == 'camera':
            self.camera_pos.move(dx=dx, dy=dy)
        elif mode == 'both':
            self.world_pos.move(dx=dx, dy=dx)
            self.camera_pos.move(dx=dx, dy=dy)
        else:
            raise Exception