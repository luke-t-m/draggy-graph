from ubercanvas import UberCanvas
from helpers import get_canvas_xy, SMALL_NUM


class GraphCanvas(UberCanvas):
    def __init__(self, root, ):
        UberCanvas.__init__(self, root)

        self.tool = "move"
        self.holding = None

        self.node_radius = 1

    def set_tool(self, tool):
        self.tool = tool

    def draw_circle(self, x, y, size, colour, tags=None):
        mod = size * self.zoom

        id = self.canvas.create_oval(
            x - mod, y - mod,
            x + mod, y + mod,
            fill=colour,
            tags=tags
        )

        tags = [f"dep_{id}", "label"]
        self.canvas.create_text(x, y, text="sneed", tags=tags)
    
    def move_circle(self, id, x, y):
        current_coords = self.canvas.coords(id)
        radius = (current_coords[2] - current_coords[0]) / 2
        self.canvas.coords(id, x - radius, y - radius, x + radius, y + radius)

        # find all vertices with tags, and redraw them. also text.

        node_x = (current_coords[0] + current_coords[2]) / 2
        node_y = (current_coords[1] + current_coords[3]) / 2

        to_redraw = self.canvas.find_withtag(f"dep_{id}&&vertice")
        for vert_id in to_redraw:
            cur = self.canvas.coords(vert_id)
            if cur[0] == node_x and cur[1] == node_y:
                cur[0] = x
                cur[1] = y
            else:
                cur[2] = x
                cur[3] = y
            
            self.canvas.coords(vert_id, *cur)

        to_redraw = self.canvas.find_withtag(f"dep_{id}&&label")
        print(to_redraw)
        for text_id in to_redraw:
            self.canvas.coords(text_id, x, y)

    def place_node(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.draw_circle(x, y, self.node_radius, "red", tags=("node", "draggable"))
        self.canvas.create_oval()

    def create_vertice(self, node1_id, node2_id):
        node1_coords = self.canvas.coords(node1_id)
        node2_coords = self.canvas.coords(node2_id)
        node1_x = (node1_coords[0] + node1_coords[2]) / 2
        node1_y = (node1_coords[1] + node1_coords[3]) / 2
        node2_x = (node2_coords[0] + node2_coords[2]) / 2
        node2_y = (node2_coords[1] + node2_coords[3]) / 2

        tags = [f"dep_{node1_id}", f"dep_{node2_id}", "vertice"]

        self.canvas.create_line(node1_x, node1_y, node2_x, node2_y, tags=tags)

    def find_at_xy(self, x, y, tag):
        under_mouse = self.canvas.find_overlapping(x - SMALL_NUM, y - SMALL_NUM, x + SMALL_NUM, y + SMALL_NUM)
        for id in under_mouse:
            if tag in self.canvas.gettags(id):
                return id
    
    
    # Functions that yearn to be bound.
            
    # TODO: zooming breaks vertices.
    
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
                found = self.find_at_xy(cx, cy, "node")
                good = len(self.canvas.find_withtag(f"dep_{found}&&dep_{self.holding}")) == 0
                print(good)
                if self.holding is not None and found is not None and self.holding != found and good:
                    self.create_vertice(self.holding, found)

                self.holding = found

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



