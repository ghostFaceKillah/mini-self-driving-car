import enum
import multiprocessing


class Vertical(enum.Enum):
    up = 1
    down = 2
    nothing = 3


class Horizontal(enum.Enum):
    left = 1
    right = 2
    nothing = 3


class TheState():
    def __init__(self):
        self.img = None
        self.horizontal = Horizontal.nothing
        self.vertical = Vertical.nothing

        self.img_lock = multiprocessing.Lock()
        self.keyboard_lock = multiprocessing.Lock()

    def set_image(self, img):
        with self.img_lock:
            self.img = img.copy()

    def get_image(self):
        with self.img_lock:
            if self.img is not None:
                return self.img.copy()

    def get_steering(self):
        with self.keyboard_lock:
            return self.horizontal, self.vertical

    def set_vertical(self, val):
        with self.keyboard_lock:
            self.vertical = val

    def set_horizontal(self, val):
        with self.keyboard_lock:
            self.horizontal = val



