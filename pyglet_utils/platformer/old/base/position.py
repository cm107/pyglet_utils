from __future__ import annotations
from typing import TypeVar

from .basic import BasicObject
from common_utils.check_utils import check_type


T = TypeVar('T')

class BasePosition(BasicObject[T]):
    def __init__(self, x: int, y: int):
        super().__init__()
        check_type(x, valid_type_list=[int])
        check_type(y, valid_type_list=[int])
        self.x = x
        self.y = y
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def distance_from(self, other: T) -> float:
        check_type(other, valid_type_list=[type(self)])
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5