from typing import TypeVar

from pyglet.sprite import Sprite
from common_utils.check_utils import check_type

from ...base.basic import BasicObject
from .position import Position

T = TypeVar('T')

class GameObject(BasicObject[T]):
    def __init__(self, sprite: Sprite, position: Position):
        check_type(sprite, valid_type_list=[Sprite])
        check_type(position, valid_type_list=[Position])

        self.sprite = sprite
        self.width = sprite.width
        self.height = sprite.height
        self.position = position

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def draw(self):
        self.sprite.draw()

    def update_sprite(self, sprite: Sprite):
        check_type(sprite, valid_type_list=[Sprite])
        self.sprite = sprite
        self.width = sprite.width
        self.height = sprite.height