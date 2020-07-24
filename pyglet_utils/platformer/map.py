from typing import List, cast
from pyglet.image import AbstractImage, TextureRegion
from pyglet.sprite import Sprite
from pyglet.graphics import Batch

from common_utils.base.basic import MultiParameterHandler

from .resources import TileImages, ItemImages
from .grid import Grid
from .frame import Frame
from .platform import Platform
from .render import RenderBox
from .mouse import Mouse
from .game_obj import GameObjectHandler
from ..lib.shapes import Rectangle
from ..lib.exception_handler import Error

class BlockSelector:
    def __init__(self, images_constructor: type):
        assert type(images_constructor) is type
        self.images_constructor = images_constructor
        self.keys = [key for key, val in self.images_constructor.__dict__.items() if type(val) is TextureRegion]
        if len(self.keys) == 0:
            raise Error(
                f"""
                Couldn't find any items of type TextureRegion in {images_constructor.__class__.__name__}.
                This selector only works with TextureRegions. Please double check your images_constructor class.
                """
            )
        self.current_idx = 0 if len(self.keys) > 0 else None
        self.current_img = self._get_current_img()
    
    def _get_current_img(self) -> TextureRegion:
        return self.images_constructor.__dict__[self.keys[self.current_idx]]

    def toggle_img(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        self.current_img = self._get_current_img()

class BlockSelectorHandler(MultiParameterHandler['BlockSelectorHandler', 'BlockSelector']):
    def __init__(self, block_selectors: List[BlockSelector]):
        super().__init__(obj_type=BlockSelector, obj_list=block_selectors)
        self.block_selectors = self.obj_list
        if len(self.block_selectors) == 0:
            raise Error(
            f"""
            BlockSelectorHandler constructor requires at least one selector be provided.
            """
            )
        self.current_idx = 0
        self.current_selector = self._get_current_selector()

    def _get_current_selector(self) -> BlockSelector:
        return self.block_selectors[self.current_idx]

    def toggle_selector(self):
        self.current_idx = (self.current_idx + 1) % len(self.block_selectors)
        self.current_selector = self._get_current_selector()
    
    @property
    def img(self) -> TextureRegion:
        return self.current_selector.current_img

class MapMaker:
    def __init__(
        self, frame: Frame, grid: Grid, renderbox: RenderBox, mouse: Mouse, game_obj_handler: GameObjectHandler,
        platform_list: List[Platform]=None, block_queue: Platform=None
    ):
        self.frame = frame
        self.grid = grid
        self.renderbox = renderbox
        self.mouse = mouse
        self.game_obj_handler = game_obj_handler
        self.platform_list = platform_list if platform_list is not None else []
        for platform in self.platform_list:
            self.game_obj_handler.append(platform)
        self.block_queue = block_queue if block_queue is not None else \
            Platform(frame=self.frame, grid=self.grid, renderbox=self.renderbox, batch=Batch(), name=f'Platform{len(self.platform_list)}')
        self.game_obj_handler.append(self.block_queue)

        # Block Preview Related
        self.block_selector_handler = BlockSelectorHandler(
            [
                BlockSelector(TileImages),
                BlockSelector(ItemImages)
            ]
        )
        self.block_preview_rect_color = None
        self.block_preview_rect_opacity = 50
        self.block_preview_sprite_opacity = 130
        self.block_preview_rect = cast(Rectangle, None)
        self.block_preview_sprite = cast(Sprite, None)

    def add_block_to_queue(self, x: int, y: int, img: AbstractImage):
        self.block_queue.add_block(x=x, y=y, img=img)
        self.game_obj_handler.append(self.block_queue.blocks[-1], to_renderbox=False)
    
    def add_block_to_queue_from_space(self, grid_space_x: int, grid_space_y: int, img: AbstractImage):
        x, y = self.grid.grid_space_to_world_coord(space_x=grid_space_x, space_y=grid_space_y)
        self.add_block_to_queue(x=x, y=y, img=img)

    def add_block_to_queue_from_mouse(self):
        self.add_block_to_queue_from_space(grid_space_x=self.mouse.grid_space_x, grid_space_y=self.mouse.grid_space_y, img=self.block_selector_handler.img)

    def remove_queue_block(self, name: str):
        self.game_obj_handler.remove(name)
        self.block_queue.remove_block(name=name)

    def remove_queue_block_from_space(self, grid_space_x: int, grid_space_y: int):
        names = self.grid.grid_spaces_to_names([(grid_space_x, grid_space_y)])
        for name in names:
            self.remove_queue_block(name=name)

    def remove_queue_block_from_mouse(self):
        self.remove_queue_block_from_space(grid_space_x=self.mouse.grid_space_x, grid_space_y=self.mouse.grid_space_y)

    def push_queue(self):
        self.platform_list.append(self.block_queue.copy())
        self.block_queue = Platform(frame=self.frame, grid=self.grid, renderbox=self.renderbox, batch=Batch(), name=f'Platform{len(self.platform_list)}')
        self.game_obj_handler.append(self.block_queue)
    
    def update_block_preview_rect_color(self):
        raise NotImplementedError

    def update_block_preview(self):
        if self.mouse.grid_space_x is not None and self.mouse.grid_space_y is not None:
            rect_x = self.grid.tile_width * self.mouse.grid_space_x + self.grid.grid_origin_x - self.frame.x
            rect_y = self.grid.tile_height * self.mouse.grid_space_y + self.grid.grid_origin_y - self.frame.y
            if self.block_preview_sprite is None:
                self.block_preview_rect = Rectangle(
                    x=rect_x, y=rect_y,
                    width=self.grid.tile_width, height=self.grid.tile_height,
                    color=(100,255,20), transparency=self.block_preview_rect_opacity
                )
                self.block_preview_sprite = Sprite(
                    img=self.block_selector_handler.img, x=rect_x, y=rect_y
                )
                self.block_preview_sprite.opacity = self.block_preview_sprite_opacity
            else:
                self.block_preview_rect.move_to(x=rect_x, y=rect_y)
                self.block_preview_sprite.position = (rect_x, rect_y)

    def reset_block_preview(self):
        self.block_preview_rect = None
        self.block_preview_sprite = None

    def toggle_block_preview_selector(self):
        print(f'Flag1')
        self.block_selector_handler.toggle_selector()
        self.reset_block_preview()
        self.update_block_preview()
    
    def toggle_block_preview_img(self):
        print(f'Flag2')
        self.block_selector_handler.current_selector.toggle_img()
        self.reset_block_preview()
        self.update_block_preview()

    def draw_block_preview(self):
        if self.block_preview_sprite is not None:
            self.block_preview_rect.draw()
            self.block_preview_sprite.draw()