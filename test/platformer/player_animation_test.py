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

# TODO: Implement Contact Recognition so that the jump sprite can be used when I walk off of an edge.
#       Prerequisite: World Grid
# TODO: Create a rendering engine that decides which batches to render based on whether members of
#       a given batch are inside of a RenderBox, which should be just slightly larger than the frame.

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
            default_grid_visible=True,
            default_coord_labels_visible=True,
            coord_label_color=(255,0,0), coord_label_opacity=255,
            coord_label_font_size=8
        )

        # Create Ground
        dirt_img = TileImages.dirtRight
        dirt_tile_w, dirt_tile_h = dirt_img.width, dirt_img.height
        ground_list = []
        n_ground = int(self.width / dirt_tile_w)

        ground_pos_list = [(i*dirt_tile_w, 0) for i in range(n_ground)] + [(2*dirt_tile_w, dirt_tile_h)]
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

    def on_draw(self):
        self.clear()
        self.platform.draw()
        self.player.draw()
        self.grid.draw()
        self.fps_display.draw()
        self.player_coord_label.draw()

    def on_key_press(self, symbol, modifiers):
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
        elif symbol == key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
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
        dx = self.player.vx * dt
        dy = self.player.vy * dt
        self.player.vy -= 1*9.81*dt*60
        self.player.move(dx=dx, dy=dy)
        self.player_coord_label.text = self.grid.get_coords_str(obj_name=self.player.name)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

game = GameWindow(
    width=700, height=700, caption='Walk Animation Test'
)
game.run()