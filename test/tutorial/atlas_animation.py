import pyglet
from pyglet_utils.tutorial import resources
from pyglet.window import Window
from pyglet.image import Animation
from pyglet.sprite import Sprite

# Create and open a window
window = Window(width=500, height=500, caption='Bird Atlas')

bird_anim = Animation.from_image_sequence(sequence=resources.bird_seq, duration=1/20, loop=True)
bird_sprite = Sprite(img=bird_anim, x=50, y=150)
bird_sprite.scale = 2

@window.event
def on_draw():
  window.clear()
  bird_sprite.draw()

if __name__ == '__main__':
  pyglet.app.run()