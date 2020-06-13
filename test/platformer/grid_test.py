import pyglet
from pyglet.window import Window, FPSDisplay
from pyglet_utils.platformer.shapes import Rectangle, RectangleGrid, LineGrid

# Create and open a window
window = Window(width=550, height=500, caption='Grid Drawing Test')
fps_display = FPSDisplay(window)

# tile_grid = RectangleGrid(
#     grid_width=window.width, grid_height=window.height,
#     tile_width=50, tile_height=50, usage='static',
#     color_seq=[(0,0,0),(255,255,255)]
# )
tile_grid = LineGrid(
    grid_width=window.width, grid_height=window.height,
    tile_width=50, tile_height=50, usage='static',
    color=(255,255,255)
)
rectangle = Rectangle(x=50, y=50, width=100, height=100)

@window.event
def on_draw():
    window.clear()
    rectangle.draw()
    tile_grid.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_key_release(symbol, modifiers):
    pass

def update(dt):
    rectangle.move(dx=1)

if __name__ == '__main__':
    fps = 60
    pyglet.clock.schedule_interval(update, 1/fps)
    pyglet.app.run()