from ubercanvas import UberCanvas
from helpers import get_canvas_xy, SMALL_NUM


class GraphCanvas(UberCanvas):
    def __init__(self, root, ):
        UberCanvas.__init__(self, root)

        self.tool = "move"
        self.holding = None

        self.node_radius = 0.25

    def set_tool(self, tool):
        self.tool = tool

    def draw_circle(self, x, y, size, colour, tags=None):
        mod = size * self.zoom
        return self.canvas.create_oval(
            x - mod, y - mod,
            x + mod, y + mod,
            fill=colour,
            tags=tags
        )
    
    def move_circle(self, id, x, y):
        current_coords = self.canvas.coords(id)
        radius = (current_coords[2] - current_coords[0]) / 2
        self.canvas.coords(id, x - radius, y - radius, x + radius, y + radius)

    def place_node(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.draw_circle(x, y, self.node_radius, "red", tags=("node", "draggable"))

    def make_vertice(self, id1, id2):
        a = self.canvas.coords(id1)
        # TODO: get coords of 1 and 2. draw line. tag with ids of 1 and 2.
        # whenever node is moved, change coords of anything tagged with those ids.

    def find_at_xy(self, x, y, tag):
        under_mouse = self.canvas.find_overlapping(x - SMALL_NUM, y - SMALL_NUM, x + SMALL_NUM, y + SMALL_NUM)
        for id in under_mouse:
            if tag in self.canvas.gettags(id):
                return id
    
    
    # Functions that yearn to be bound.
    
    def handle_mouse1(self, event):
        cx, cy = get_canvas_xy(self.canvas, event)
        match self.tool:
            case "move":
                self.start_canvas_drag(event)
            case "place":
                self.place_node(event)
            case "drag":
                self.holding = self.find_at_xy(cx, cy, "draggable")
            case "connect":
                self.holding = self.find_at_xy(cx, cy, "node")

    def handle_mouse1_release(self, event):
        return


    def handle_motion(self, event):
        match self.tool:
            case "move":
                pass
            case "place":
                pass
            case "drag":
                pass
            case "connect":
                pass

    def handle_drag(self, event):
        cx, cy = get_canvas_xy(self.canvas, event)
        match self.tool:
            case "move":
                self.canvas_drag(event)
            case "place":
                pass
            case "drag":
                if self.holding != None:
                    self.move_circle(self.holding, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
            case "connect":
                pass



