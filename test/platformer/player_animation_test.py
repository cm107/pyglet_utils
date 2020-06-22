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

# TODO: Create RenderBox as a member of GameWindow. RenderBox should be just slightly larger than Frame.
# TODO: Create a rendering engine that decides which batches to render based on whether members of
#       a given batch are inside of a RenderBox.
# TODO: Implement interactive map maker (based on mouse input).
#       Prerequisite: Rendering Engine
# TODO: Implement map save/load.
#       Prerequisite: Map maker

class GameWindow(Window):
    def __init__(self, width: int, height: int, caption: str):
        super().__init__(width=width, height=height, caption=caption)

        self.fps_display = FPSDisplay(self)
        self.frame = Frame(window=self)

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
        dirt_tile_w, dirt_tile_h = dirt_img.width, dirt_img.height
        n_ground = int(self.width / dirt_tile_w)

        ground_pos_list = [(i*dirt_tile_w, 0) for i in range(n_ground)] + \
            [(2*dirt_tile_w, i*dirt_tile_h) for i in range(1,3)] + \
            [(6*dirt_tile_w, i*dirt_tile_h) for i in range(1,2)]
        self.platform = Platform(pos_list=ground_pos_list, img_list=[dirt_img], batch=Batch(), frame=self.frame, name='Platform1')

        for block in self.platform.blocks:
            self.grid.add_obj(obj=block, name=block.name)

        # Create Player
        self.player = Player(x=int(0.5*self.width), y=int(0.3*self.height), frame=self.frame, grid=self.grid, debug=False)
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

    def toggle_pause(self):
        self.paused = not self.paused

    def on_draw(self):
        self.clear()
        self.platform.draw()
        self.player.draw()
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
                self.player.toggle_debug()
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
                self.player.toggle_debug()

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
            self.player_coord_label.text = self.grid.get_coords_str(obj_name=self.player.name)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

game = GameWindow(
    width=700, height=700, caption='Walk Animation Test'
)
game.run()