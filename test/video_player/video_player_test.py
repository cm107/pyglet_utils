from typing import cast
import cv2
import numpy as np
from PIL import Image

import pyglet
from pyglet.window import Window, FPSDisplay, key
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.image import ImageData
from pyglet.gl import GLubyte

from pyglet_utils.lib.shapes import Rectangle
from pyglet_utils.lib.panel import Panel
from pyglet_utils.lib.basic import BasicObject

from streamer.streamer import Streamer

def cv2glet(img: np.ndarray) -> ImageData:
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if img is None:
        return None
    rows, cols, channels = img.shape
    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                height=rows, 
                                format='BGR', 
                                data=raw_img, 
                                pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg

class VideoFrame(BasicObject):
    def __init__(self, x: int, y: int, width: int, height: int, image_data: ImageData=None):
        super().__init__(x=x, y=y, width=width, height=height)
        self._image_data = image_data
    
    @property
    def image_data(self) -> ImageData:
        return self._image_data
    
    @property
    def orig_aspect_ratio(self) -> float:
        return self._image_data.width / self._image_data.height

    @image_data.setter
    def image_data(self, image_data: ImageData):
        if isinstance(image_data, ImageData):
            self._image_data = image_data
        elif isinstance(image_data, np.ndarray):
            self._image_data = cv2glet(image_data)
        elif isinstance(image_data, None):
            self._image_data = None
        else:
            raise TypeError(f"Cannot set VideoFrame.image_data to type {type(image_data)}")

    def draw(self):
        if self.image_data is not None:
            self.image_data.blit(x=self.x, y=self.y, width=self.width, height=self.height)

class VideoPanel(Panel):
    def __init__(self, relative_x: int, relative_y: int, width: int, height: int, streamer: Streamer, parent):
        super().__init__(
            relative_x=relative_x, relative_y=relative_y,
            width=width, height=height,
            parent=parent,
            bg_color=(0,0,0), bg_transparency=255
        )
        self.streamer = streamer
        if streamer.width / streamer.height >= width / height:
            target_width = width
            target_height = int(streamer.height * (target_width / streamer.width))
            bottom_offset = (height - target_height) // 2
            left_offset = 0
        else:
            target_height = height
            target_width = int(streamer.width * (target_height / streamer.height))
            left_offset = relative_x + (width - target_width) // 2
            bottom_offset = relative_y + 0
        self.frame = VideoFrame(x=left_offset, y=bottom_offset, width=target_width, height=target_height)
        # self.add_obj(self.frame, relative=True, scale_with_parent=True)

    def next_frame(self) -> np.ndarray:
        if self.streamer.get_num_frames_read() == self.streamer.get_frame_count():
            self.streamer.goto_frame(0)
        self.frame.image_data = self.streamer.get_frame()
        print(f'Progress: {self.streamer.get_progress_ratio_string()}')
        if self.frame is None:
            self.close()
    
    def draw(self):
        super().draw()
        self.frame.draw()

class BottomPanel(Panel):
    def __init__(self, relative_x: int, relative_y: int, width: int, height: int, parent):
        super().__init__(
            relative_x=relative_x, relative_y=relative_y,
            width=width, height=height,
            parent=parent,
            bg_color=(255,0,0), bg_transparency=255
        )

        # sample_text = Label(
        #     text='Sample Text',
        #     font_name='Times New Roman',
        #     font_size=20,
        #     x=int(0.5*self.width), y=int(0.5*self.height),
        #     color=tuple([0, 255, 255] + [255]),
        #     anchor_x='center', anchor_y='center', bold=True
        # )
        # self.add_obj(sample_text, relative=True, scale_with_parent=True)

class VideoPlayerWindow(Window):
    def __init__(
        self, width: int, height: int, src, caption: str, window_fps: int
    ):
        super().__init__(
            width=width, height=height, caption=caption,
            resizable=True
        )
        streamer = Streamer(src=src)

        self.bottom_panel = BottomPanel(
            relative_x=0, relative_y=0,
            width=self.width, height=int(self.height*0.1),
            parent=self
        )
        self.video_panel = VideoPanel(
            relative_x=0, relative_y=self.bottom_panel.height,
            width=self.width, height=self.height-self.bottom_panel.height,
            streamer=streamer,
            parent=self
        )

        self.fps_display = FPSDisplay(self)

        # Pause Related
        self.paused = False
        self.paused_text = Label(
            text='Paused',
            font_name='Times New Roman',
            font_size=30,
            x=int(0.50*self.width), y=int(0.98*self.height),
            color=tuple([255, 100, 100] + [255]),
            anchor_x='center', anchor_y='top', bold=True
        )

        # Clock Related
        self.window_fps = window_fps
        self._frame_fps = self.video_panel.streamer.get_fps()

    @property
    def x(self) -> int:
        return 0
    
    @property
    def y(self) -> int:
        return 0

    @property
    def frame_fps(self) -> int:
        return self._frame_fps

    def toggle_pause(self):
        self.paused = not self.paused

    def on_draw(self):
        self.clear()
        self.video_panel.draw()
        self.bottom_panel.draw()
        self.fps_display.draw()
        if self.paused:
            self.paused_text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.toggle_pause()
        elif symbol == key.ESCAPE:
            self.close()
        elif symbol == key.RIGHT:
            self.video_panel.streamer.fastforward(100)
            self.video_panel.next_frame()
        elif symbol == key.LEFT:
            self.video_panel.streamer.rewind(100)
            self.video_panel.next_frame()

    def on_key_release(self, symbol, modifiers):
        pass

    def on_resize(self, width: int, height: int):
        self._projection.set(width, height, *self.get_framebuffer_size())
        height_prop = self.video_panel._orig_height / (self.video_panel._orig_height + self.bottom_panel._orig_height)
        video_panel_height = int(height * height_prop)
        self.video_panel.shape = (width, video_panel_height)
        self.bottom_panel.shape = (width, height-video_panel_height)

        if self.video_panel.frame._image_data is not None:
            if self.video_panel.frame.orig_aspect_ratio >= width / height:
                target_width = width
                target_height = int(target_width / self.video_panel.frame.orig_aspect_ratio)
                self.video_panel.frame.shape = (target_width, target_height)
                target_x = 0
                target_y = 0.5*(height - self.bottom_panel.height - target_height)+self.bottom_panel.height
                self.video_panel.frame.position = (target_x, target_y)
            else:
                target_height = height
                target_width = int(target_height * self.video_panel.frame.orig_aspect_ratio)
                self.video_panel.frame.shape = (target_width, target_height)
                target_y = self.bottom_panel.height
                target_x = int(0.5*(width - target_width))
                self.video_panel.frame.position = (target_x, target_y)

    def update_frame(self, dt):
        if not self.paused:
            self.video_panel.next_frame()
        else:
            pass

    def update_window(self, dt):
        pass

    def run(self):
        pyglet.clock.schedule_interval(self.update_frame, 1/self.frame_fps)
        pyglet.clock.schedule_interval(self.update_window, 1/self.window_fps)
        pyglet.app.run()

# video_path = '/home/clayton/workspace/prj/data_keep/data/toyota/dataset/real/phone_videos/new/VID_20200217_161043.mp4'
video_path = '/home/clayton/workspace/prj/data_keep/data/toyota/dataset/real/camera_videos/camera1.mp4'
worker = VideoPlayerWindow(
    width=1200, height=800,
    src=video_path,
    caption='Video Player Test', window_fps=60
)
worker.run()