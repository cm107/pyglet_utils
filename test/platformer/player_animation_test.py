import pyglet
from pyglet_utils.platformer.resources import TileImages, ItemImages
from pyglet.window import Window, FPSDisplay, mouse as window_mouse
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet.text import Label

from pyglet_utils.platformer.player import Player
from pyglet_utils.platformer.grid import Grid
from pyglet_utils.platformer.frame import Frame
from pyglet_utils.platformer.platform import Platform, PlatformBlock
from pyglet_utils.platformer.render import RenderBox
from pyglet_utils.platformer.mouse import Mouse
from pyglet_utils.platformer.game_obj import GameObjectHandler
from pyglet_utils.lib.shapes import Rectangle
from typing import cast

# TODO: Make it so that the block sprite can be previewed with a low opacity before it is placed.
# TODO: Implement map save/load.
#       Prerequisite: Map maker
# TODO: Make it so that the position of objects only need to be calculated when
#       they are inside of the RenderBox.

from typing import List
from pyglet.image import AbstractImage

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
        self.block_preview_rect_color = None
        self.current_img = ItemImages.bomb
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
        self.add_block_to_queue_from_space(grid_space_x=self.mouse.grid_space_x, grid_space_y=self.mouse.grid_space_y, img=self.current_img)

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
                    img=self.current_img, x=rect_x, y=rect_y
                )
                self.block_preview_sprite.opacity = self.block_preview_sprite_opacity
            else:
                self.block_preview_rect.move_to(x=rect_x, y=rect_y)
                self.block_preview_sprite.position = (rect_x, rect_y)

    def reset_block_preview(self):
        self.block_preview_rect = None
        self.block_preview_sprite = None

    def draw_block_preview(self):
        if self.block_preview_sprite is not None:
            self.block_preview_rect.draw()
            self.block_preview_sprite.draw()

