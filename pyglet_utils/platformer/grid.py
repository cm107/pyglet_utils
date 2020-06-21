from .shapes import LineGrid
from .frame import Frame
from typing import Any, List, Tuple
from common_utils.base.basic import BasicObject, BasicHandler
from math import floor, ceil
from pyglet.text import Label
from pyglet.graphics import Batch

class GridObject(BasicObject['GridObject']):
    def __init__(
        self, obj: Any, name: str, grid_width: int, grid_height: int, tile_width: int, tile_height: int,
        grid_origin_x: int=0, grid_origin_y: int=0,
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
        self._grid_origin_x, self._grid_origin_y = grid_origin_x, grid_origin_y
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
        space_x = floor((self.x - self._grid_origin_x + dx) / self._tile_width)
        space_y = floor((self.y - self._grid_origin_y + dy) / self._tile_height)
        return (space_x, space_y)

    @property
    def bottom_left_space(self) -> Tuple[int]:
        return self.get_bottom_left_space()

    def get_bottom_right_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor(((self.x - self._grid_origin_x + dx) + self.width - 1) / self._tile_width)
        space_y = floor((self.y - self._grid_origin_y + dy) / self._tile_height)
        return (space_x, space_y)

    @property
    def bottom_right_space(self) -> Tuple[int]:
        return self.get_bottom_right_space()

    def get_top_left_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor((self.x - self._grid_origin_x + dx) / self._tile_width)
        space_y = floor(((self.y - self._grid_origin_y + dy) + self.height - 1) / self._tile_height)
        return (space_x, space_y)

    @property
    def top_left_space(self) -> Tuple[int]:
        return self.get_top_left_space()

    def get_top_right_space(self, dx: int=0, dy: int=0) -> Tuple[int]:
        space_x = floor(((self.x - self._grid_origin_x + dx) + self.width - 1) / self._tile_width)
        space_y = floor(((self.y - self._grid_origin_y + dy) + self.height - 1) / self._tile_height)
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
    def __init__(
        self, grid_width: int, grid_height: int, tile_width: int, tile_height: int, grid_obj_list: List[GridObject]=None,
        grid_origin_x: int=0, grid_origin_y: int=0
    ):
        super().__init__(obj_type=GridObject, obj_list=grid_obj_list)
        self.grid_obj_list = self.obj_list

        self._grid_width = grid_width
        self._grid_height = grid_height
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._grid_origin_x, self._grid_origin_y = grid_origin_x, grid_origin_y

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
        self, grid_width: int, grid_height: int, tile_width: int, tile_height: int, frame: Frame,
        contained_obj_list: GridObjectList=None,
        grid_origin_x: int=0, grid_origin_y: int=0,
        default_grid_visible: bool=False, default_coord_labels_visible: bool=False,
        coord_label_font_size: int=12, coord_label_color: Tuple[int]=(255,255,255), coord_label_opacity: int=255
    ):
        if grid_width % tile_width != 0:
            raise Exception(f'grid_width % tile_width == {grid_width % tile_width} != 0')
        if grid_height % tile_height != 0:
            raise Exception(f'grid_height % tile_height == {grid_height % tile_height} != 0')
        self._grid_width, self._grid_height = grid_width, grid_height
        self._tile_width, self._tile_height = tile_width, tile_height
        self.frame = frame
        if grid_origin_x % tile_width != 0:
            raise Exception(f'grid_origin_x % tile_width == {grid_origin_x % tile_width} != 0')
        if grid_origin_y % tile_height != 0:
            raise Exception(f'grid_origin_y % tile_height == {grid_origin_y % tile_height} != 0')
        self._grid_origin_x, self._grid_origin_y = grid_origin_x, grid_origin_y
        self.__line_grid = LineGrid(
            grid_width=self.grid_width, grid_height=self.grid_height,
            tile_width=self.tile_width, tile_height=self.tile_height,
            grid_origin_x=self.grid_origin_x, grid_origin_y=self.grid_origin_y,
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
    
    @property
    def grid_origin_x(self) -> int:
        return self._grid_origin_x
    
    @property
    def grid_origin_y(self) -> int:
        return self._grid_origin_y
    
    @property
    def grid_origin(self) -> (int, int):
        return (self.grid_origin_x, self.grid_origin_y)

    def move(self, dx: int=0, dy: int=0):
        if dx != 0 or dy != 0:
            # Move Line Grid
            hor_vertex_list, vert_vertex_list = self.__line_grid._vertex_list_grid
            for hor_vertex in hor_vertex_list:
                # hor_vertex.vertices[0] += dx
                # hor_vertex.vertices[1] += dy
                # hor_vertex.vertices[2] += dx
                # hor_vertex.vertices[3] += dy
                hor_vertex.vertices[1] = (hor_vertex.vertices[1] + dy) % self.frame.height
                hor_vertex.vertices[3] = (hor_vertex.vertices[3] + dy) % self.frame.height
            for vert_vertex in vert_vertex_list:
                # vert_vertex.vertices[0] += dx
                # vert_vertex.vertices[1] += dy
                # vert_vertex.vertices[2] += dx
                # vert_vertex.vertices[3] += dy
                vert_vertex.vertices[0] = (vert_vertex.vertices[0] + dx) % self.frame.width
                vert_vertex.vertices[2] = (vert_vertex.vertices[2] + dx) % self.frame.width
            
            # Move Coordinate Labels
            for coord_label in self.coord_labels:
                coord_label.x += dx
                coord_label.y += dy
                needs_new_label = False
                if coord_label.x >= self.frame.width or coord_label.x < 0:
                    needs_new_label = True
                    coord_label.x = coord_label.x % self.frame.width
                if coord_label.y >= self.frame.height or coord_label.y < 0:
                    needs_new_label = True
                    coord_label.y = coord_label.y % self.frame.height
                if needs_new_label:
                    label_world_x = coord_label.x + self.frame.x
                    label_world_y = coord_label.y + self.frame.y
                    new_x_coord = int((label_world_x - self.grid_origin_x) // self.tile_width)
                    new_y_coord = int((label_world_y - self.grid_origin_y) // self.tile_height)
                    coord_label.text = f'({new_x_coord}, {new_y_coord})'

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
                    text=f'({grid_x-self.grid_origin_x//self.tile_width}, {grid_y-self.grid_origin_y//self.tile_height})',
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
    
    def get_coords_str(self, obj_name: str) -> str:
        grid_obj = self.contained_obj_list.get_obj_from_name(obj_name)
        xmin, ymin, xmax, ymax = None, None, None, None
        for x, y in grid_obj.occupied_spaces:
            xmin = x if xmin is None or x < xmin else xmin
            ymin = y if ymin is None or y < ymin else ymin
            xmax = x if xmax is None or x > xmax else xmax
            ymax = y if ymax is None or y > ymax else ymax
        coord_str = f'{obj_name}: ({xmin}:{xmax}, {ymin}:{ymax})'
        return coord_str
    
    def add_obj(self, obj: Any, name: str, is_anchor_x_centered: bool=False):
        obj_id = id if id is not None else len(self.contained_obj_list)
        grid_obj = GridObject(
            obj=obj, name=name,
            grid_width=self.grid_width, grid_height=self.grid_height,
            tile_width=self.tile_width, tile_height=self.tile_height,
            grid_origin_x=self.grid_origin_x, grid_origin_y=self.grid_origin_y,
            is_anchor_x_centered=is_anchor_x_centered
        )
        self.contained_obj_list.append(grid_obj)