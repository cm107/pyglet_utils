from __future__ import annotations

from logger import logger
from common_utils.check_utils import check_type
from .acceleration import Acceleration

class Velocity:
    def __init__(self, x: float, y: float):
        check_type(x, valid_type_list=[int, float])
        check_type(y, valid_type_list=[int, float])
        self.x = x
        self.y = y
    
    def accelerate(self, acceleration: Acceleration):
        if not isinstance(acceleration, Acceleration):
            logger.error(f'not isinstance(acceleration, Acceleration) == True')
            logger.error(f'type(acceleration): {type(acceleration)}')
            logger.error(f'acceleration: {acceleration}')
            raise Exception
        self.x += acceleration.x
        self.y += acceleration.y
    
    @classmethod
    def stationary(cls) -> Velocity:
        return Velocity(x=0.0, y=0.0)