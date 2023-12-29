from ubercanvas import UberCanvas


class GraphCanvas(UberCanvas):
    def __init__(self, root, ):
        UberCanvas.__init__(self, root)

        self.tool = "move"

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
    
    def place_node(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        node_id = self.draw_circle(x, y, self.node_radius, "red", tags=("node", "draggable"))
        self.node_ids.append(node_id)
    
    # Functions that yearn to be bound.
    
    def handle_mouse1(self, event):
        match self.tool:
            case "move":
                self.start_canvas_drag(event)
            case "place":
                self.place_node(event)
            case "drag_node":
                return
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
                return
                self.move_circle(self.dragging, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
                self.draw_midline()


