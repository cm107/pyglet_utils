from __future__ import annotations
from typing import Any, List, Tuple
from ..lib.shapes import Rectangle

class PanelObject:
    def __init__(self, obj: Any, parent, scale_with_parent: bool=False):
        assert hasattr(parent, 'x')
        assert hasattr(parent, 'y')
        assert hasattr(parent, 'width')
        assert hasattr(parent, 'height')
        self.parent = parent

        assert hasattr(obj, 'x')
        assert hasattr(obj, 'y')
        assert hasattr(obj, 'width')
        assert hasattr(obj, 'height')
        assert hasattr(obj, 'draw')
        self.obj = obj
        self._orig_relative_x, self._orig_relative_y = self.relative_x, self.relative_y
        self._orig_width, self._orig_height = self.width, self.height
        self._orig_aspect_ratio = self.aspect_ratio

        self.scale_with_parent = scale_with_parent

    @classmethod
    def from_relative_obj(self, obj: Any, parent, scale_with_parent: bool=False) -> PanelObject:
        assert hasattr(parent, 'x')
        assert hasattr(parent, 'y')
        assert hasattr(obj, 'x')
        assert hasattr(obj, 'y')

        obj.x = parent.x + obj.x
        obj.y = parent.y + obj.y
        return PanelObject(obj=obj, parent=parent, scale_with_parent=scale_with_parent)

    @property
    def x(self) -> int:
        return self.obj.x
    
    @x.setter
    def x(self, x: int):
        self.obj.x = x

    @property
    def y(self) -> int:
        return self.obj.y
    
    @y.setter
    def y(self, y: int):
        self.obj.y = y

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)
    
    @position.setter
    def position(self, position: (int, int)):
        (self.x, self.y) = position

    @property
    def relative_x(self) -> int:
        return self.x - self.parent.x
    
    @relative_x.setter
    def relative_x(self, relative_x: int):
        self.x = relative_x + self.parent.x

    @property
    def relative_y(self) -> int:
        return self.y - self.parent.y
    
    @relative_y.setter
    def relative_y(self, relative_y: int):
        self.y = relative_y + self.parent.y

    @property
    def relative_position(self) -> (int, int):
        return (self.relative_x, self.relative_y)
    
    @relative_position.setter
    def relative_position(self, relative_position: (int, int)):
        (self.relative_x, self.relative_y) = relative_position

    @property
    def width(self) -> int:
        return self.obj.width
    
    @width.setter
    def width(self, width: int):
        self.obj.width = width

    @property
    def height(self) -> int:
        return self.obj.height
    
    @height.setter
    def height(self, height: int):
        self.obj.height = height

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def draw(self):
        self.obj.draw()

class Panel:
    def __init__(
        self, relative_x: int, relative_y: int, width: int, height: int, parent,
        bg_color: Tuple[int]=(255,0,0), bg_transparency: int=255, contained_objects: List[PanelObject]=None
    ):
        assert hasattr(parent, 'x')
        assert hasattr(parent, 'y')
        assert hasattr(parent, 'width')
        assert hasattr(parent, 'height')
        assert hasattr(parent, 'close')
        self.parent = parent
        
        assert relative_x >= 0 and relative_x + width <= self.parent.width
        assert relative_y >= 0 and relative_y + height <= self.parent.height
        self._x = self.parent.x + relative_x
        self._y = self.parent.y + relative_y
        self._orig_relative_x, self._orig_relative_y = relative_x, relative_y
        self._width = width
        self._height = height
        self._orig_width, self._orig_height = width, height

        self.contained_objects = contained_objects if contained_objects is not None else []
        self.bg_rect = Rectangle(
            x=self.x, y=self.y, width=self.width, height=self.height,
            color=bg_color, transparency=bg_transparency
        )
    
    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
        self._x = x
        self.bg_rect.x = x
        self.bg_rect.update_vertices()

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y
        self.bg_rect.y = y
        self.bg_rect.update_vertices()

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)
    
    @position.setter
    def position(self, position: (int, int)):
        (self._x, self._y) = position
        self.bg_rect.x, self.bg_rect.y = self._x, self._y
        self.bg_rect.update_vertices()

    @property
    def relative_x(self) -> int:
        return self.x - self.parent.x
    
    @relative_x.setter
    def relative_x(self, relative_x: int):
        self.x = relative_x + self.parent.x

    @property
    def relative_y(self) -> int:
        return self.y - self.parent.y
    
    @relative_y.setter
    def relative_y(self, relative_y: int):
        self.y = relative_y + self.parent.y

    @property
    def relative_position(self) -> (int, int):
        return (self.relative_x, self.relative_y)
    
    @relative_position.setter
    def relative_position(self, relative_position: (int, int)):
        (self.relative_x, self.relative_y) = relative_position

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, width: int):
        self._width = width
        self.bg_rect.width = width
        self.bg_rect.update_vertices()
        scalable_obj_list = [obj for obj in self.contained_objects if obj.scale_with_parent]
        width_ratio = width / self._orig_width
        for obj in scalable_obj_list:
            obj.relative_x = int(width_ratio * obj._orig_relative_x)
            obj.width = int(width_ratio * obj._orig_width)
    
    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, height: int):
        self._height = height
        self.bg_rect.height = height
        self.bg_rect.update_vertices()
        scalable_obj_list = [obj for obj in self.contained_objects if obj.scale_with_parent]
        height_ratio = height / self._orig_height
        for obj in scalable_obj_list:
            obj.relative_y = int(height_ratio * obj._orig_relative_y)
            obj.height = int(height_ratio * obj._orig_height)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)
    
    @shape.setter
    def shape(self, shape: (int, int)):
        (self.width, self.height) = shape

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def draw(self):
        self.bg_rect.draw()
        for panel_obj in self.contained_objects:
            panel_obj.draw()

    def add_obj(self, obj: Any, relative: bool=False, scale_with_parent: bool=False):
        if not relative:
            self.contained_objects.append(PanelObject(obj=obj, parent=self, scale_with_parent=scale_with_parent))
        else:
            self.contained_objects.append(PanelObject.from_relative_obj(obj=obj, parent=self, scale_with_parent=scale_with_parent))
    
    def close(self):
        self.parent.close()