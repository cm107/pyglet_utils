import pyglet
from pyglet_utils.platformer.resources import TileImages
from pyglet.window import Window, FPSDisplay
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet_utils.platformer.player import Player
from pyglet_utils.platformer.shapes import LineGrid
from pyglet_utils.platformer.grid import Grid
from pyglet_utils.platformer.frame import Frame
from pyglet_utils.platformer.platform import Platform

# TODO: Make it so that the grid is fixed to the world coordinates and does not follow the player.
# TODO: Implement Contact Recognition so that the jump sprite can be used when I walk off of an edge.
#       Prerequisite: World Grid
# TODO: Create a rendering engine that decides which batches to render based on whether members of
#       a given batch are inside of a RenderBox, which should be just slightly larger than the frame.

# Create and open a window
window = Window(width=560, height=560, caption='Walk Animation Test')
fps_display = FPSDisplay(window)

frame = Frame(window=window)

grid = Grid(
    grid_width=window.width, grid_height=window.height,
    tile_width=35, tile_height=35,
    default_grid_visible=False,
    coord_label_color=(255,0,0), coord_label_opacity=255,
    coord_label_font_size=6
)

# Create Ground
dirt_img = TileImages.dirtRight
dirt_tile_w, dirt_tile_h = dirt_img.width, dirt_img.height
ground_list = []
n_ground = int(window.width / dirt_tile_w)

ground_pos_list = [(i*dirt_tile_w, 0) for i in range(n_ground)] + [(2*dirt_tile_w, dirt_tile_h)]
platform = Platform(pos_list=ground_pos_list, img_list=[dirt_img], batch=Batch(), frame=frame, name='Platform1')

for block in platform.blocks:
    grid.add_obj(obj=block, name=block.name)

# Create Player
player = Player(x=int(0.5*window.width), y=int(0.3*window.height), frame=frame, debug=False)
grid.add_obj(obj=player, name='player', is_anchor_x_centered=True)

@window.event
def on_draw():
    window.clear()
    platform.draw()
    player.draw()
    grid.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global player, grid
    if symbol == key.LEFT:
        player.arrow_key_buffer.press('left')
        if not player.is_jumping:
            player.start_walking(direction='left')
        else:
            player.face(direction='left')
    elif symbol == key.RIGHT:
        player.arrow_key_buffer.press('right')
        if not player.is_jumping:
            player.start_walking(direction='right')
        else:
            player.face(direction='right')
    elif symbol == key.N:
        player.toggle_player()
    elif symbol == key.SPACE:
        if not player.is_jumping:
            player.start_jumping()
    elif symbol == key.G:
        grid.toggle_grid_visible()
    elif symbol == key.C:
        grid.toggle_coord_labels_visible()
    elif symbol == key.D:
        player.toggle_debug()

@window.event
def on_key_release(symbol, modifiers):
    global player
    if symbol == key.LEFT:
        player.arrow_key_buffer.release('left')
        if player.is_walking:
            if player.arrow_key_buffer.is_released:
                player.stop_walking()
            else:
                player.start_walking(direction=player.arrow_key_buffer.buffer[-1])
    elif symbol == key.RIGHT:
        player.arrow_key_buffer.release('right')
        if player.is_walking:
            if player.arrow_key_buffer.is_released:
                player.stop_walking()
            else:
                player.start_walking(direction=player.arrow_key_buffer.buffer[-1])

def move_player(dx: int, dy: int):
    global player, grid

    player_grid_obj = grid.contained_obj_list.get_obj_from_name('player')
    other_occupied_spaces = grid.contained_obj_list.get_occupied_spaces(exclude_names=['player'])

    # Move X
    proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dx=dx)
    collision = False
    for proposed_player_occupied_space in proposed_player_occupied_spaces:
        if proposed_player_occupied_space in other_occupied_spaces:
            collision = True
            break
    if not collision:
        # player.x += dx
        player.set_x(x=player.x+dx, fix_camera=True)
        player.frame.move_camera(dx=-dx, exclude_names=[player.name])

    # Move Y
    proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dy=dy)
    collision = False
    for proposed_player_occupied_space in proposed_player_occupied_spaces:
        if proposed_player_occupied_space in other_occupied_spaces:
            collision = True
            break
    if not collision:
        # player.y += dy
        player.set_y(y=player.y+dy, fix_camera=True)
        player.frame.move_camera(dy=-dy, exclude_names=[player.name])
    else:
        player.vy = 0
        if dy < 0:
            if player.is_jumping:
                player.stop_jumping()
                if player.arrow_key_buffer.is_pressed:
                    player.start_walking(direction=player.arrow_key_buffer.buffer[-1])
                else:
                    player.vx = 0

def update(dt):
    global player, grid, platform, frame

    dx = player.vx * dt
    dy = player.vy * dt
    player.vy -= 1*9.81*dt*60
    move_player(dx=dx, dy=dy)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()