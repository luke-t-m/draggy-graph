import tkinter as tk
from tkinter import messagebox
import signal

from ubercanvas import UberCanvas


class DraggyGraphApp():
    def __init__(self, app_name):
        self.app_name = app_name

        self.exit_msg = f"You have unsaved work!\nPlease confirm you wish to exit {self.app_name}."
        self.do_exit_msg = False

        # Window.
        self.root = tk.Tk()
        self.root.title(self.app_name)
        self.root.geometry("600x400+100+100")
        self.root.minsize(300, 200)

        self.ubercanvas = UberCanvas(self.root)

        self.make_bindings()

        # Check signals so app isn't left a zombie after kill in terminal.
        signal.signal(signal.SIGINT, self.destroy_app)
        self.loop_for_signals()
        self.root.protocol("WM_DELETE_WINDOW", self.do_close)

        self.root.mainloop()

    # Calls itself forever. Causes context switch so signal handling works.
    def loop_for_signals(self):
        self.root.after(100, self.loop_for_signals)

    def destroy_app(self, *_):
        print("\nGoodbye!")
        self.root.destroy()

    def do_close(self):
        if self.do_exit_msg and not messagebox.askokcancel(
            f"Exit {self.app_name}",
            self.exit_msg,
        ):
            return
        self.destroy_app()

    def make_bindings(self):
        # Zoom bindings.
        self.root.bind("<Configure>", self.ubercanvas.update_canvas_size)
        self.root.bind("<Control-0>", self.ubercanvas.reset_zoom)  # TODO
        self.ubercanvas.bind("<Control-Button-4>", self.ubercanvas.zoom_in)
        self.ubercanvas.bind("<Control-Button-5>", self.ubercanvas.zoom_out)

        # Drag canvas bindings.
        #self.ubercanvas.bind("<Button-2>", self.ubercanvas.start_canvas_drag)
        self.ubercanvas.bind("<B2-Motion>", self.ubercanvas.canvas_drag)
        self.ubercanvas.bind("<ButtonRelease-2>", self.ubercanvas.stop_canvas_drag)

        # Scroll canvas bindings.
        # TODO: only make these work if mouse is over canvas.
        self.ubercanvas.bind("<Button-4>", self.ubercanvas.scroll_up)
        self.ubercanvas.bind("<Button-5>", self.ubercanvas.scroll_down)
        self.ubercanvas.bind("<Shift-Button-4>", self.ubercanvas.scroll_left)
        self.ubercanvas.bind("<Shift-Button-5>", self.ubercanvas.scroll_right)


if __name__ == "__main__":
    DraggyGraphApp('the "its over" department')