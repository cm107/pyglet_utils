import pyglet
from pyglet_utils.platformer.resources import PlayerImages
from pyglet.window import Window, FPSDisplay
from pyglet.image import Animation
from pyglet.sprite import Sprite
from pyglet.window import key

# Create and open a window
window = Window(width=500, height=500, caption='Walk Animation Test')
fps_display = FPSDisplay(window)

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

sprite = Sprite(img=player_res.idle_right, x=180, y=150)
sprite.scale = 2
base_speed = 200
player_speed = 0
current_state = key.RIGHT

@window.event
def on_draw():
  window.clear()
  sprite.draw()
  fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global player_speed, current_state
    if symbol == key.LEFT:
        sprite.image = player_res.walk_left_anim
        player_speed = -base_speed
        current_state = symbol
    elif symbol == key.RIGHT:
        sprite.image = player_res.walk_right_anim
        player_speed = base_speed
        current_state = symbol
    elif symbol == key.UP:
        set_player(player_select+1)
        on_key_release(symbol=current_state, modifiers=modifiers)
    elif symbol == key.DOWN:
        set_player(player_select-1)
        on_key_release(symbol=current_state, modifiers=modifiers)


@window.event
def on_key_release(symbol, modifiers):
    global player_speed, current_state
    if symbol == key.LEFT:
        sprite.image = player_res.idle_left
        player_speed = 0
        current_state = symbol
    elif symbol == key.RIGHT:
        sprite.image = player_res.idle_right
        player_speed = 0
        current_state = symbol

def update(dt):
    sprite.x += player_speed * dt

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()