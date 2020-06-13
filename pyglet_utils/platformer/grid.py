from .shapes import LineGrid
from typing import Any, List, Tuple
from common_utils.base.basic import BasicObject, BasicHandler
from math import floor, ceil
from pyglet.text import Label
from pyglet.graphics import Batch

class GridObject(BasicObject['GridObject']):
    def __init__(
        self, obj: Any, name: str, grid_width: int, grid_height: int, tile_width: int, tile_height: int,
        is_anchor_x_centered: bool=False
    ):
        super().__init__()
        assert hasattr(obj, 'x')
        assert hasattr(obj, 'y')
        assert hasattr(obj, 'width')
        assert hasattr(obj, 'height')
        self.obj = obj
        self.name = name
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._tile_width = tile_width
        self._tile_height = tile_height
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
    def width(self) -> int:
        return int(self.obj.width)

    @property
    def height(self) -> int:
        return int(self.obj.height)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def get_bottom_left_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor((self.x + dx) / self._tile_width)
        space_y = floor((self.y + dy) / self._tile_height)
        return (space_x, space_y)

    @property
    def bottom_left_space(self) -> Tuple[int]:
        return self.get_bottom_left_space()

    def get_bottom_right_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor(((self.x + dx) + self.width - 1) / self._tile_width)
        space_y = floor((self.y + dy) / self._tile_height)
        return (space_x, space_y)

    @property
    def bottom_right_space(self) -> Tuple[int]:
        return self.get_bottom_right_space()

    def get_top_left_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor((self.x + dx) / self._tile_width)
        space_y = floor(((self.y + dy) + self.height - 1) / self._tile_height)
        return (space_x, space_y)

    @property
    def top_left_space(self) -> Tuple[int]:
        return self.get_top_left_space()

    def get_top_right_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor(((self.x + dx) + self.width - 1) / self._tile_width)
        space_y = floor(((self.y + dy) + self.height - 1) / self._tile_height)
        return (space_x, space_y)
    
    @property
    def top_right_space(self) -> Tuple[int]:
        return self.get_top_right_space()

    def get_occupied_spaces(self, dx: int=0, dy: int=0) -> List[Tuple[int]]:
        spaces = []
        bottom_left_x, bottom_left_y = self.get_bottom_left_space(dx=dx, dy=dy)
        bottom_right_x, bottom_right_y = self.get_bottom_right_space(dx=dx, dy=dy)
        top_left_x, top_left_y = self.get_top_left_space(dx=dx, dy=dy)
        top_right_x, top_right_y = self.get_top_right_space(dx=dx, dy=dy)

        xmin = min(bottom_left_x, bottom_right_x, top_left_x, top_right_x)
        xmax = max(bottom_left_x, bottom_right_x, top_left_x, top_right_x)
        ymin = min(bottom_left_y, bottom_right_y, top_left_y, top_right_y)
        ymax = max(bottom_left_y, bottom_right_y, top_left_y, top_right_y)

        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                spaces.append((x, y))
        return spaces

    @property
    def occupied_spaces(self) -> List[Tuple[int]]:
        return self.get_occupied_spaces()

class GridObjectList(BasicHandler['GridObjectList', 'GridObject']):
    def __init__(self, grid_width: int, grid_height: int, tile_width: int, tile_height: int, grid_obj_list: List[GridObject]=None):
        super().__init__(obj_type=GridObject, obj_list=grid_obj_list)
        self.grid_obj_list = self.obj_list

        self._grid_width = grid_width
        self._grid_height = grid_height
        self._tile_width = tile_width
        self._tile_height = tile_height

    def get_obj_names_in_region(self, xmin: int, ymin: int, xmax: int, ymax: int) -> List[str]:
        region_obj_names = []
        for obj in self:
            spaces = obj.occupied_spaces
            for x, y in spaces:
                if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                    region_obj_names.append(obj.name)
        return region_obj_names

    def get_obj_from_name(self, name: str) -> GridObject:
        for obj in self:
            if obj.name == name:
                return obj
        raise Exception(f"Couldn't find grid object of name {name}")

    def get_occupied_spaces(self, exclude_names: List[str]=None) -> List[Tuple[int]]:
        spaces = []
        for obj in self:
            if not exclude_names or obj.name not in exclude_names:
                spaces.extend(obj.occupied_spaces)
        return spaces

    @property
    def occupied_spaces(self) -> List[Tuple[int]]:
        return self.get_occupied_spaces()

