import json
from abc import abstractclassmethod
from typing import List, TypeVar
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.image import AbstractImage, Animation
from .resources import ResourceImage, ResourceAnimation
from .frame import Frame
from .grid import Grid
from .render import RenderBox
from ..lib.exception_handler import Error

from logger import logger
from common_utils.base.basic import MultiParameterHandler
from common_utils.check_utils import check_issubclass
from common_utils.file_utils import file_exists

class GameObject:
    def __init__(
        self, x: int, y: int, res, frame: Frame, grid: Grid, renderbox: RenderBox, name: str,
        batch: Batch=None, usage: str='dynamic',
        is_anchor_x_centered: bool=False, parent_name: str=None
    ):
        self._frame = frame
        self._grid = grid
        self._renderbox = renderbox
        self._x, self._y = x, y
        if isinstance(res, ResourceImage):
            self._sprite = Sprite(img=res.img, x=self.camera_x, y=self.camera_y, batch=batch, usage=usage)
        elif isinstance(res, ResourceAnimation):
            self._sprite = Sprite(img=res.animation, x=self.camera_x, y=self.camera_y, batch=batch, usage=usage)
        else:
            logger.error(f'res must be an instance of ResourceImage or ResourceAnimation')
            logger.error(f'type(res): {type(res)}')
            raise Exception
        self._resource_dict = res.to_dict()
        self._name = name
        self._parent_name = parent_name
        self._batch = batch
        self._is_anchor_x_centered = is_anchor_x_centered

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
    def resource_dict(self) -> dict:
        return self._resource_dict

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
            return self.x + self.width//2 + 1
    
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

    @abstractclassmethod
    def copy(self) -> H:
        raise NotImplementedError

    @property
    def x(self) -> int:
        return min([obj.x for obj in self]) if len(self) > 0 else None

    @x.setter
    def x(self, x: int):
        dx = x - self.x if len(self) > 0 else 0
        for obj in self:
            obj.x += dx

    @property
    def y(self) -> int:
        return min([obj.y for obj in self]) if len(self) > 0 else None

    @y.setter
    def y(self, y: int):
        dy = y - self.y if len(self) > 0 else 0
        for obj in self:
            obj.y += dy

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def x_left(self) -> int:
        return min([obj.x_left for obj in self]) if len(self) > 0 else None

    @x_left.setter
    def x_left(self, x_left: int):
        dx = x_left - self.x_left if len(self) > 0 else 0
        for obj in self:
            obj.x += dx

    @property
    def x_right(self) -> int:
        return max([obj.x_right for obj in self]) if len(self) > 0 else None

    @x_right.setter
    def x_right(self, x_right: int):
        dx = x_right - self.x_right if len(self) > 0 else 0
        for obj in self:
            obj.x += dx

    @property
    def y_bottom(self) -> int:
        return min([obj.y_bottom for obj in self]) if len(self) > 0 else None

    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        dy = y_bottom - self.y_bottom if len(self) > 0 else 0
        for obj in self:
            obj.y += dy

    @property
    def y_top(self) -> int:
        return max([obj.y_top for obj in self]) if len(self) > 0 else None

    @y_top.setter
    def y_top(self, y_top: int):
        dy = y_top - self.y_top if len(self) > 0 else 0
        for obj in self:
            obj.y += dy

    @property
    def width(self) -> int:
        return self.x_right - self.x_left if len(self) > 0 else 0
    
    @property
    def height(self) -> int:
        return self.y_top - self.y_bottom if len(self) > 0 else 0

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def update_sprite_position(self):
        for obj in self:
            obj.update_sprite_position()

    @property
    def camera_x(self) -> int:
        return self.x - self.frame.x if len(self) > 0 else None
    
    @property
    def camera_y(self) -> int:
        return self.y - self.frame.y if len(self) > 0 else None

    def draw(self):
        self.batch.draw()

