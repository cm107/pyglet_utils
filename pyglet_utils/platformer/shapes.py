from __future__ import annotations
from typing import List, Tuple, Dict, Any
from pyglet.graphics import draw, draw_indexed, vertex_list, vertex_list_indexed
import pyglet.gl as gl
from pyglet.graphics.vertexdomain import VertexList, IndexedVertexList
from pyglet.graphics import Batch

from logger import logger
from common_utils.common_types.point import Point2D, Point2D_List
from common_utils.base.basic import BasicObject, BasicHandler
from common_utils.check_utils import check_list_length, check_value_from_list, \
    check_type, check_type_from_list, check_value

from typing import TypeVar
from abc import abstractmethod, ABCMeta

T = TypeVar('T')
H = TypeVar('H')

def find_duplicates(val_list: list) -> Dict[Any, int]:
    duplicate_dict = {}
    for val in val_list:
        if val not in duplicate_dict and val_list.count(val) > 1:
            duplicate_dict[val] = val_list.count(val)
    return duplicate_dict

class GL_Color(BasicObject):
    def __init__(self, r: int, b: int, g: int):
        super().__init__()
        check_type(r, valid_type_list=[int])
        check_type(g, valid_type_list=[int])
        check_type(b, valid_type_list=[int])
        self.r = r
        self.b = b
        self.g = g

    def to_list(self) -> List[int]:
        return [self.r, self.b, self.g]

    @classmethod
    def from_list(self, vals: List[int]) -> GL_Color:
        check_list_length(vals, correct_length=3)
        r, b, g = vals
        return GL_Color(r=r, b=b, g=g)
    
    def to_tuple(self) -> Tuple[int]:
        return (self.r, self.b, self.g)

    @classmethod
    def from_tuple(self, vals: Tuple[int]) -> GL_Color:
        check_list_length(vals, correct_length=3)
        r, b, g = vals
        return GL_Color(r=r, b=b, g=g)

class GL_Point2D(BasicObject['GL_Point2D']):
    def __init__(self, x: float, y: float, color: GL_Color=GL_Color(255,0,0)):
        super().__init__()
        check_type(x, valid_type_list=[float, int])
        check_type(y, valid_type_list=[float, int])
        check_type(color, valid_type_list=[GL_Color])
        self.__x = x
        self.__y = y
        self.__color = color

    @property
    def vertex_list(self) -> VertexList:
        return vertex_list(
            1,
            ('v2f', (self.x, self.y)),
            ('c3B', self.color.to_tuple())
        )
    
    def draw(self):
        self.vertex_list.draw(gl.GL_POINTS)

    @property
    def x(self) -> float:
        return self.__x
    
    @x.setter
    def x(self, x: float):
        check_type(x, valid_type_list=[float, int])
        self.__x = x
    
    @property
    def y(self) -> float:
        return self.__y
    
    @y.setter
    def y(self, y: float):
        check_type(y, valid_type_list=[float, int])
        self.__y = y
    
    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    @property
    def color(self) -> GL_Color:
        return self.__color
    
    @color.setter
    def color(self, color: GL_Color):
        if isinstance(color, GL_Color):
            self.__color = color
        elif isinstance(color, list):
            self.__color = GL_Color.from_list(color)
        elif isinstance(color, tuple):
            self.__color = GL_Color.from_tuple(color)
        else:
            raise Exception

