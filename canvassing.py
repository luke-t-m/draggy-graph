import tkinter as tk
from tkinter import messagebox
import signal


# to-do:
# vagueify variable names in code, no "midpoint" shit!!!
# extract generic stuff to class in another file that gets extended.
# have node class- stores name and connections.
# find a way to give lines some kind of "tag" to associate them with their node
# on drag, just delete and redraw associated lines.
# add a settings file that stores settings. Rebinding, prompts, etc.


class CanvasApp:
    def __init__(self, app_name, canvas_radius):
        self.app_name = app_name
        self.canvas_radius = canvas_radius

        self.exit_msg = f"You have unsaved work!\nPlease confirm you wish to exit {self.app_name}."
        self.do_exit_msg = False

        self.min_zoom = 1
        self.max_zoom = 300
        self.zoom = self.min_zoom
        self.zoom_delta = 0.2
        self.scroll_delta = 2

        # Window.
        self.root = tk.Tk()
        self.root.title(self.app_name)
        self.root.geometry("600x400+100+100")
        self.root.minsize(300, 200)

        # Canvas Frame.
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=0)
        # Canvas.
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
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
                i,
                -self.canvas_radius,
                i,
                self.canvas_radius,
                fill="grey",
                width=0.1,
            )
            # Horizontal line.
            self.canvas.create_line(
                -self.canvas_radius,
                i,
                self.canvas_radius,
                i,
                fill="grey",
                width=0.1,
            )
        # Pack canvas and scrollbars.
        self.hor_scrollbar.grid(row=1, column=0, sticky="ew")
        self.vert_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.update_scroll_region()
        self.update_canvas_size()

        # Zoom bindings.
        self.root.bind("<Configure>", lambda _: self.update_canvas_size())
        self.root.bind("<Control-0>", lambda _: self.set_zoom(2))  # TODO
        self.canvas.bind(
            "<Control-Button-4>",
            lambda e: self.change_zoom(1 + self.zoom_delta, e)
        )
        self.canvas.bind(
            "<Control-Button-5>",
            lambda e: self.change_zoom(1 - self.zoom_delta, e)
        )

        # Drag canvas bindings.
        self.canvas.bind("<Button-2>", self.start_canvas_drag)
        self.canvas.bind("<B2-Motion>", self.canvas_drag)

        # Scroll canvas bindings.
        self.canvas.bind(
            "<Button-4>",
            lambda _: self.canvas.yview_scroll(-self.scroll_delta, "units")
        )
        self.canvas.bind(
            "<Button-5>",
            lambda _: self.canvas.yview_scroll(self.scroll_delta, "units")
        )
        self.canvas.bind(
            "<Shift-Button-4>",
            lambda _: self.canvas.xview_scroll(self.scroll_delta, "units")
        )
        self.canvas.bind(
            "<Shift-Button-5>",
            lambda _: self.canvas.xview_scroll(-self.scroll_delta, "units")
        )

        # Zoom in so the start dominates the screen. TODO: maths it.
        self.change_zoom(self.max_zoom / (self.min_zoom * 4))

        # Check signals so app isn't left a zombie after kill in terminal.
        signal.signal(signal.SIGINT, self.destroy_app)
        self.loop_for_signals()
        self.root.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        self.root.mainloop()

    # Calls itself forever. Causes context switch so signal handling works.
    def loop_for_signals(self):
        self.root.after(100, self.loop_for_signals)

    def destroy_app(self, *_):
        print("\nGoodbye!")
        self.root.destroy()

    def on_delete_window(self):
        if self.do_exit_msg and not messagebox.askokcancel(
            f"Exit {self.app_name}",
            self.exit_msg,
        ):
            return
        self.destroy_app()

    def update_scroll_region(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_canvas_size(self):
        w_width = self.root.winfo_width()
        w_height = self.root.winfo_height()
        self.canvas.config(
            width=int(w_width * 0.8) - 50,
            height=w_height - 50,
        )

    def set_zoom(self, new_zoom):
        self.change_zoom(new_zoom / self.zoom)

    def change_zoom(self, factor, event=None):
        if self.min_zoom < (new_zoom := self.zoom * factor) < self.max_zoom:
            self.zoom = new_zoom
            if event is not None:
                true_x = self.canvas.canvasx(event.x)
                true_y = self.canvas.canvasy(event.y)
            else:
                true_x = true_y = 0
            self.canvas.scale("all", true_x, true_y, factor, factor)
            self.update_scroll_region()

    def start_canvas_drag(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def canvas_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


if __name__ == "__main__":
    CanvasApp("Raw CanvasApp", 50)


"""

    def _handle_left_click(self, event):
        match self.tool:
            case Tools.DRAG_CANVAS:
                self.canvas.scan_mark(event.x, event.y)
            case Tools.PLACE_POINT:
                self.place_point(event)
            case Tools.DRAG_POINT:
                self.dragging = self.find_draggable(event)


    def _handle_motion(self, event):
        self.move_circle(self.cursor, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        match self.tool:
            case Tools.DRAG_CANVAS:
                pass
            case Tools.PLACE_POINT:
                self.move_circle(self.cursor, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
            case DRAG_POINT:
                pass

    def handle_drag(self, event):
        match self.tool:
            case Tools.DRAG_CANVAS:
                self.canvas.scan_dragto(event.x, event.y, gain=1)
            case Tools.PLACE_POINT:
                pass
            case Tools.DRAG_POINT:
                self.move_circle(self.dragging, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
                self.draw_midline()


                
                        # Bindings.
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        # Zoom in on mouse wheel.
        self.canvas.bind(
            "<Control-Button-4>",
            func=lambda event: self.change_zoom(1.2, event),
        )
        # Zoom out on mouse wheel.
        self.canvas.bind(
            "<Control-Button-5>",
            func=lambda event: self.change_zoom(0.8, event),
        )
        # Reset zoom.
        self.root.bind("Control-0", func=lambda _: self.set_zoom(2))

        # Zoom in so the start dominates the screen. TODO: maths it.
        self.change_zoom(self.max_zoom / (self.min_zoom * 4))

        # Check signals so app isn't left a zombie after kill in terminal.
        signal.signal(signal.SIGINT, self.destroy_app)
        # This may seem useless, but program won't catch signals
        # from mainloop alone. Something about context switching.
        self.loop_for_signals()
        self.root.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        self.cursor = self.draw_circle(0, 0, self.cone_radius / 5, "black")
        self.canvas.bind("<Motion>", self.handle_motion)



        def find_draggable(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        mod = 0.01
        objects_under_mouse = self.canvas.find_overlapping(x - mod, y - mod, x + mod, y + mod)
        for object_id in objects_under_mouse:
            print(object_id)
            print(self.canvas.gettags(object_id))
            if "draggable" in self.canvas.gettags(object_id):
                return object_id

    def place_point(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        midpoint = self.draw_circle(x, y, self.cone_radius, "red", tags=("point", "draggable"))
        self.midpoints.append(midpoint)
        self.draw_midline()

    def draw_circle(self, x, y, size, colour, tags=None):
        mod = size * self.zoom
        return self.canvas.create_oval(
            x - mod,
            y - mod,
            x + mod,
            y + mod,
            fill=colour,
            tags=tags
        )

    def move_circle(self, object, x, y):
        current_coords = self.canvas.coords(object)
        mod = (current_coords[2] - current_coords[0]) / 2
        self.canvas.coords(object, x - mod, y - mod, x + mod, y + mod)

    def set_tool(self, toolnum):
        self.tool = Tools(toolnum)
        print(f"set tool to {self.tool}")



"""