class GameWindow(Window):
    def __init__(self, width: int, height: int, caption: str):
        super().__init__(width=width, height=height, caption=caption)
        self.set_mouse_visible(True)
        self.fps_display = FPSDisplay(self)
        self.frame = Frame(window=self)

        # Create Render Box
        self.renderbox = RenderBox(frame=self.frame, render_distance_proportion=1.2)

        self.grid = Grid(
            grid_width=self.width, grid_height=self.height,
            tile_width=70, tile_height=70,
            frame=self.frame,
            grid_origin_x=70, grid_origin_y=70,
            default_grid_visible=False,
            default_coord_labels_visible=True,
            coord_label_color=(255,0,0), coord_label_opacity=255,
            coord_label_font_size=8
        )

        # Create GameObjectHandler
        self.game_obj_handler = GameObjectHandler(frame=self.frame, grid=self.grid, renderbox=self.renderbox)

        # Create Ground
        dirt_img = TileImages.dirtRight
        ground_grid_pos_list = [
            (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1), (6, -1), (7, -1), (8, -1)
        ]
        platform = Platform.from_grid_space_coords(
            grid_pos_list=ground_grid_pos_list, img_list=[dirt_img], batch=Batch(),
            frame=self.frame, grid=self.grid, renderbox=self.renderbox, name='Platform0'
        )

        # Create Player
        self.player = Player(x=int(0.5*self.width), y=int(0.3*self.height), frame=self.frame, grid=self.grid, renderbox=self.renderbox, debug=False)
        self.game_obj_handler.append(self.player)
        self.player_coord_label = Label(
            text=self.grid.get_coords_str(obj_name=self.player.name),
            font_name='Times New Roman',
            font_size=15,
            x=int(0.50*self.width), y=int(0.02*self.height),
            color=tuple([0, 255, 0] + [255])
        )

        # Pause Related
        self.paused = False
        self.paused_text = Label(
            text='Paused',
            font_name='Times New Roman',
            font_size=30,
            x=int(0.50*self.width), y=int(0.98*self.height),
            color=tuple([255, 100, 100] + [255]),
            anchor_x='center', anchor_y='top', bold=True
        )

        # Mouse Related
        self.mouse = Mouse(grid=self.grid, frame=self.frame)

        # MapMaker Related
        self.map_maker = MapMaker(
            frame=self.frame, renderbox=self.renderbox, grid=self.grid, mouse=self.mouse, game_obj_handler=self.game_obj_handler,
            platform_list=[platform], block_queue=None
        )

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_debug(self):
        self.player.toggle_debug()
        self.renderbox.toggle_debug()

    def on_mouse_enter(self, x, y):
        self.mouse.enter_window(x=x, y=y)
        self.mouse.update_grid_space()
        self.map_maker.update_block_preview()

    def on_mouse_leave(self, x, y):
        self.mouse.leave_window()
        self.map_maker.reset_block_preview()
        self.mouse.update_grid_space()
        self.map_maker.update_block_preview()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.move(x=x, y=y, dx=dx, dy=dy)
        self.mouse.update_grid_space()
        self.map_maker.update_block_preview()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        space_x, space_y = self.grid.world_coord_to_grid_space(x=x+self.frame.x, y=y+self.frame.y)
        if button == window_mouse.LEFT:
            if (space_x, space_y) not in self.grid.contained_obj_list.get_occupied_spaces(include_names=self.frame.get_all_obj_names_in_frame()):
                print('Added')
                self.map_maker.add_block_to_queue_from_mouse()
        elif button == window_mouse.RIGHT:
            if (space_x, space_y) in self.grid.contained_obj_list.get_occupied_spaces(include_names=self.frame.get_all_obj_names_in_frame()):
                print('Removed')
                self.map_maker.remove_queue_block_from_mouse()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_draw(self):
        self.clear()
        self.renderbox.draw_all_renderable_objects()
        self.map_maker.draw_block_preview()
        self.grid.draw()
        self.fps_display.draw()
        self.player_coord_label.draw()
        if self.paused:
            self.paused_text.draw()

    def on_key_press(self, symbol, modifiers):
        if not self.paused:
            if symbol == key.LEFT:
                self.player.arrow_key_buffer.press('left')
                if not self.player.is_jumping:
                    self.player.start_walking(direction='left')
                else:
                    self.player.face(direction='left')
            elif symbol == key.RIGHT:
                self.player.arrow_key_buffer.press('right')
                if not self.player.is_jumping:
                    self.player.start_walking(direction='right')
                else:
                    self.player.face(direction='right')
            elif symbol == key.N:
                self.player.toggle_player()
            elif symbol == key.SPACE:
                if not self.player.is_jumping:
                    self.player.start_jumping()
            elif symbol == key.G:
                self.grid.toggle_grid_visible()
            elif symbol == key.C:
                self.grid.toggle_coord_labels_visible()
            elif symbol == key.D:
                self.toggle_debug()
            elif symbol == key.Q:
                self.map_maker.push_queue()
            elif symbol == key.P:
                self.toggle_pause()
            elif symbol == key.ESCAPE:
                self.close()
        else:
            if symbol == key.P:
                self.toggle_pause()
            elif symbol == key.ESCAPE:
                self.close()
            elif symbol == key.G:
                self.grid.toggle_grid_visible()
            elif symbol == key.C:
                self.grid.toggle_coord_labels_visible()
            elif symbol == key.D:
                self.toggle_debug()
            elif symbol == key.Q:
                self.map_maker.push_queue()

    def on_key_release(self, symbol, modifiers):
        if not self.paused:
            if symbol == key.LEFT:
                self.player.arrow_key_buffer.release('left')
                if self.player.is_walking:
                    if self.player.arrow_key_buffer.is_released:
                        self.player.stop_walking()
                    else:
                        self.player.start_walking(direction=self.player.arrow_key_buffer.buffer[-1])
            elif symbol == key.RIGHT:
                self.player.arrow_key_buffer.release('right')
                if self.player.is_walking:
                    if self.player.arrow_key_buffer.is_released:
                        self.player.stop_walking()
                    else:
                        self.player.start_walking(direction=self.player.arrow_key_buffer.buffer[-1])

    def update(self, dt):
        if not self.paused:
            self.player.vy -= 1*9.81*dt*60
            dx = self.player.vx * dt
            dy = self.player.vy * dt
            self.player.move(dx=dx, dy=dy)
            self.mouse.update_grid_space()
            # self.mouse.update_cursor_rect()
            self.map_maker.update_block_preview()
            self.player_coord_label.text = self.grid.get_coords_str(obj_name=self.player.name)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

game = GameWindow(
    width=700, height=700, caption='Walk Animation Test'
)
game.run()