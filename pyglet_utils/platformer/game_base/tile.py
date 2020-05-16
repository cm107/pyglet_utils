from pyglet.sprite import Sprite

from .common.object import GameObject
from .common.position import Position

class Tile(GameObject['Tile']):
    def __init__(self, sprite: Sprite, position: Position):
        super().__init__(sprite=sprite, position=position)