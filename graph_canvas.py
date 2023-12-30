from ubercanvas import UberCanvas


class GraphCanvas(UberCanvas):
    def __init__(self, root, ):
        UberCanvas.__init__(self, root)

        self.tool = "move"
        self.dragging = None

        self.node_radius = 0.25

        self.node_ids = []
        self.line_ids = []

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
        node_id = self.draw_circle(x, y, self.node_radius, "red", tags=("node", "draggable"))
        self.node_ids.append(node_id)

    def find_draggable(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        mod = 0.01
        under_mouse = self.canvas.find_overlapping(x - mod, y - mod, x + mod, y + mod)
        for id in under_mouse:
            if "draggable" in self.canvas.gettags(id):
                return id
    
    
    # Functions that yearn to be bound.
    
    def handle_mouse1(self, event):
        match self.tool:
            case "move":
                self.start_canvas_drag(event)
            case "place":
                self.place_node(event)
            case "drag":
                self.dragging = self.find_draggable(event)


    def handle_motion(self, event):
        match self.tool:
            case "move":
                pass
            case "place":
                pass
            case "drag":
                pass

    def handle_drag(self, event):
        match self.tool:
            case "move":
                self.canvas_drag(event)
            case "place":
                pass
            case "drag":
                if self.dragging != None:
                    self.move_circle(self.dragging, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))