class Grid:
    def __init__(
        self, grid_width: int, grid_height: int, tile_width: int, tile_height: int, contained_obj_list: GridObjectList=None,
        default_grid_visible: bool=False, default_coord_labels_visible: bool=False,
        coord_label_font_size: int=12, coord_label_color: Tuple[int]=(255,255,255), coord_label_opacity: int=255
    ):
        if grid_width % tile_width != 0:
            raise Exception(f'grid_width % tile_width == {grid_width % tile_width} != 0')
        if grid_height % tile_height != 0:
            raise Exception(f'grid_height % tile_height == {grid_height % tile_height} != 0')
        self._grid_width, self._grid_height = grid_width, grid_height
        self._tile_width, self._tile_height = tile_width, tile_height
        self.__line_grid = LineGrid(
            grid_width=self.grid_width, grid_height=self.grid_height,
            tile_width=self.tile_width, tile_height=self.tile_height,
            usage='static', color=(255,255,255)
        )

        self.grid_visible = default_grid_visible
        self.contained_obj_list = contained_obj_list if contained_obj_list is not None else \
            GridObjectList(
                grid_width=grid_width, grid_height=grid_height,
                tile_width=tile_width, tile_height=tile_height
            )
        self.coord_labels, self.coord_labels_batch = self._build_coord_labels(
            font_size=coord_label_font_size,
            color=coord_label_color,
            opacity=coord_label_opacity
        )
        self.coord_labels_visible = default_coord_labels_visible

    @property
    def grid_width(self) -> int:
        return self._grid_width
    
    @property
    def grid_height(self) -> int:
        return self._grid_height
    
    @property
    def tile_width(self) -> int:
        return self._tile_width
    
    @property
    def tile_height(self) -> int:
        return self._tile_height
    
    def toggle_grid_visible(self):
        self.grid_visible = not self.grid_visible

    def _build_coord_labels(self, font_size: int=12, color: Tuple[int]=(255, 255, 255), opacity: int=255) -> (List[Label], Batch):
        coord_labels = []
        coord_labels_batch = Batch()
        n_rows = self.grid_height // self.tile_height
        n_cols = self.grid_width // self.tile_width
        for grid_y in range(n_rows):
            y_center = int((grid_y + 0.5) * self.tile_height)
            for grid_x in range(n_cols):
                x_center = int((grid_x + 0.5) * self.tile_width)
                coord_label = Label(
                    text=f'({grid_x}, {grid_y})',
                    font_name='Times New Roman',
                    font_size=font_size,
                    x=x_center, y=y_center,
                    anchor_x='center', anchor_y='center',
                    color=tuple(list(color)+[opacity]),
                    batch=coord_labels_batch
                )
                coord_labels.append(coord_label)
        return coord_labels, coord_labels_batch
    
    def toggle_coord_labels_visible(self):
        self.coord_labels_visible = not self.coord_labels_visible

    def draw(self):
        if self.grid_visible:
            self.__line_grid.draw()
            if self.coord_labels_visible:
                self.coord_labels_batch.draw()
    
    def add_obj(self, obj: Any, name: str, is_anchor_x_centered: bool=False):
        obj_id = id if id is not None else len(self.contained_obj_list)
        grid_obj = GridObject(
            obj=obj, name=name,
            grid_width=self.grid_width, grid_height=self.grid_height,
            tile_width=self.tile_width, tile_height=self.tile_height,
            is_anchor_x_centered=is_anchor_x_centered
        )
        self.contained_obj_list.append(grid_obj)