class GL_Points2D_Base(BasicHandler[H, 'GL_Point2D']):
    def __init__(self, point_list: List[GL_Point2D]=None):
        super().__init__(obj_type=GL_Point2D, obj_list=point_list)
        self.point_list = point_list

    def move(self, dx: float=0.0, dy: float=0.0):
        for point in self:
            point.move(dx=dx, dy=dy)

    @property
    def color_list(self) -> List[GL_Color]:
        return [point.color for point in self]

    @color_list.setter
    def color_list(self, color: List[GL_Color]):
        if type(color) is list:
            check_list_length(color, correct_length=len(self))
            check_type_from_list(color, valid_type_list=[GL_Color])
            for point, val in zip(self, color):
                point.color = val
        elif type(color) is GL_Color:
            for point in self:
                point.color = color
        else:
            raise Exception

    @property
    def vertex_list(self) -> VertexList:
        flat_coords = []
        flat_colors = []
        for point in self:
            flat_coords.extend([point.x, point.y])
            flat_colors.extend(point.color.to_list())
        return vertex_list(
            len(self),
            ('v2f', tuple(flat_coords)),
            ('c3B', tuple(flat_colors))
        )

    def get_indexed_vertex_list(self, idx_order: List[int]) -> IndexedVertexList:
        flat_coords = []
        flat_colors = []
        for point in self:
            flat_coords.extend([point.x, point.y])
            flat_colors.extend(point.color.to_list())
        return vertex_list_indexed(
            len(self),
            tuple(idx_order),
            ('v2f', tuple(flat_coords)),
            ('c3B', tuple(flat_colors))
        )

    def draw(self, idx_order: List[int]=None, mode: int=gl.GL_POINTS):
        if idx_order is None:
            self.vertex_list.draw(mode)
        else:
            self.get_indexed_vertex_list(idx_order=idx_order).draw(mode)

class GL_Points2D(
    GL_Points2D_Base['GL_Points2D'],
    BasicHandler['GL_Points2D', 'GL_Point2D']
):
    def __init__(self, point_list: List[GL_Point2D]=None):
        super().__init__(point_list=point_list)

    @classmethod
    def from_list(self, coord_list: List[list], color_list: List[list]=None) -> GL_Points2D:
        color_list0 = color_list if color_list is not None else [GL_Color(255,0,0).to_list()]*len(coord_list)
        return GL_Points2D([GL_Point2D(x=coord[0], y=coord[1], color=GL_Color.from_list(color)) for coord, color in zip(coord_list, color_list0)])

    def points_only_method(self):
        pass

    def draw(self, idx_order: List[int]=None):
        super().draw(idx_order=idx_order, mode=gl.GL_POINTS)

class GL_Triangles2D(
    GL_Points2D_Base['GL_Triangles2D'],
    BasicHandler['GL_Triangles2D', 'GL_Point2D']
):
    def __init__(self, point_list: List[GL_Point2D]=None):
        super().__init__(point_list=point_list)

    @classmethod
    def from_list(self, coord_list: List[list], color_list: List[list]=None) -> GL_Triangles2D:
        color_list0 = color_list if color_list is not None else [GL_Color(255,0,0).to_list()]*len(coord_list)
        return GL_Triangles2D([GL_Point2D(x=coord[0], y=coord[1], color=GL_Color.from_list(color)) for coord, color in zip(coord_list, color_list0)])

    def triangles_only_method(self):
        pass

    def draw(self, idx_order: List[int]):
        super().draw(idx_order=idx_order, mode=gl.GL_TRIANGLES)

class GL_TriangleStrip2D(
    GL_Points2D_Base['GL_TriangleStrip2D'],
    BasicHandler['GL_TriangleStrip2D', 'GL_Point2D']
):
    def __init__(self, point_list: List[GL_Point2D]=None):
        super().__init__(point_list=point_list)

    @classmethod
    def from_list(self, coord_list: List[list], color_list: List[list]=None) -> GL_TriangleStrip2D:
        color_list0 = color_list if color_list is not None else [GL_Color(255,0,0).to_list()]*len(coord_list)
        return GL_Triangles2D([GL_Point2D(x=coord[0], y=coord[1], color=GL_Color.from_list(color)) for coord, color in zip(coord_list, color_list0)])

    def triangles_only_method(self):
        pass

    def draw(self, idx_order: List[int]):
        super().draw(idx_order=idx_order, mode=gl.GL_TRIANGLES_STRIP)

