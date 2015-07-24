import math


def center_text_x(label, width):
    area = label.get_rect()
    remainder = width - area.width
    return math.floor(remainder / 2.0)


def center_text_y(label, height):
    area = label.get_rect()
    remainder = height - area.height
    return math.floor(remainder / 2.0)
