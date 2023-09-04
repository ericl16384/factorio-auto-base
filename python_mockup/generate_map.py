import random

NO_ORE = "no ore"
IRON_ORE = "iron ore"
COPPER_ORE = "copper ore"

class Map:
    def __init__(self) -> None:
        self.lookup = {}
        self.seed = random.randint(0, 2**64-1)
    
    def get_natural_tile(self, x, y):
        pos = (x, y)

        random.seed(f"{self.seed}{pos}")

        r = random.random()

        if r < 0.1:
            t = IRON_ORE
        elif r < 0.2:
            t = COPPER_ORE
        else:
            t = NO_ORE
        
        return t
    
    # def generate(self, min_x, min_y, max_x, max_y):


    def get_tile(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)

        pos = (x, y)

        if pos not in self.lookup:
            self.lookup[pos] = self.get_natural_tile(*pos)

        return self.lookup[pos]