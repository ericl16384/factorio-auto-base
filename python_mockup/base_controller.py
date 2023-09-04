import simulation

class GetNextMove:
    def __init__(self) -> None:
        self.node = 0

        self.x = 0
        self.y = 0
        self.layer = 0

        self.next_move_x = 0
        self.next_move_y = 0
        self.new_layer = 0
    
    def next(self):
        # print(f"move=\t({next_move_x},\t{next_move_y})")

        # print(f"self.node={n}\t({self.x},\t{self.y})\t{self.layer}")
        # yield (next_move_x, next_move_y)


        # assert (self.x, self.y) not in all_previous
        # all_previous.add((self.x, self.y))


        # input()
        # print()


        # new layer
        if self.new_layer:
            self.next_move_y -= self.next_move_y
            self.new_layer -= self.new_layer


        # right side
        if self.x == self.layer and self.next_move_x > 0:
            self.next_move_x -= 1
            self.next_move_y += 1
            # print(f"move switched")
        
        # top side
        if self.y == self.layer and self.next_move_y > 0:
            self.next_move_x -= 1
            self.next_move_y -= 1
            # print(f"move switched")
        
        # left side
        if self.x == -self.layer and self.next_move_x < 0:
            self.next_move_x += 1
            self.next_move_y -= 1
            # print(f"move switched")
        
        # bottom side
        if self.y == -self.layer and self.next_move_y < 0:
            self.next_move_x += 1
            self.next_move_y += 1
            # print(f"move switched")


        # start
        if self.next_move_x == 0 and self.next_move_y == 0:
            self.new_layer += 1
        
        # new layer
        if self.x == self.layer and self.y == -1:
            self.new_layer += 1
        
        if self.new_layer:
            self.next_move_x -= self.next_move_x
            self.next_move_y -= self.next_move_y
            self.layer += 1
            self.next_move_x = self.layer - self.x
            self.next_move_y = -self.y
        
        
        out = ((self.x, self.y), self.node)

        self.x += self.next_move_x
        self.y += self.next_move_y

        self.node += 1

        return out


class BaseController:
    def __init__(self, base: simulation.Base) -> None:
        self.base = base

        self.get_next_move = GetNextMove()
        self.get_next_move.next()

        # self.open_node_positions = []
        # self.queue_adjacent_node_positions(*base.start_pos)

    def queue_adjacent_node_positions(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)
        # pos = (x, self.y)

        for p in (
            (x + 1, self.y),
            (x, self.y + 1),
            (x - 1, self.y),
            (x, self.y - 1)
        ):
            if self.base.get_node(*p) == self.base.UNTOUCHED and p not in self.open_node_positions:
                self.open_node_positions.append(p)
    
    def next(self):
        # assert len(self.open_node_positions)

        # p = self.open_node_positions.pop(0)

        # self.base.build_node(*p, self.base.EMPTY)
        # self.queue_adjacent_node_positions(*p)

        self.base.build_node(*self.get_next_move.next()[0], self.base.EMPTY)