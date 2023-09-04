import random

class Map:
    NO_ORE = "no ore"
    IRON_ORE = "iron ore"
    COPPER_ORE = "copper ore"

    def __init__(self) -> None:
        self.seed = random.randint(0, 2**64-1)
        self.tiles = {}
    
    def get_generated_tile(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)
        pos = (x, y)

        random.seed(f"{self.seed}{pos}")

        r = random.random()

        if r < 0.05:
            t = self.IRON_ORE
        elif r < 0.10:
            t = self.COPPER_ORE
        else:
            t = self.NO_ORE
        
        return t
    
    # def generate_tile(self, x, y):
    #     pos = (x, y)
    #     self.tiles[pos] = self.get_generated_tile(*pos)

    # def generate_area(self, min_x, min_y, max_x, max_y):
    #     pass

    def get_tile(self, x, y):
        pos = (x, y)

        if pos not in self.tiles:
            self.tiles[pos] = self.get_generated_tile(*pos)

        return self.tiles[pos]

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
        self.start_pos = (start_x, start_y)

        self.nodes = {}

        self.build_node(*self.start_pos, self.CONTROL_LOGIC)

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
    