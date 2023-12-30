import tkinter as tk

from helpers import consec_func


class UberCanvas:
    def __init__(self, root, canvas_radius=50):
        self.root = root
        self.canvas_radius = canvas_radius

        self.min_zoom = 1
        self.max_zoom = 300
        self.zoom = self.min_zoom
        self.zoom_delta = 0.2
        self.scroll_delta = 2

        # Canvas Frame.
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=0)
        # Canvas.
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.bind = self.canvas.bind


        # Scroll bars.
        self.hor_scrollbar = tk.Scrollbar(
            self.canvas_frame,
            orient="horizontal",
            command=self.canvas.xview,
        )
        self.vert_scrollbar = tk.Scrollbar(
            self.canvas_frame,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.canvas.configure(
            yscrollcommand=self.vert_scrollbar.set,
            xscrollcommand=self.hor_scrollbar.set,
        )
        # One metre gridlines.
        for i in range(-self.canvas_radius, self.canvas_radius + 1):
            # Vertical line.
            self.canvas.create_line(
                i, -self.canvas_radius,
                i, self.canvas_radius,
                fill="grey",
                width=0.1,
            )
            # Horizontal line.
            self.canvas.create_line(
                -self.canvas_radius, i,
                self.canvas_radius, i,
                fill="grey",
                width=0.1,
            )
        # Pack canvas and scrollbars.
        self.hor_scrollbar.grid(row=1, column=0, sticky="ew")
        self.vert_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.update_scroll_region()
        self.update_canvas_size()

        # Zoom in so the start dominates the screen. TODO: maths it.
        self.change_zoom(self.max_zoom / (self.min_zoom * 4))

    def update_scroll_region(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_canvas_size(self, *_):
        w_width = self.root.winfo_width()
        w_height = self.root.winfo_height()
        self.canvas.config(
            width=int(w_width * 0.8) - 50,
            height=w_height - 50,
        )

    def change_zoom(self, factor, event=None):
        if self.min_zoom < (new_zoom := self.zoom * factor) < self.max_zoom:
            self.zoom = new_zoom
            if event is not None:
                true_x = self.canvas.canvasx(event.x)
                true_y = self.canvas.canvasy(event.y)
            else:
                true_x = self.canvas.canvasx(self.canvas.winfo_width() / 2) #TODO: make this werk right.
                true_y = self.canvas.canvasy(self.canvas.winfo_height() / 2)
            self.canvas.scale("all", true_x, true_y, factor, factor)
            self.update_scroll_region()

    def set_zoom(self, new_zoom):
        self.change_zoom(new_zoom / self.zoom)

    # Functions that want to be bound.

    def reset_zoom(self, _):
        self.set_zoom(2) # TODO

    def zoom_in(self, event):
        self.change_zoom(1 + self.zoom_delta, event)

    def zoom_out(self, event):
        self.change_zoom(1 - self.zoom_delta, event)

    def scroll_up(self, _):
        self.canvas.yview_scroll(-self.scroll_delta, "units")
    
    def scroll_down(self, _):
        self.canvas.yview_scroll(self.scroll_delta, "units")

    def scroll_right(self, _):
        self.canvas.xview_scroll(self.scroll_delta, "units")
    
    def scroll_left(self, _):
        self.canvas.xview_scroll(-self.scroll_delta, "units")

    scroll_upleft = consec_func(scroll_up, scroll_left)
    scroll_upright = consec_func(scroll_up, scroll_right)
    scroll_downleft = consec_func(scroll_down, scroll_left)
    scroll_downright = consec_func(scroll_down, scroll_right)

    def start_canvas_drag(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def canvas_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

