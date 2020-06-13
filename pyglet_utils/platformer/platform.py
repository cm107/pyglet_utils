from typing import List, Tuple, cast
from pyglet.image import AbstractImage
from pyglet.graphics import Batch
from .frame import Frame
from .game_obj import GameObject

class PlatformBlock(GameObject):
    def __init__(self, x: int, y: int, img: AbstractImage, frame: Frame, batch: Batch=None, name: str='PlatformBlock1'):
        super().__init__(x=x, y=y, img=img, frame=frame, name=name, batch=batch, usage='dynamic')
        self.batch = batch
        self.frame = frame
        self.name = name

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

    def draw(self):
        self.batch.draw()