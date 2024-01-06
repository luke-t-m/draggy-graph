
SMALL_NUM = 0.0000000001


def consec_func(func1, func2):
    def func3(*args):
        func1(*args)
        func2(*args)
    return func3


def get_canvas_xy(canvas, event):
    return canvas.canvasx(event.x), canvas.canvasy(event.y)


def close_enough(a, b):
    return abs(a - b) <= SMALL_NUM
