import pyglet
from pyglet_utils.tutorial import resources
from pyglet.window import Window
from pyglet.image import Animation, ImageGrid
from pyglet.sprite import Sprite

# Create and open a window
window = Window(width=500, height=500, caption='Bird Atlas')

# Cut our cat up into a 5x5 grid of images to move through (sprite sheet)
bird_seq = ImageGrid(resources.bird, 3, 5)
bird_seq = bird_seq[10:] + bird_seq[5:10] + bird_seq[:4] # Fix order

bird_anim = Animation.from_image_sequence(sequence=bird_seq, duration=1/20, loop=True)
bird_sprite = Sprite(img=bird_anim, x=50, y=150)
bird_sprite.scale = 2

@window.event
def on_draw():
  window.clear()
  bird_sprite.draw()

if __name__ == '__main__':
  pyglet.app.run()