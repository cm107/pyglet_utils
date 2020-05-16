from typing import List

import pyglet
from pyglet_utils.platformer.resources import PlayerImages, TileImages
from pyglet.window import Window, FPSDisplay
from pyglet.image import Animation
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet.shapes import Circle, Rectangle

# TODO: Implement a TileGrid for the sake of easily finding the objects around the player that need to be checked for collision.
# TODO: Change the collision algorithm so that movement checks are based on contacts.
#       E.g. The player can only move right when contact_right is None.
#       When contact_right is equal to a tile, movement proposals in that direction are ignored.
#       The contact can only be released when vx is set to a negative number.

class Player:
    def __init__(self, x: int, y: int, batch: Batch=None, debug: bool=False):
        # Player Sprite Select Related
        self.player_res_list = [PlayerImages.p1, PlayerImages.p2, PlayerImages.p3]
        self.player_select = 0
        self.player_res = self.player_res_list[self.player_select]
        self.sprite = Sprite(img=self.player_res.jump_right, x=x, y=y, batch=batch)

        # Movement Related
        self.BASE_WALKING_SPEED = 200
        self.BASE_JUMPING_SPEED = 300
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 'right'
        self.status = 'jumping'

        # Debug
        self.debug = debug
        self.ref_point = Circle(x=self.x, y=self.y, radius=5, color=(255,0,0))
        self.ref_rect = Rectangle(x=self.x, y=self.y, width=self.width, height=self.height, color=(0,0,255))
        self.ref_rect.anchor_x = self.ref_rect.width // 2

    @property
    def x(self) -> int:
        return self.sprite.x
    
    @x.setter
    def x(self, x: int):
        self.sprite.x = x
        if self.debug:
            self.ref_point.x = x
            self.ref_rect.x = x

    @property
    def y(self) -> int:
        return self.sprite.y
    
    @y.setter
    def y(self, y: int):
        self.sprite.y = y
        if self.debug:
            self.ref_point.y = y
            self.ref_rect.y = y

    @property
    def width(self) -> int:
        return self.player_res.idle_right.width
    
    @property
    def height(self) -> int:
        return self.player_res.idle_right.height

    @property
    def shape(self) -> (int, int):
        return (self.sprite.width, self.sprite.height)

    def change_player(self, idx: int):
        self.player_res = self.player_res_list[idx]
        self.player_select = idx
        self.update_sprite()

    def toggle_player(self):
        self.change_player((self.player_select+1) % len(self.player_res_list))

    def change_sprite(self, image):
        self.sprite.image = image
        if self.debug:
            self.ref_rect.width = self.sprite.width
            self.ref_rect.height = self.sprite.height
            self.ref_rect.anchor_x = self.ref_rect.width // 2

    def update_sprite(self):
        if self.status == 'idle':
            if self.facing == 'right':
                self.change_sprite(self.player_res.idle_right)
            elif self.facing == 'left':
                self.change_sprite(self.player_res.idle_left)
            else:
                raise Exception
        elif self.status == 'jumping':
            if self.facing == 'right':
                self.change_sprite(self.player_res.jump_right)
            elif self.facing == 'left':
                self.change_sprite(self.player_res.jump_left)
            else:
                raise Exception
        elif self.status == 'walking':
            if self.facing == 'right':
                self.change_sprite(self.player_res.walk_right_anim)
            elif self.facing == 'left':
                self.change_sprite(self.player_res.walk_left_anim)
            else:
                raise Exception
        else:
            raise Exception

    @property
    def is_idle(self) -> bool:
        return self.status == 'idle'

    @property
    def is_walking(self) -> bool:
        return self.status == 'walking'

    @property
    def is_jumping(self) -> bool:
        return self.status == 'jumping'

    def face(self, direction: str):
        if direction == 'right':
            self.facing = 'right'
            self.update_sprite()
        elif direction == 'left':
            self.facing = 'left'
            self.update_sprite()
        else:
            raise Exception

    def start_walking(self, direction: str):
        if direction == 'right':
            self.vx = self.BASE_WALKING_SPEED
            self.facing = 'right'
            self.status = 'walking'
            self.update_sprite()
        elif direction == 'left':
            self.vx = -self.BASE_WALKING_SPEED
            self.facing = 'left'
            self.status = 'walking'
            self.update_sprite()
        else:
            raise Exception
    
    def stop_walking(self):
        self.status = 'idle'
        self.vx = 0
        self.update_sprite()

    def start_jumping(self):
        self.status = 'jumping'
        self.vy = self.BASE_JUMPING_SPEED
        self.update_sprite()
    
    def stop_jumping(self):
        self.status = 'idle'
        self.vy = 0
        self.update_sprite()

    def draw(self):
        if self.debug:
            self.ref_point.draw()
            self.ref_rect.draw()
        self.sprite.draw()


    @property
    def x_left(self) -> int:
        return self.x

    @property
    def x_right(self) -> int:
        return self.x + self.width

    @property
    def y_bottom(self) -> int:
        return self.y

    @property
    def y_top(self) -> int:
        return self.y + self.height

    def overlaping_with(self, sprite: Sprite) -> (str, str):
        def left_edge(sprite: Sprite) -> int:
            return sprite.x
        
        def right_edge(sprite: Sprite) -> int:
            return sprite.x + sprite.width

        def bottom_edge(sprite: Sprite) -> int:
            return sprite.y

        def top_edge(sprite: Sprite) -> int:
            return sprite.y + sprite.height

        def inside_width(x: int, sprite: Sprite) -> bool:
            return x > sprite.x and x < sprite.x + sprite.width

        def inside_height(y: int, sprite: Sprite) -> bool:
            return y > sprite.y and y < sprite.y + sprite.height

        def horizontal_overlap(sprite: Sprite) -> (str, int):
            if inside_width(x=self.x_right, sprite=sprite):
                return 'right', self.x_right - left_edge(sprite)
            elif inside_width(x=self.x_left, sprite=sprite):
                return 'left', right_edge(sprite) - self.x_left
            else:
                return None, None

        def vertical_overlap(sprite: Sprite) -> (str, int):
            if inside_height(y=self.y_top, sprite=sprite):
                return 'top', self.y_top - bottom_edge(sprite)
            elif inside_height(y=self.y_bottom, sprite=sprite):
                return 'bottom', top_edge(sprite) - self.y_bottom
            else:
                return None, None

        return horizontal_overlap(sprite), vertical_overlap(sprite)