class GL_Quads2D(
    GL_Points2D_Base['GL_Quads2D'],
    BasicHandler['GL_Quads2D', 'GL_Point2D']
):
    def __init__(self, point_list: List[GL_Point2D]=None):
        super().__init__(point_list=point_list)

    @classmethod
    def from_list(self, coord_list: List[list], color_list: List[list]=None) -> GL_Quads2D:
        color_list0 = color_list if color_list is not None else [GL_Color(255,0,0).to_list()]*len(coord_list)
        return GL_Triangles2D([GL_Point2D(x=coord[0], y=coord[1], color=GL_Color.from_list(color)) for coord, color in zip(coord_list, color_list0)])

    def quads_only_method(self):
        pass

    def draw(self, idx_order: List[int]):
        super().draw(idx_order=idx_order, mode=gl.GL_QUADS)

class Rectangle:
    def __init__(
        self, x: int, y: int, width: int, height: int, color: Tuple[int]=(255,0,0),
        transparency: int=255, usage: str='dynamic'
    ):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.transparency = transparency
        check_value(usage, valid_value_list=['static', 'dynamic', 'stream'])
        self.usage = usage
        self.vertex_list = self.__get_indexed_vertex_list()

    def __get_indexed_vertex_list(self):
        return vertex_list_indexed(
            4,
            [0, 1, 2, 1, 2, 3],
            (
                f'v2f/{self.usage}',
                (
                    self.x, self.y,
                    self.x, self.y + self.height,
                    self.x + self.width, self.y,
                    self.x + self.width, self.y + self.height
                )
            ),
            (f'c4B/{self.usage}', tuple((list(self.color) + [self.transparency])*4))
        )

    def __update_vertices(self):
        self.vertex_list.vertices = [
            self.x, self.y,
            self.x, self.y + self.height,
            self.x + self.width, self.y,
            self.x + self.width, self.y + self.height
        ]
    
    def __update_colors(self):
        self.vertex_list.colors = tuple(list(self.color)*4)

    def move(self, dx: int=0, dy: int=0):
        self.x += dx
        self.y += dy
        self.__update_vertices()

    def scale(self, scale_x: float=1.0, scale_y: float=1.0):
        self.width = int(self.width*scale_x)
        self.height = int(self.height*scale_y)
        self.__update_vertices()

    def grow(self, dw: int=0, dh: int=0):
        self.width += dw
        self.height += dh
        self.__update_vertices()
    
    def change_color(self, color: Tuple[int]):
        self.color = color
        self.__update_colors()

    def draw(self):
        self.vertex_list.draw(gl.GL_TRIANGLES)

class GLGrid(metaclass=ABCMeta):
    def __init__(
        self, grid_width: int, grid_height: int, tile_width: int, tile_height: int,
        grid_origin_x: int=0, grid_origin_y: int=0
    ):
        if grid_width % tile_width != 0:
            raise Exception(f'grid_width % tile_width == {grid_width % tile_width} != 0')
        if grid_height % tile_height != 0:
            raise Exception(f'grid_height % tile_height == {grid_height % tile_height} != 0')
        self._grid_width, self._grid_height = grid_width, grid_height
        self._tile_width, self._tile_height = tile_width, tile_height
        self._grid_origin_x, self._grid_origin_y = grid_origin_x, grid_origin_y
        self.batch = Batch()
        self._vertex_list_grid = []

    @property
    def grid_width(self) -> int:
        return self._grid_width
    
    @property
    def grid_height(self) -> int:
        return self._grid_height
    
    @property
    def grid_shape(self) -> (int, int):
        return (self.grid_width, self.grid_height)

    @property
    def tile_width(self) -> int:
        return self._tile_width
    
    @property
    def tile_height(self) -> int:
        return self._tile_height

    @property
    def tile_shape(self) -> (int, int):
        return (self.tile_width, self.tile_height)

    @property
    def grid_origin_x(self) -> int:
        return self._grid_origin_x
    
    @property
    def grid_origin_y(self) -> int:
        return self._grid_origin_y
    
    @property
    def grid_origin(self) -> (int, int):
        return (self.grid_origin_x, self.grid_origin_y)

    @abstractmethod
    def _init_batch(self, usage: str):
        raise NotImplementedError
    
    def draw(self):
        self.batch.draw()

