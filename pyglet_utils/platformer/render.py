from typing import List, Any, Tuple
from .frame import Frame
from ..lib.shapes import Rectangle
from pyglet.graphics import Batch

class RenderObject:
    def __init__(self, obj: Any):
        assert hasattr(obj, 'x_left')
        assert hasattr(obj, 'x_right')
        assert hasattr(obj, 'y_bottom')
        assert hasattr(obj, 'y_top')
        assert hasattr(obj, 'batch')
        assert hasattr(obj, 'draw')            
        assert hasattr(obj, 'name')
        self.obj = obj

    @property
    def x_left(self) -> int:
        return self.obj.x_left
    
    @x_left.setter
    def x_left(self, x_left: int):
        self.obj.x_left = x_left

    @property
    def x_right(self) -> int:
        return self.obj.x_right
    
    @x_right.setter
    def x_right(self, x_right: int):
        self.obj.x_right = x_right

    @property
    def y_bottom(self) -> int:
        return self.obj.y_bottom
    
    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        self.obj.y_bottom = y_bottom

    @property
    def y_top(self) -> int:
        return self.obj.y_top
    
    @y_top.setter
    def y_top(self, y_top: int):
        self.obj.y_top = y_top

    @property
    def name(self) -> str:
        return self.obj.name
    
    @name.setter
    def name(self, name: str):
        self.obj.name = name

    @property
    def batch(self) -> Batch:
        return self.obj.batch
    
    @batch.setter
    def batch(self, batch: int):
        self.obj.batch = batch

    @property
    def is_batch(self) -> bool:
        return self.batch is not None

    def draw(self):
        self.obj.update_sprite_position()
        if self.is_batch:
            self.batch.draw()
        else:
            self.obj.draw()

class BoundingBox:
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    
    def contains(self, obj, fully: bool=False):
        # Assume obj is a subclass of GameObject
        if not fully:
            hor_contained_partially = obj.x_right > self.xmin and obj.x_left < self.xmax
            vert_contained_partially = obj.y_top > self.ymin and obj.y_bottom < self.ymax
            return hor_contained_partially and vert_contained_partially
        else:
            hor_contained_fully = obj.x_left >= self.xmin and obj.x_right <= self.xmax
            vert_contained_fully = obj.y_bottom >= self.ymin and obj.y_top <= self.ymax
            return hor_contained_fully and vert_contained_fully

class RenderBox:
    def __init__(
        self, frame: Frame, render_distance_proportion: float=1.2, render_objs: List[RenderObject]=None,
        debug: bool=False, debug_color: Tuple[int]=(0, 255, 0), debug_transparency: int=50
    ):
        self.frame = frame
        self._render_distance_proportion = render_distance_proportion
        self.render_objs = render_objs if render_objs is not None else []
        
        # Debug Related
        self.debug = debug
        self.debug_rect = Rectangle(
            x=self.x, y=self.y,
            width=self.width, height=self.height,
            color=debug_color, transparency=debug_transparency,
            usage='dynamic'
        )

    @property
    def render_distance_proportion(self) -> float:
        return self._render_distance_proportion

    @render_distance_proportion.setter
    def render_distance_proportion(self, render_distance_proportion: float):
        self._render_distance_proportion = render_distance_proportion

    @property
    def x_margin(self) -> int:
        return int((self.frame.width * self.render_distance_proportion - self.frame.width) / 2)

    @x_margin.setter
    def x_margin(self, x_margin: int):
        self.render_distance_proportion = (2 * x_margin + self.frame.width) / self.frame.width

    @property
    def y_margin(self) -> int:
        return int((self.frame.height * self.render_distance_proportion - self.frame.height) / 2)

    @y_margin.setter
    def y_margin(self, y_margin: int):
        self.render_distance_proportion = (2 * y_margin + self.frame.height) / self.frame.height

    @property
    def x(self) -> int:
        return self.frame.x - self.x_margin
    
    @x.setter
    def x(self, x: int):
        self.x_margin = self.frame.x - x
    
    @property
    def y(self) -> int:
        return self.frame.y - self.y_margin
    
    @y.setter
    def y(self, y: int):
        self.y_margin = self.frame.y - y
    
    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def width(self) -> int:
        return self.frame.width + 2 * self.x_margin
    
    @width.setter
    def width(self, width: int):
        self.x_margin = int((width - self.frame.width) / 2)

    @property
    def height(self) -> int:
        return self.frame.height + 2 * self.y_margin
    
    @height.setter
    def height(self, height: int):
        self.y_margin = int((height - self.frame.height) / 2)
    
    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    @property
    def x_left(self) -> int:
        return self.x
    
    @property
    def x_right(self) -> int:
        return self.x + self.width
    
    @property
    def y_bottom(self) -> int:
        return self.y
    
    @property
    def y_top(self) -> int:
        return self.y + self.height

    def add_render_obj(self, obj: Any):
        self.render_objs.append(RenderObject(obj))

    def remove_render_obj(self, name: str):
        for i in range(len(self.render_objs)):
            if self.render_objs[i].name == name:
                del self.render_objs[i]
                break

    def _get_bbox(self) -> BoundingBox:
        return BoundingBox(xmin=self.x_left, ymin=self.y_bottom, xmax=self.x_right, ymax=self.y_top)

    def get_all_renderable_objects(self, exclude_names: List[str]=None, fully_contained_only: bool=False) -> List[RenderObject]:
        result = []
        bbox = self._get_bbox()
        for obj in self.render_objs:
            if exclude_names is not None and obj.name in exclude_names:
                continue
            if bbox.contains(obj, fully=fully_contained_only):
                result.append(obj)
        return result
    
    def update_debug(self):
        self.debug_rect.x = self.x
        self.debug_rect.y = self.y
        self.debug_rect.width = self.width
        self.debug_rect.height = self.height

    def toggle_debug(self):
        self.debug = not self.debug

    def draw_all_renderable_objects(self, exclude_names: List[str]=None, fully_contained_only: bool=False):
        objs = self.get_all_renderable_objects(exclude_names=exclude_names, fully_contained_only=fully_contained_only)
        for obj in objs:
            obj.draw()
        
        if self.debug:
            self.debug_rect.draw()