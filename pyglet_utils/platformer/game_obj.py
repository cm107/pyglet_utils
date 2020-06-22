from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.image import AbstractImage, Animation
from .frame import Frame

from logger import logger

class GameObject:
    def __init__(
        self, x: int, y: int, img: AbstractImage, frame: Frame, name: str, batch: Batch=None, usage: str='dynamic',
        is_anchor_x_centered: bool=False
    ):
        self._x, self._y = x, y
        self._camera_x, self._camera_y = x - frame.x, y - frame.y
        if not isinstance(img, (AbstractImage, Animation)):
            logger.error(f'img must be an instance of AbstractImage or Animation')
            logger.error(f'type(img): {type(img)}')
            raise Exception
        self.sprite = Sprite(img=img, x=self._camera_x, y=self._camera_y, batch=batch, usage=usage)
        self.name = name
        self.batch = batch
        self.frame = frame
        self.frame.add_obj(self, name=name, is_anchor_x_centered=is_anchor_x_centered)
        self._is_anchor_x_centered = is_anchor_x_centered

    @property
    def is_anchor_x_centered(self) -> bool:
        return self._is_anchor_x_centered
    
    @is_anchor_x_centered.setter
    def is_anchor_x_centered(self, is_anchor_x_centered: bool):
        frame_obj = self.frame.get_obj(name=self.name)
        frame_obj.is_anchor_x_centered = is_anchor_x_centered
        self._is_anchor_x_centered = is_anchor_x_centered

    @property
    def camera_x(self) -> int:
        return self._camera_x
    
    @camera_x.setter
    def camera_x(self, camera_x: int):
        self._camera_x = camera_x
        self.sprite.x = self._camera_x

    @property
    def camera_y(self) -> int:
        return self._camera_y
    
    @camera_y.setter
    def camera_y(self, camera_y: int):
        self._camera_y = camera_y
        self.sprite.y = self._camera_y

    def set_x(self, x: int, fix_camera: bool=False):
        if fix_camera:
            dx = x - self._x
            self.frame.x = self.frame.x + dx
        else:
            self._camera_x = x - self.frame.x
        self._x = x

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
       self.set_x(x=x, fix_camera=False)

    def set_y(self, y: int, fix_camera: bool=False):
        if fix_camera:
            dy = y - self._y
            self.frame.y = self.frame.y + dy
        else:
            self._camera_y = y - self.frame.y
        self._y = y

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, y: int):
        self.set_y(y=y, fix_camera=False)

    @property
    def width(self) -> int:
        return self.sprite.width
    
    @property
    def height(self) -> int:
        return self.sprite.height

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    @property
    def x_left(self) -> int:
        if not self.is_anchor_x_centered:
            return self.x
        else:
            return self.x - self.width//2
    
    @x_left.setter
    def x_left(self, x_left: int):
        if not self.is_anchor_x_centered:
            self.x = x_left
        else:
            self.x = x_left - self.width//2
    
    @property
    def x_right(self) -> int:
        if not self.is_anchor_x_centered:
            return self.x + self.width
        else:
            return self.x + self.width//2
    
    @x_right.setter
    def x_right(self, x_right: int):
        if not self.is_anchor_x_centered:
            self.x = x_right - self.height
        else:
            self.x = x_right - self.width//2
    
    @property
    def y_bottom(self) -> int:
        return self.y
    
    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        self.y = y_bottom
    
    @property
    def y_top(self) -> int:
        return self.y + self.height
    
    @y_top.setter
    def y_top(self, y_top: int):
        self.y = y_top - self.height
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
    
    def draw(self):
        self.sprite.draw()