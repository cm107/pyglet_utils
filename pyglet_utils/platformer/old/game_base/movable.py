from __future__ import annotations
from typing import List, TypeVar

from pyglet.sprite import Sprite
from pyglet.window import Window

from common_utils.check_utils import check_type

from .common.position import Position
from .common.velocity import Velocity
from .common.object import GameObject
from .grid import TileMap

T = TypeVar('T')

class MovableGameObject(GameObject[T]):
    def __init__(self, sprite: Sprite, position: Position, velocity: Velocity=Velocity.stationary()):
        super().__init__(sprite=sprite, position=position)
        check_type(velocity, Velocity)

        self.velocity = velocity

    @classmethod
    def origin(cls, sprite: Sprite, window: Window) -> MovableGameObject:
        return MovableGameObject(sprite=sprite, position=Position.origin(window=window), velocity=Velocity.stationary())

    def move(self, dx: int, dy: int, tile_map: TileMap):
        # new_x = self
        # for i in range(collision_grid.height):
        #     for j in range(collision_grid.width):
        #         tile_x, tile_y = 
        raise NotImplementedError