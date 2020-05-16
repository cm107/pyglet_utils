from __future__ import annotations
from common_utils.check_utils import check_type

class Acceleration:
    def __init__(self, x: float, y: float):
        check_type(x, valid_type_list=[int, float])
        check_type(y, valid_type_list=[int, float])
        self.x = x
        self.y = y
    
    @classmethod
    def gravity(cls, scale: float=1.0) -> Acceleration:
        return Acceleration(x=0.0, y=-9.81*scale)