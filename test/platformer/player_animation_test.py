import pyglet
from pyglet_utils.platformer.resources import TileImages
from pyglet.window import Window, FPSDisplay
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet.text import Label

from pyglet_utils.platformer.player import Player
from pyglet_utils.platformer.grid import Grid
from pyglet_utils.platformer.frame import Frame
from pyglet_utils.platformer.platform import Platform
from pyglet_utils.platformer.render import RenderBox
from pyglet_utils.platformer.mouse import Mouse

# TODO: Implement interactive map maker (based on mouse input).
# TODO: Implement map save/load.
#       Prerequisite: Map maker
# TODO: Make it so that the position of objects only need to be calculated when
#       they are inside of the RenderBox.

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

        # Create Ground
        dirt_img = TileImages.dirtRight
        ground_grid_pos_list = [
            (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (2, -1), (3, -1), (3, 0), (4, -1), (5, -1), (5, 0), (6, -1), (7, -1), (7, 0), (8, -1)
        ]
        self.platform = Platform.from_grid_space_coords(grid_pos_list=ground_grid_pos_list, grid=self.grid, img_list=[dirt_img], batch=Batch(), frame=self.frame, name='Platform1')
        for block in self.platform.blocks:
            self.grid.add_obj(obj=block, name=block.name, parent_name=self.platform.name)
        self.renderbox.add_render_obj(self.platform)

        # Create Player
        self.player = Player(x=int(0.5*self.width), y=int(0.3*self.height), frame=self.frame, renderbox=self.renderbox, grid=self.grid, debug=False)
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

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_debug(self):
        self.player.toggle_debug()
        self.renderbox.toggle_debug()

    def on_mouse_enter(self, x, y):
        self.mouse.enter_window(x=x, y=y)
        self.mouse.update_cursor_rect()

    def on_mouse_leave(self, x, y):
        self.mouse.leave_window()
        self.mouse.update_cursor_rect()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.move(x=x, y=y, dx=dx, dy=dy)
        self.mouse.update_cursor_rect()

    def on_draw(self):
        self.clear()
        self.renderbox.draw_all_renderable_objects()
        self.mouse.draw()
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
            self.mouse.update_cursor_rect()
            self.player_coord_label.text = self.grid.get_coords_str(obj_name=self.player.name)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

game = GameWindow(
    width=700, height=700, caption='Walk Animation Test'
)
game.run()