# Create and open a window
window = Window(width=500, height=500, caption='Walk Animation Test')
fps_display = FPSDisplay(window)

# Create Ground
dirt_img = TileImages.dirtRight
dirt_tile_w, dirt_tile_h = dirt_img.width, dirt_img.height
ground_batch = Batch()
ground_list = []
n_ground = int(window.width / dirt_tile_w)
for i in range(n_ground):
    ground_list.append(Sprite(img=dirt_img, x=i*dirt_tile_w, y=0, batch=ground_batch))
ground_list.append(Sprite(img=dirt_img, x=2*dirt_tile_w, y=dirt_tile_h, batch=ground_batch))

# Create Player
player = Player(x=4.5*dirt_tile_w, y=2*dirt_tile_h, debug=True)

@window.event
def on_draw():
    window.clear()
    ground_batch.draw()
    player.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global player
    if symbol == key.LEFT:
        if not player.is_jumping:
            player.start_walking(direction='left')
        else:
            player.face(direction='left')
    elif symbol == key.RIGHT:
        if not player.is_jumping:
            player.start_walking(direction='right')
        else:
            player.face(direction='right')
    elif symbol == key.N:
        player.toggle_player()
    elif symbol == key.SPACE:
        if not player.is_jumping:
            player.start_jumping()

@window.event
def on_key_release(symbol, modifiers):
    global player
    if symbol == key.LEFT:
        if player.is_walking:
            player.stop_walking()
    elif symbol == key.RIGHT:
        if player.is_walking:
            player.stop_walking()

def move_player(dx: float, dy: float):
    global player, ground_list
    old_x, old_y = player.x, player.y
    player.x += dx
    player.y += dy

    collision = False
    for i, ground in enumerate(ground_list):
        (horizontal_overlap, x_overlap), (vertical_overlap, y_overlap) = player.overlaping_with(ground)
        
        if not vertical_overlap:
            pass
        elif vertical_overlap == 'bottom' and horizontal_overlap and x_overlap <= y_overlap:
            print(f"vertical_overlap == 'bottom'")
            player.y = ground.y + ground.height
            # player.y = old_y
            player.vy = 0
            if player.is_jumping:
                player.stop_jumping()
        elif vertical_overlap == 'top' and horizontal_overlap and x_overlap <= y_overlap:
            print(f"vertical_overlap == 'top'")
            player.y = ground.y - player.height
            # player.y = old_y
            player.vy = 0

        if not horizontal_overlap:
            pass
        elif horizontal_overlap == 'right' and vertical_overlap and x_overlap > y_overlap:
            print(f"horizontal_overlap == 'right'")
            player.x = ground.x - player.width//2
            # player.x = old_x
            player.vx = 0
        elif horizontal_overlap == 'left' and vertical_overlap and x_overlap > y_overlap:
            print(f"horizontal_overlap == 'left'")
            player.x = ground.x + ground.width//2
            # player.x = old_x
            player.vx = 0
        
        if horizontal_overlap and vertical_overlap:
            break

def update(dt):
    global player

    dx = player.vx * dt
    dy = player.vy * dt
    player.vy -= 1*9.81*dt*60
    move_player(dx=dx, dy=dy)
    
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()