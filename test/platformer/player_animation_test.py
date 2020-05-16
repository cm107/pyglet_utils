import pyglet
from pyglet_utils.platformer.resources import PlayerImages, TileImages
from pyglet.window import Window, FPSDisplay
from pyglet.image import Animation
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.graphics import Batch

# Create and open a window
window = Window(width=500, height=500, caption='Walk Animation Test')
fps_display = FPSDisplay(window)

# Create Ground
dirt_img = TileImages.dirtMid
dirt_tile_w, dirt_tile_h = dirt_img.width, dirt_img.height
ground_batch = Batch()
ground_list = []
n_ground = int(window.width / dirt_tile_w)
for i in range(n_ground):
    ground_list.append(Sprite(img=dirt_img, x=i*dirt_tile_w, y=0, batch=ground_batch))

# Create Player
player_select = 0
player_res = PlayerImages.p1

def set_player(idx: int):
    global player_select, player_res
    player_select = idx % 3
    if player_select == 0:
        player_res = PlayerImages.p1
    elif player_select == 1:
        player_res = PlayerImages.p2
    elif player_select == 2:
        player_res = PlayerImages.p3
    else:
        raise Exception

sprite = Sprite(img=player_res.idle_right, x=180, y=dirt_tile_h)
sprite.scale = 2
base_speed = 200
player_vx, player_vy = 0, 0
current_state = key.RIGHT
grounded = True

@window.event
def on_draw():
    window.clear()
    ground_batch.draw()
    sprite.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global player_vx, player_vy, current_state, grounded
    if grounded:
        if symbol == key.LEFT:
            sprite.image = player_res.walk_left_anim
            player_vx = -base_speed
            current_state = symbol
        elif symbol == key.RIGHT:
            sprite.image = player_res.walk_right_anim
            player_vx = base_speed
            current_state = symbol
        elif symbol == key.UP:
            set_player(player_select+1)
            on_key_release(symbol=current_state, modifiers=modifiers)
        elif symbol == key.DOWN:
            set_player(player_select-1)
            on_key_release(symbol=current_state, modifiers=modifiers)
        elif symbol == key.SPACE:
            if current_state == key.RIGHT:
                sprite.image = player_res.jump_right
            elif current_state == key.LEFT:
                sprite.image = player_res.jump_left
            else:
                raise Exception(f'current_state: {current_state}')
            grounded = False
            player_vy = 15


@window.event
def on_key_release(symbol, modifiers):
    global player_vx, current_state
    if symbol == key.LEFT:
        sprite.image = player_res.idle_left
        player_vx = 0
        current_state = symbol
    elif symbol == key.RIGHT:
        sprite.image = player_res.idle_right
        player_vx = 0
        current_state = symbol

def update(dt):
    global player_vy, grounded
    sprite.x += player_vx * dt
    if not grounded:
        if sprite.y >= dirt_tile_h:
            sprite.y += int(player_vy * dt * 60)
            player_vy -= 0.1*9.81*dt*60
        else:
            sprite.y = dirt_tile_h
            player_vy = 0
            grounded = True
            if current_state == key.RIGHT:
                sprite.image = player_res.idle_right
            elif current_state == key.LEFT:
                sprite.image = player_res.idle_left
            else:
                raise Exception(f'current_state: {current_state}')
    
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()