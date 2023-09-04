class BaseController:
    def __init__(self, base) -> None:
        self.base = base

        self.open_node_positions = []
        self.queue_adjacent_node_positions(*base.start_pos)

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
            if self.base.get_node(*p) == self.base.UNTOUCHED and p not in self.open_node_positions:
                self.open_node_positions.append(p)
    
    def next(self):
        assert len(self.open_node_positions)

        p = self.open_node_positions.pop(0)

        self.base.build_node(*p, self.base.EMPTY)
        self.queue_adjacent_node_positions(*p)