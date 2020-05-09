import pyglet
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet_utils.tutorial import resources

game_window = Window()
pyglet.gl.glClearColor(0, 0, 0, 1)

batch = Batch()

@game_window.event
def on_draw():
    game_window.clear()
    player_sprite.draw()
    enemy_sprite.draw()
    dimple_batch.draw()
    
def update(dt):
    for dimple in dimple_list:
        dimple.x += 1
    pass

if __name__ == '__main__':
    import random

    resources.player.width, resources.player.height = 250, 250
    resources.enemy.width, resources.enemy.height = 250, 250
    resources.dimple.width, resources.dimple.height = 20, 20
    player_sprite = Sprite(img=resources.player, x=10, y=10)
    enemy_sprite = Sprite(img=resources.enemy, x=100, y=100)
    dimple_batch = Batch()
    dimple_list = []
    for i in range(20):
        temp_dimple = Sprite(img=resources.dimple, x=random.randint(10, 300), y=random.randint(10, 300), batch=dimple_batch)
        dimple_list.append(temp_dimple)
    pyglet.clock.schedule_interval(update, 0.5)
    pyglet.app.run()