class RectangleGrid(GLGrid):
    def __init__(self, grid_width: int, grid_height: int, tile_width: int, tile_height: int, usage: str='dynamic', color_seq: List[Tuple[int]]=[(255,0,0), (0,255,0), (0,0,255)]):
        super().__init__(
            grid_width=grid_width, grid_height=grid_height,
            tile_width=tile_width, tile_height=tile_height
        )
        self._init_batch(usage=usage, color_seq=color_seq)
    
    def _init_batch(self, usage: str, color_seq: List[Tuple[int]]):
        check_value(usage, valid_value_list=['static', 'dynamic', 'stream'])
        n_rows = self.grid_height // self.tile_height
        n_cols = self.grid_width // self.tile_width
        for row in range(n_rows):
            vertex_list_row = []
            for col in range(n_cols):
                x = col * self.tile_width
                y = row * self.tile_height
                color = color_seq[(row * n_cols + col) % len(color_seq)]
                vertex_list = self.batch.add_indexed(
                    4,
                    gl.GL_TRIANGLES,
                    None,
                    [0, 1, 2, 1, 2, 3],
                    (
                        f'v2f/{usage}',
                        (
                            x, y,
                            x, y + self.tile_height,
                            x + self.tile_width, y,
                            x + self.tile_width, y + self.tile_height
                        )
                    ),
                    (f'c3B/{usage}', tuple(list(color)*4))
                )
                vertex_list_row.append(vertex_list)
            self._vertex_list_grid.append(vertex_list_row)

    def vertex_list(self, row: int, col: int):
        return self._vertex_list_grid[row][col]

class LineGrid(GLGrid):
    def __init__(
        self, grid_width: int, grid_height: int, tile_width: int, tile_height: int,
        grid_origin_x: int=0, grid_origin_y: int=0,
        usage: str='dynamic', color: Tuple[int]=(0,0,255)
    ):
        super().__init__(
            grid_width=grid_width, grid_height=grid_height,
            tile_width=tile_width, tile_height=tile_height,
            grid_origin_x=grid_origin_x, grid_origin_y=grid_origin_y
        )
        self._init_batch(usage=usage, color=color)
    
    def _init_batch(self, usage: str, color: Tuple[int]):
        check_value(usage, valid_value_list=['static', 'dynamic', 'stream'])
        n_rows = self.grid_height // self.tile_height
        n_cols = self.grid_width // self.tile_width
        horizontal_vertex_lists = []
        for row in range(n_rows+1):
            y = row * self.tile_height
            vertex_list = self.batch.add_indexed(
                2,
                gl.GL_LINES,
                None,
                [0, 1],
                (
                    f'v2f/{usage}',
                    (
                        0, (self.grid_origin_y+y)%self.grid_height,
                        self.grid_width, (self.grid_origin_y+y)%self.grid_height
                    )
                ),
                (f'c3B/{usage}', tuple(list(color)*2))
            )
            horizontal_vertex_lists.append(vertex_list)
        vertical_vertex_lists = []
        for col in range(n_cols+1):
            x = col * self.tile_width
            vertex_list = self.batch.add_indexed(
                2,
                gl.GL_LINES,
                None,
                [0, 1],
                (
                    f'v2f/{usage}',
                    (
                        (self.grid_origin_x+x)%self.grid_width, 0,
                        (self.grid_origin_x+x)%self.grid_width, self.grid_height
                    )
                ),
                (f'c3B/{usage}', tuple(list(color)*2))
            )
            vertical_vertex_lists.append(vertex_list)
        self._vertex_list_grid.append(horizontal_vertex_lists)
        self._vertex_list_grid.append(vertical_vertex_lists)

    def vertex_list(self, n: int, orientation: int='horizontal'):
        check_value(orientation, valid_value_list=['horizontal', 'vertical'])
        if orientation == 'horizontal':
            return self._vertex_list_grid[0][n]
        elif orientation == 'vertical':
            return self._vertex_list_grid[1][n]
        else:
            raise Exception