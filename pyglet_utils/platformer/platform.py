from typing import List, Tuple, cast
from pyglet.image import AbstractImage
from pyglet.graphics import Batch
from .frame import Frame
from .game_obj import GameObject

class PlatformBlock(GameObject):
    def __init__(self, x: int, y: int, img: AbstractImage, frame: Frame, batch: Batch=None, name: str='PlatformBlock1'):
        super().__init__(x=x, y=y, img=img, frame=frame, name=name, batch=batch, usage='dynamic')

class Platform:
    def __init__(self, pos_list: List[Tuple[int]], img_list: List[AbstractImage], frame: Frame, batch: Batch=None, name: str='Platform1'):
        self.batch = batch if batch is not None else Batch()
        self.blocks = [
            PlatformBlock(
                x=x, y=y, img=img_list[i % len(img_list)],
                frame=frame, batch=self.batch,
                name=f'{name}_Block{i}'
            ) for i, (x, y) in enumerate(pos_list)
        ]
        cast(List[PlatformBlock], self.blocks)
        self.frame = frame
        self.name = name

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