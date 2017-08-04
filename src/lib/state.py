import enum

class Direction(enum.Enum):
    up_down = 1
    left_right = 2


class StatePart(enum.Enum):
    keyboard = 1
    image = 2
    lock = 3

