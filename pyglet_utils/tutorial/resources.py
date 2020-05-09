import pyglet

pyglet.resource.path = ["/home/clayton/Pictures/sprites"]
pyglet.resource.reindex()

player = pyglet.resource.image("player.png")
enemy = pyglet.resource.image("enemy.png")
dimple = pyglet.resource.image("dimple.png")
boss = pyglet.resource.image("boss.png")
bird = pyglet.resource.image("atlas/bird.png")