# class LinkedList:
#     def __init__(self, data) -> None:
#         self.data = data
#         self.child = None

class Base:
    UNTOUCHED = "untouched"
    EMPTY = "empty"
    CONTROL_LOGIC = "control logic"

    IRON_MINE = "iron mine"
    COPPER_MINE = "copper mine"

    IRON_SMELTERY = "iron smeltery"
    COPPER_SMELTERY = "copper smeltery"

    def __init__(self, map, start_x, start_y) -> None:
        self.map = map

        assert isinstance(start_x, int)
        assert isinstance(start_y, int)
        self.pos = (start_x, start_y)

        self.nodes = {}

        self.build_node(*self.pos, self.CONTROL_LOGIC)

        self.open_node_positions = []
        self.queue_adjacent_node_positions(*self.pos)

    def get_node(self, x, y):
        pos = (x, y)

        if pos in self.nodes:
            return self.nodes[pos]
        else:
            return self.UNTOUCHED

    def build_node(self, x, y, type):
        assert isinstance(x, int)
        assert isinstance(y, int)
        pos = (x, y)

        assert pos not in self.nodes
        self.nodes[pos] = type
    

    def queue_adjacent_node_positions(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)
        # pos = (x, y)

        for p in (
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1)
        ):
            if self.get_node(*p) == self.UNTOUCHED and p not in self.open_node_positions:
                self.open_node_positions.append(p)
    
    def next(self):
        assert len(self.open_node_positions)

        p = self.open_node_positions.pop(0)

        self.build_node(*p, self.EMPTY)
        self.queue_adjacent_node_positions(*p)