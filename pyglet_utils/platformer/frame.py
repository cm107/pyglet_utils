from pyglet.window import Window
from common_utils.base.basic import BasicObject, BasicHandler
from typing import Any, List

class FrameObject(BasicObject['FrameObject']):
    def __init__(
        self, obj: Any, name: str, is_anchor_x_centered: bool=False
    ):
        super().__init__()
        assert hasattr(obj, 'x')
        assert hasattr(obj, 'y')
        assert hasattr(obj, 'camera_x')
        assert hasattr(obj, 'camera_y')
        assert hasattr(obj, 'width')
        assert hasattr(obj, 'height')
        self.obj = obj
        self.name = name
        self._is_anchor_x_centered = is_anchor_x_centered
    
    @property
    def x(self) -> int:
        if not self._is_anchor_x_centered:
            return int(self.obj.x)
        else:
            return int(self.obj.x - 0.5*self.obj.width)

    @x.setter
    def x(self, x: int):
        self.obj.x = x
    
    @property
    def y(self) -> int:
        return int(self.obj.y)
    
    @y.setter
    def y(self, y: int):
        self.obj.y = y
    
    @property
    def camera_x(self) -> int:
        return self.obj.camera_x

    @camera_x.setter
    def camera_x(self, camera_x: int):
        self.obj.camera_x = camera_x

    @property
    def camera_y(self) -> int:
        return self.obj.camera_y

    @camera_y.setter
    def camera_y(self, camera_y: int):
        self.obj.camera_y = camera_y

    @property
    def width(self) -> int:
        return int(self.obj.width)

    @property
    def height(self) -> int:
        return int(self.obj.height)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)
    
    def is_in_frame(self, frame_x: int, frame_y: int, window: Window) -> bool:
        rel_x = self.x - frame_x
        rel_y = self.y - frame_y
        x_in_frame = rel_x >= 0 and rel_x < window.width
        y_in_frame = rel_y >= 0 and rel_y < window.height
        return x_in_frame and y_in_frame
    
    def move(self, dx: int=0, dy: int=0):
        self.x += dx
        self.y += dy

    def move_camera(self, dx: int=0, dy: int=0):
        self.camera_x += dx
        self.camera_y += dy
    
class FrameObjectList(BasicHandler['FrameObjectList', 'FrameObject']):
    def __init__(self, frame_obj_list: List[FrameObject]=None):
        super().__init__(obj_type=FrameObject, obj_list=frame_obj_list)
        self.frame_obj_list = self.obj_list
    
    def get_all_obj_in_frame(self, frame_x: int, frame_y: int, window: Window) -> List[FrameObject]:
        return [obj for obj in self if obj.is_in_frame(frame_x=frame_x, frame_y=frame_y, window=window)]
    
class Frame:
    def __init__(self, window: Window, x: int=0, y: int=0, contained_obj_list: FrameObjectList=None):
        self.window = window
        self._x = x
        self._y = y
        self.contained_obj_list = contained_obj_list if contained_obj_list is not None else FrameObjectList()
    
    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
        self._x = x
    
    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, y: int):
        self._y = y
    
    @property
    def width(self) -> int:
        return self.window.width
    
    @property
    def height(self) -> int:
        return self.window.height
    
    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
    
    def add_obj(self, obj: Any, name: str, is_anchor_x_centered: bool=False):
        self.contained_obj_list.append(
            FrameObject(
                obj=obj,
                name=name,
                is_anchor_x_centered=is_anchor_x_centered
            )
        )

    def get_all_obj(self, exclude_names: List[str]=None) -> List[FrameObject]:
        if exclude_names:
            return [obj for obj in self.contained_obj_list if obj.name not in exclude_names]
        else:
            return [obj for obj in self.contained_obj_list]

    def get_all_obj_in_frame(self) -> List[FrameObject]:
        self.contained_obj_list.get_all_obj_in_frame(frame_x=self.x, frame_y=self.y, window=self.window)
    
    def move_camera(self, dx: int=0, dy: int=0, exclude_names: List[str]=None):
        frame_objs = self.get_all_obj(exclude_names=exclude_names)
        for frame_obj in frame_objs:
            frame_obj.move_camera(dx=dx, dy=dy)