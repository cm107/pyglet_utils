from __future__ import division

from pyglet.window import key
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
import pyglet
from pyglet_utils.tutorial import resources

game_window = pyglet.window.Window(
    width=800,
    height=650,
    caption="Pyglet Tutorial"
)

game_window.set_mouse_visible(False)
pyglet.gl.glClearColor(0.4, 0.4, 1, 1)

resources.player.width, resources.player.height = 100, 100
player = Sprite(resources.player, x=400, y=0)
player_x = 0
player_y = 0
player_speed = 150

resources.enemy.width, resources.enemy.height = 100, 100
enemies_batch = Batch()
enemies_sprites = []
enemy_positions = [
    (250, 100), (550, 100), (300, 300),
    (500, 300), (150, 450), (650, 450)
]
for x, y in enemy_positions:
    enemies_sprites.append(
        Sprite(
            img=resources.enemy,
            x=x, y=y,
            batch=enemies_batch
        )
    )

resources.boss.width, resources.boss.height = 100, 100
boss = Sprite(resources.boss, x=400, y=550)
boss.scale = 2

@game_window.event
def on_draw():
    game_window.clear()
    enemies_batch.draw()
    boss.draw()
    player.draw()


@game_window.event
def on_key_press(symbol, modifiers):
    global player_x, player_y
    if symbol == key.LEFT:
        player_x = -player_speed
        player_y = 0
    elif symbol == key.RIGHT:
        player_x = player_speed
        player_y = 0
    elif symbol == key.UP:
        player_x = 0
        player_y = player_speed
    elif symbol == key.DOWN:
        player_x = 0
        player_y = -player_speed
    elif symbol == key.SPACE:
        player_x = 0
        player_y = 0


def update(dt):
    player.x += player_x * dt
    player.y += player_y * dt


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()