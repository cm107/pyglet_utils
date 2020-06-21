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

# TODO: Display player's grid coordinates.
# TODO: Make it so that the grid is fixed to the world coordinates and does not follow the player.
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
            grid_width=self.width-100, grid_height=self.height-100,
            tile_width=70, tile_height=70,
            grid_origin_x=0, grid_origin_y=0,
            default_grid_visible=False,
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
        self.player = Player(x=int(0.5*self.width), y=int(0.3*self.height), frame=self.frame, debug=False)
        self.grid.add_obj(obj=self.player, name=self.player.name, is_anchor_x_centered=True)
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

    def move_player(self, dx: int, dy: int):
        player_grid_obj = self.grid.contained_obj_list.get_obj_from_name(self.player.name)
        other_occupied_spaces = self.grid.contained_obj_list.get_occupied_spaces(exclude_names=[self.player.name])

        # Move X
        proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dx=dx)
        collision = False
        for proposed_player_occupied_space in proposed_player_occupied_spaces:
            if proposed_player_occupied_space in other_occupied_spaces:
                collision = True
                break
        if not collision:
            # player.x += dx
            self.player.set_x(x=self.player.x+dx, fix_camera=True)
            self.player.frame.move_camera(dx=-dx, exclude_names=[self.player.name])
            self.grid.move(dx=-dx)

        # Move Y
        proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dy=dy)
        collision = False
        for proposed_player_occupied_space in proposed_player_occupied_spaces:
            if proposed_player_occupied_space in other_occupied_spaces:
                collision = True
                break
        if not collision:
            # player.y += dy
            self.player.set_y(y=self.player.y+dy, fix_camera=True)
            self.player.frame.move_camera(dy=-dy, exclude_names=[self.player.name])
            self.grid.move(dy=-dy)
        else:
            self.player.vy = 0
            if dy < 0:
                if self.player.is_jumping:
                    self.player.stop_jumping()
                    if self.player.arrow_key_buffer.is_pressed:
                        self.player.start_walking(direction=self.player.arrow_key_buffer.buffer[-1])
                    else:
                        self.player.vx = 0

    def update(self, dt):
        dx = self.player.vx * dt
        dy = self.player.vy * dt
        self.player.vy -= 1*9.81*dt*60
        self.move_player(dx=dx, dy=dy)
        self.player_coord_label.text = self.grid.get_coords_str(obj_name=self.player.name)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

game = GameWindow(
    width=560+100, height=560+100, caption='Walk Animation Test'
)
game.run()