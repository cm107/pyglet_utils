from typing import List

from .resources import PlayerImages
from .frame import Frame
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.shapes import Circle, Rectangle

from common_utils.check_utils import check_value

class ArrowKeyBuffer:
    def __init__(self, buffer: List[str]=None):
        self.buffer = buffer if buffer is not None else []
        self._valid_directions = ['left', 'right']
    
    def press(self, direction: str):
        check_value(direction, valid_value_list=self._valid_directions)
        self.buffer.append(direction)
    
    def release(self, direction: str):
        check_value(direction, valid_value_list=self._valid_directions)
        while direction in self.buffer:
            idx = self.buffer.index(direction)
            del self.buffer[idx]
    
    @property
    def is_pressed(self) -> bool:
        return len(self.buffer) > 0

    @property
    def is_released(self) -> bool:
        return len(self.buffer) == 0

class Player:
    def __init__(self, x: int, y: int, frame: Frame, name: str='Player1', batch: Batch=None, debug: bool=False):
        self.name = name
        self._x, self._y = x, y
        self._camera_x, self._camera_y = x - frame.x, y - frame.y

        # Player Sprite Select Related
        self.player_res_list = [PlayerImages.p1, PlayerImages.p2, PlayerImages.p3]
        self.player_select = 0
        self.player_res = self.player_res_list[self.player_select]
        self.sprite = Sprite(img=self.player_res.jump_right, x=self._camera_x, y=self._camera_y, batch=batch)

        # Movement Related
        self.BASE_WALKING_SPEED = 200
        self.BASE_JUMPING_SPEED = 300
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 'right'
        self.status = 'jumping'
        self.arrow_key_buffer = ArrowKeyBuffer()

        # Frame Related
        self.frame = frame
        self.frame.add_obj(obj=self, name=name, is_anchor_x_centered=True)

        # Debug
        self.debug = debug
        self.ref_point = Circle(x=self.camera_x, y=self.camera_y, radius=5, color=(255,0,0))
        self.ref_rect = Rectangle(x=self.camera_x, y=self.camera_y, width=self.width, height=self.height, color=(0,0,255))
        self.ref_rect.anchor_x = self.ref_rect.width // 2

    @property
    def camera_x(self) -> int:
        return self._camera_x
    
    @camera_x.setter
    def camera_x(self, camera_x: int):
        self._camera_x = camera_x
        self.sprite.x = self._camera_x
        if self.debug:
            self.ref_point.x = self._camera_x
            self.ref_rect.x = self._camera_x

    @property
    def camera_y(self) -> int:
        return self._camera_y
    
    @camera_y.setter
    def camera_y(self, camera_y: int):
        self._camera_y = camera_y
        self.sprite.y = self._camera_y
        if self.debug:
            self.ref_point.y = self._camera_y
            self.ref_rect.y = self._camera_y

    def set_x(self, x: int, fix_camera: bool=False):
        if fix_camera:
            dx = x - self._x
            self.frame.x = self.frame.x + dx
        else:
            self._camera_x = x - self.frame.x
        self._x = x

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
       self.set_x(x=x, fix_camera=False)

    def set_y(self, y: int, fix_camera: bool=False):
        if fix_camera:
            dy = y - self._y
            self.frame.y = self.frame.y + dy
        else:
            self._camera_y = y - self.frame.y
        self._y = y

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, y: int):
        self.set_y(y=y, fix_camera=False)

    @property
    def width(self) -> int:
        return self.sprite.width
    
    @property
    def height(self) -> int:
        return self.sprite.height

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)

    def change_player(self, idx: int):
        self.player_res = self.player_res_list[idx]
        self.player_select = idx
        self.update_sprite()

    def toggle_player(self):
        self.change_player((self.player_select+1) % len(self.player_res_list))

    def toggle_debug(self):
        self.debug = not self.debug

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