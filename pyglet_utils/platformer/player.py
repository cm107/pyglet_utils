from typing import List, cast

from .resources import PlayerImages
from .frame import Frame
from .grid import Grid, GridObject
from ..lib.exception_handler import Error
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
    def __init__(self, x: int, y: int, frame: Frame, grid: Grid, name: str='Player1', batch: Batch=None, debug: bool=False):
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

        # Grid Related
        self.grid = grid
        self.grid.add_obj(obj=self, name=name, is_anchor_x_centered=True)
        self.up_contact_obj_list = cast(List[GridObject], [])
        self.down_contact_obj_list = cast(List[GridObject], [])
        self.left_contact_obj_list = cast(List[GridObject], [])
        self.right_contact_obj_list = cast(List[GridObject], [])

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
        self.grid.show_contacts = not self.grid.show_contacts

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

    def start_falling(self):
        self.status = 'jumping'
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
        return self.x - self.width//2

    @x_left.setter
    def x_left(self, x_left: int):
        self.x = x_left - self.width//2

    @property
    def x_right(self) -> int:
        return self.x + self.width//2

    @x_right.setter
    def x_right(self, x_right: int):
        self.x = x_right - self.width//2

    @property
    def y_bottom(self) -> int:
        return self.y

    @y_bottom.setter
    def y_bottom(self, y_bottom: int):
        self.y = y_bottom

    @property
    def y_top(self) -> int:
        return self.y + self.height

    @y_top.setter
    def y_top(self, y_top: int):
        self.y = y_top - self.height

    def move(self, dx: int, dy: int):
        player_grid_obj = self.grid.contained_obj_list.get_obj_from_name(self.name)
        other_grid_objects = self.grid.contained_obj_list.get_objects(exclude_names=[self.name])
        self.up_contact_obj_list = []
        self.down_contact_obj_list = []
        self.left_contact_obj_list = []
        self.right_contact_obj_list = []
        self.grid.reset_contacts()

        # Move X
        proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dx=dx)
        collision = False
        for proposed_player_occupied_space in proposed_player_occupied_spaces:
            for other_grid_object in other_grid_objects:
                if proposed_player_occupied_space in other_grid_object.occupied_spaces:
                    other_grid_object.is_in_contact = True
                    if dx > 0:
                        self.right_contact_obj_list.append(other_grid_object)
                    elif dx < 0:
                        self.left_contact_obj_list.append(other_grid_object)
                    else:
                        raise Error(f'Player got stuck in object in x direction.')
                    collision = True
        if not collision:
            self.set_x(x=self.x+dx, fix_camera=True)
            self.frame.move_camera(dx=-dx, exclude_names=[self.name])
            self.grid.move(dx=-dx)
        else:
            if len(self.left_contact_obj_list) > 0:
                dx_adjustment = self.left_contact_obj_list[0].x_right + 1 - self.x_left
                self.set_x(x=self.x+dx_adjustment, fix_camera=True)
                self.frame.move_camera(dx=-dx_adjustment, exclude_names=[self.name])
                self.grid.move(dx=-dx_adjustment)
            elif len(self.right_contact_obj_list) > 0:
                dx_adjustment = self.right_contact_obj_list[0].x_left - self.x_right
                self.set_x(x=self.x+dx_adjustment, fix_camera=True)
                self.frame.move_camera(dx=-dx_adjustment, exclude_names=[self.name])
                self.grid.move(dx=-dx_adjustment)
            else:
                raise Exception

        # Move Y
        proposed_player_occupied_spaces = player_grid_obj.get_occupied_spaces(dy=dy)
        collision = False
        for proposed_player_occupied_space in proposed_player_occupied_spaces:
            for other_grid_object in other_grid_objects:
                if proposed_player_occupied_space in other_grid_object.occupied_spaces:
                    other_grid_object.is_in_contact = True
                    if dy > 0:
                        self.up_contact_obj_list.append(other_grid_object)
                    elif dy < 0:
                        self.down_contact_obj_list.append(other_grid_object)
                    else:
                        raise Error(f'Player got stuck in object in y direction.')
                    collision = True
        if not collision:
            self.set_y(y=self.y+dy, fix_camera=True)
            self.frame.move_camera(dy=-dy, exclude_names=[self.name])
            self.grid.move(dy=-dy)
            self.start_falling()
        else:
            self.vy = 0
            if len(self.down_contact_obj_list) > 0:
                dy_adjustment = self.down_contact_obj_list[0].y_top - self.y_bottom
                self.set_y(y=self.y+dy_adjustment, fix_camera=True)
                self.frame.move_camera(dy=-dy_adjustment, exclude_names=[self.name])
                self.grid.move(dy=-dy_adjustment)

                if self.is_jumping:
                    self.stop_jumping()
                    if self.arrow_key_buffer.is_pressed:
                        self.start_walking(direction=self.arrow_key_buffer.buffer[-1])
                    else:
                        self.vx = 0
            elif len(self.up_contact_obj_list) > 0:
                dy_adjustment = self.up_contact_obj_list[0].y_bottom - self.y_top
                self.set_y(y=self.y+dy_adjustment, fix_camera=True)
                self.frame.move_camera(dy=-dy_adjustment, exclude_names=[self.name])
                self.grid.move(dy=-dy_adjustment)
            else:
                raise Exception