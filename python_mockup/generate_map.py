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