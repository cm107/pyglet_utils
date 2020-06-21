import pyglet
from pyglet.window import Window, FPSDisplay
from pyglet_utils.platformer.shapes import GL_Point2D, GL_Points2D, GL_TriangleStrip2D, GL_Quads2D, Rectangle

# Create and open a window
window = Window(width=500, height=500, caption='Shape Drawing Test')
fps_display = FPSDisplay(window)

red, green, blue = [255,0,0], [0,255,0], [0,0,255]

test_points = GL_Points2D.from_list(
    [
        [10, 10], [100, 10], [10, 100], [100, 100], [200, 200]
    ]
)

test_triangles = GL_TriangleStrip2D.from_list(
    coord_list=[
        [100, 100], [200, 100], [100, 200], [200, 200]
    ],
    color_list=[red, blue, blue, red]
)

rectangle = Rectangle(x=50, y=50, width=100, height=100, color=(255,0,0), transparency=100)

@window.event
def on_draw():
    window.clear()
    test_points.draw()
    test_triangles.draw(idx_order=[0,1,2,3])
    rectangle.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_key_release(symbol, modifiers):
    pass

def update(dt):
    test_triangles.move(dx=1)
    rectangle.move(dx=1)
    rectangle.scale(scale_y=1.01)
    
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()