class GameObjectHandler:
    def __init__(self, frame: Frame, grid: Grid, renderbox: RenderBox):
        # Object Based
        self.frame = frame
        self.grid = grid

        # Batch Based
        self.renderbox = renderbox

        # Resource Related
        self.save_dict = {
            'nonbatch_objects': {},
            'batch_objects': {}
        }

        self.__check_lengths()
    
    def __check_lengths(self):
        assert len(self.frame.contained_obj_list) == len(self.grid.contained_obj_list)
        assert len(self.renderbox.render_objs) <= len(self.frame.contained_obj_list)

    def __append_to_save_dict(self, obj, to_frame: bool=True, to_grid: bool=True, to_renderbox: bool=True):
        # TODO: Fix the problem where PlatformBlocks are added to nonbatch_objects.
        if issubclass(type(obj), GameObject):
            if obj.name not in self.save_dict['nonbatch_objects']:
                self.save_dict['nonbatch_objects'][obj.name] = {
                    'in_frame_objs': to_frame,
                    'in_grid_objs': to_grid,
                    'in_renderbox_objs': to_renderbox,
                    'resource_info': obj.resource_dict
                }
            else:
                self.save_dict['nonbatch_objects'][obj.name] = {
                    'in_frame_objs': to_frame or self.save_dict['nonbatch_objects'][obj.name]['in_frame_objs'],
                    'in_grid_objs': to_grid or self.save_dict['nonbatch_objects'][obj.name]['in_grid_objs'],
                    'in_renderbox_objs': to_renderbox or self.save_dict['nonbatch_objects'][obj.name]['in_renderbox_objs'],
                    'resource_info': obj.resource_dict
                }
        elif issubclass(type(obj), GameObjectBatch):
            if obj.name not in self.save_dict['batch_objects']:
                self.save_dict['batch_objects'][obj.name] = {
                    'in_frame_objs': to_frame,
                    'in_grid_objs': to_grid,
                    'in_renderbox_objs': to_renderbox,
                    'contained_objects': {
                        game_obj.name: {
                            'resource_info': game_obj.resource_dict
                        } for game_obj in obj
                    }
                }
            else:
                self.save_dict['batch_objects'][obj.name] = {
                    'in_frame_objs': to_frame or self.save_dict['batch_objects'][obj.name]['in_frame_objs'],
                    'in_grid_objs': to_grid or self.save_dict['batch_objects'][obj.name]['in_grid_objs'],
                    'in_renderbox_objs': to_renderbox or self.save_dict['batch_objects'][obj.name]['in_renderbox_objs'],
                    'contained_objects': {
                        game_obj.name: {
                            'resource_info': game_obj.resource_dict
                        } for game_obj in obj
                    }
                }
        else:
            raise Exception

    def append(self, obj, to_frame: bool=True, to_grid: bool=True, to_renderbox: bool=True):
        if issubclass(type(obj), GameObject):
            if to_frame:
                self.frame.add_obj(obj=obj)
            if to_grid:
                self.grid.add_obj(obj=obj)
            if to_renderbox:
                self.renderbox.add_render_obj(obj=obj)
        elif issubclass(type(obj), GameObjectBatch):
            for game_obj in obj:
                if to_frame:
                    self.frame.add_obj(obj=game_obj)
                if to_grid:
                    self.grid.add_obj(obj=game_obj)
            if to_renderbox:
                self.renderbox.add_render_obj(obj)
        else:
            raise Error(
                f"""
                Can't append object of type {type(obj)} to GameObjectHandler because
                {type(obj)} isn't a subclass of either GameObject or GameObjectBatch.
                """
            )
        self.__append_to_save_dict(obj=obj, to_frame=to_frame, to_grid=to_grid, to_renderbox=to_renderbox)
        self.__check_lengths()
        print(f'[obj.name for obj in self.renderbox.render_objs]:\n{[obj.name for obj in self.renderbox.render_objs]}')

    def __remove_from_save_dict(self, name: str):
        if name in self.save_dict['nonbatch_objects'].keys():
            del self.save_dict['nonbatch_objects'][name]
        elif name in self.save_dict['batch_objects'].keys():
            del self.save_dict['batch_objects'][name]
        else:
            raise Error(
                f"""
                Failed to find object by the name of '{name}' in GameObjectHandler.save_dict.
                Remove failed.
                """
            )

    def remove(self, name: str):
        self.frame.remove_obj(name)
        self.grid.remove_obj(name)
        self.renderbox.remove_render_obj(name)
        self.__remove_from_save_dict(name)
        self.__check_lengths()
    
    def dump_save_dict(self, save_path: str, overwrite: bool=False):
        if file_exists(save_path) and not overwrite:
            raise Error(f'File already exists at save_path: {save_path}')
        json.dump(self.save_dict, open(save_path, 'w'), indent=2, ensure_ascii=False)