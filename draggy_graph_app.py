import tkinter as tk
from tkinter import messagebox
import signal
from collections import defaultdict

from graph_canvas import GraphCanvas


class KeyBind:
    def __init__(self, keys, func_name):
        self.keys = keys
        self.func_name = func_name

class FunctionWithType:
    def __init__(self, type, func):
        self.type = type
        self.func = func

class DraggyGraphApp:
    def __init__(self, app_name):
        self.app_name = app_name

        self.exit_msg = (
            f"You have unsaved work!\nPlease confirm you wish to close {self.app_name}."
        )
        self.do_exit_msg = False

        self.key_states = defaultdict(lambda: False)
        self.keybinds = defaultdict(lambda: [])

        # Window.
        self.root = tk.Tk()
        self.root.title(self.app_name)
        self.root.geometry("600x400+100+100")
        self.root.minsize(300, 200)

        self.canvas = GraphCanvas(self.root)

        self.canvas.draw_circle(0, 0, 1, "yellow")

        self.functions_map = {
            "Scroll up": FunctionWithType("scroll", self.canvas.scroll_up),
            "Scroll down": FunctionWithType("scroll", self.canvas.scroll_down),
            "Scroll left": FunctionWithType("scroll", self.canvas.scroll_left),
            "Scroll right": FunctionWithType("scroll", self.canvas.scroll_right),
            "Scroll up+left": FunctionWithType("scroll", self.canvas.scroll_upleft),
            "Scroll up+right": FunctionWithType("scroll", self.canvas.scroll_upright),
            "Scroll down+left": FunctionWithType("scroll", self.canvas.scroll_downleft),
            "Scroll down+right": FunctionWithType("scroll", self.canvas.scroll_downright),
            "Zoom in": FunctionWithType("zoom", lambda _: self.canvas.zoom_in(None)),
            "Zoom out": FunctionWithType("zoom", lambda _: self.canvas.zoom_out(None)),
            "Reset zoom": FunctionWithType("zoom", self.canvas.reset_zoom),
            "Select move tool": FunctionWithType("tool", lambda _: self.canvas.set_tool("move")),
            "Select place tool": FunctionWithType("tool", lambda _: self.canvas.set_tool("place")),
            "Select drag tool": FunctionWithType("tool", lambda _: self.canvas.set_tool("drag")),
        }

        self.make_fixed_bindings()
        self.make_keybinds("filename")

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
            f"Exit {self.app_name}", self.exit_msg
        ):
            return
        self.destroy_app()

    def key_pressed(self, event):
        pressed = event.keysym
        self.key_states[pressed] = True

        keybinds = self.keybinds[pressed]
        for keybind in keybinds:
            if all(self.key_states[key] for key in keybind.keys):
                to_exec = self.functions_map[keybind.func_name].func
                to_exec(event)
                return

    def key_released(self, event):
        pressed = event.keysym
        self.key_states[pressed] = False

    def make_keybinds(self, filename):
        keybinds = [
            KeyBind(["Up"], "Scroll up"),
            KeyBind(["Down"], "Scroll down"),
            KeyBind(["Left"], "Scroll left"),
            KeyBind(["Right"], "Scroll right"),
            KeyBind(["Up", "Left"], "Scroll up+left"),
            KeyBind(["Up", "Right"], "Scroll up+right"),
            KeyBind(["Down", "Left"], "Scroll down+left"),
            KeyBind(["Down", "Right"], "Scroll down+right"),
            KeyBind(["Control_L", "0"], "Reset zoom"),
            KeyBind(["Control_L", "equal"], "Zoom in"),
            KeyBind(["Control_L", "minus"], "Zoom out"),
            KeyBind(["1"], "Select move tool"),
            KeyBind(["2"], "Select place tool"),
            KeyBind(["3"], "Select drag tool")
        ]

        for keybind in keybinds:
            for key in keybind.keys:
                self.keybinds[key].append(keybind)

        for keybinds in self.keybinds.values():
            keybinds.sort(key=lambda kb: len(kb.keys), reverse=True)

    def make_fixed_bindings(self):
        self.root.bind("<Key>", self.key_pressed)
        self.root.bind("<KeyRelease>", self.key_released)

        # Zoom bindings.
        self.root.bind("<Configure>", self.canvas.update_canvas_size)
        self.canvas.bind("<Control-Button-4>", self.canvas.zoom_in)
        self.canvas.bind("<Control-Button-5>", self.canvas.zoom_out)

        # Drag canvas bindings.
        self.canvas.bind("<Button-2>", self.canvas.start_canvas_drag)
        self.canvas.bind("<B2-Motion>", self.canvas.canvas_drag)

        # Scroll canvas bindings.
        # TODO: only make these work if mouse is over canvas.
        self.canvas.bind("<Button-4>", self.canvas.scroll_up)
        self.canvas.bind("<Button-5>", self.canvas.scroll_down)
        self.canvas.bind("<Shift-Button-4>", self.canvas.scroll_left)
        self.canvas.bind("<Shift-Button-5>", self.canvas.scroll_right)

        # Graph canvas mouse "handler" function bindings.
        self.canvas.bind("<Button-1>", self.canvas.handle_mouse1)
        self.canvas.bind("<B1-Motion>", self.canvas.handle_drag)
        self.canvas.bind("<Motion>", self.canvas.handle_motion)

if __name__ == "__main__":
    DraggyGraphApp('the "its over" department')
