import pyglet
from pyglet.image import ImageGrid

pyglet.resource.path = ["/home/clayton/Pictures/sprites"]
pyglet.resource.reindex()

player = pyglet.resource.image("player.png")
enemy = pyglet.resource.image("enemy.png")
dimple = pyglet.resource.image("dimple.png")
boss = pyglet.resource.image("boss.png")
bird = pyglet.resource.image("atlas/bird.png")
bird_seq = ImageGrid(bird, 3, 5)
bird_seq = bird_seq[10:] + bird_seq[5:10] + bird_seq[:4] # Fix order