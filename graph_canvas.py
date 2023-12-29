from ubercanvas import UberCanvas


class GraphCanvas(UberCanvas):
    def __init__(self, root, ):
        UberCanvas.__init__(self, root)
        self.draw_circle(0, 0, 20, "red")

    def draw_circle(self, x, y, size, colour, tags=None):
        mod = size * self.zoom
        return self.canvas.create_oval(
            x - mod, y - mod,
            x + mod, y + mod,
            fill=colour,
            tags=tags
        )