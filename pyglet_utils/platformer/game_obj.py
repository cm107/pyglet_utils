from typing import List, TypeVar
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.image import AbstractImage, Animation
from .frame import Frame
from .grid import Grid
from .render import RenderBox
from ..lib.exception_handler import Error

from logger import logger
from common_utils.base.basic import MultiParameterHandler
from common_utils.check_utils import check_issubclass

class GameObject:
    def __init__(
        self, x: int, y: int, img: AbstractImage, frame: Frame, grid: Grid, renderbox: RenderBox, name: str,
        batch: Batch=None, usage: str='dynamic',
        is_anchor_x_centered: bool=False, parent_name: str=None
    ):
        self._frame = frame
        self._grid = grid
        self._renderbox = renderbox
        self._x, self._y = x, y
        if not isinstance(img, (AbstractImage, Animation)):
            logger.error(f'img must be an instance of AbstractImage or Animation')
            logger.error(f'type(img): {type(img)}')
            raise Exception
        self._sprite = Sprite(img=img, x=self.camera_x, y=self.camera_y, batch=batch, usage=usage)
        self._name = name
        self._parent_name = parent_name
        self._batch = batch
        self._is_anchor_x_centered = is_anchor_x_centered
        self.frame.add_obj(self)

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def grid(self) -> Grid:
        return self._grid
    
    @property
    def renderbox(self) -> RenderBox:
        return self._renderbox

    @property
    def sprite(self) -> Sprite:
        return self._sprite
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name
    
    @property
    def parent_name(self) -> str:
        return self._parent_name
    
    @parent_name.setter
    def parent_name(self, parent_name: str):
        self._parent_name = parent_name

    @property
    def batch(self) -> Batch:
        return self._batch
    
    @batch.setter
    def batch(self, batch: Batch):
        self._batch = batch
        self.sprite.batch = batch

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
        return self.x - self.frame.x
    
    @property
    def camera_y(self) -> int:
        return self.y - self.frame.y
    
    def set_x(self, x: int, fix_camera: bool=False):
        if fix_camera:
            dx = x - self._x
            self.frame.x = self.frame.x + dx
        self._x = x
        self.sprite.x = self.camera_x


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
        self._y = y
        self.sprite.y = self.camera_y

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
    
    def update_sprite_position(self):
        self.sprite.x = self.camera_x
        self.sprite.y = self.camera_y

    def draw(self):
        self.sprite.draw()

T = TypeVar('T')
H = TypeVar('H')

class GameObjectBatch(MultiParameterHandler[H, T]):
    def __init__(self, frame: Frame, grid: Grid, renderbox: RenderBox, name: str, batch: Batch, obj_type: type, game_objects: List[GameObject]=None):
        check_issubclass(obj_type, valid_parent_class_list=[GameObject])
        super().__init__(obj_type=obj_type, obj_list=game_objects)
        self.frame = frame
        self.grid = grid
        self.renderbox = renderbox
        self.name = name
        self.batch = batch
        for i, obj in enumerate(self.obj_list):
            self.update_obj_preappend(obj)
    
    def __check_new_obj(self, obj: T):
        check_issubclass(obj, valid_parent_class_list=[GameObject])
        assert hasattr(obj, 'sprite')
        assert hasattr(obj, 'batch')
        assert hasattr(obj, 'name')

    def update_obj_preappend(self: H, obj: T):
        obj.batch = self.batch
        obj.parent_name = self.name

    def append(self: H, obj: T):
        self.__check_new_obj(obj)
        self.update_obj_preappend(obj)
        super().append(obj)
    
    def remove(self, name: str):
        found = False
        for i in list(range(len(self)))[::-1]:
            if self.obj_list[i].name == name:
                found = True
                self.obj_list[i].batch = None
                del self.obj_list[i]
                break
        if not found:
            raise Error(f"Remove failed. Couldn't find object by the name of {name}")

    def soft_copy(self: H) -> H: # TODO: Remove necessity for this method.
        return super().copy()

    @property
    def x(self) -> int:
        return min([obj.x for obj in self])

    @x.setter
    def x(self, x: int):
        dx = x - self.x
        for obj in self:
            obj.x += dx

    @property
    def y(self) -> int:
        return min([obj.y for obj in self])

    @y.setter
    def y(self, y: int):
        dy = y - self.y
        for obj in self:
            obj.y += dy

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def x_left(self) -> int:
        return min([obj.x_left for obj in self])

    @x_left.setter
    def x_left(self, x_left: int):
        dx = x_left - self.x_left
        for obj in self:
            obj.x += dx

    @property
    def x_right(self) -> int:
        return max([obj.x_right for obj in self])

    @x_right.setter
    def x_right(self, x_right: int):
        dx = x_right - self.x_right
        for obj in self:
            obj.x += dx

    @property
    def y_bottom(self) -> int:
        return min([obj.y_bottom for obj in self])

    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        dy = y_bottom - self.y_bottom
        for obj in self:
            obj.y += dy

    @property
    def y_top(self) -> int:
        return max([obj.y_top for obj in self])

    @y_top.setter
    def y_top(self, y_top: int):
        dy = y_top - self.y_top
        for obj in self:
            obj.y += dy

    @property
    def width(self) -> int:
        return self.x_right - self.x_left
    
    @property
    def height(self) -> int:
        return self.y_top - self.y_bottom

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def update_sprite_position(self):
        for obj in self:
            obj.update_sprite_position()

    def draw(self):
        self.batch.draw()

class GameObjectHandler:
    def __init__(self, frame: Frame, grid: Grid, renderbox: RenderBox):
        # Object Based
        self.frame = frame
        self.grid = grid

        # Batch Based
        self.renderbox = renderbox
    
    def append(self, obj):
        if issubclass(type(obj), GameObject):
            self.frame.add_obj(obj=obj)
            self.grid.add_obj(obj=obj)
            self.renderbox.add_render_obj(obj=obj)
        elif issubclass(type(obj), GameObjectBatch):
            for game_obj in obj:
                self.frame.add_obj(obj=obj)
                self.grid.add_obj(obj=obj)
            self.renderbox.add_render_obj(obj)
        else:
            raise Error(
                f"""
                Can't append object of type {type(obj)} to GameObjectHandler because
                {type(obj)} isn't a subclass of either GameObject or GameObjectBatch.
                """
            )
