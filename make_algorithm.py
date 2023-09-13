import make_blueprint, random

import json
with open("factorio_signal_list.json", "r") as f:
    FACTORIO_SIGNALS = json.loads(f.read())


class Combinator:
    def __init__(self) -> None:
        pass

class Decider(Combinator):
    def __init__(self) -> None:
        super().__init__()

class Arithmetic(Combinator):
    def __init__(self) -> None:
        super().__init__()


class CombinatorOperation:
    def __init__(self) -> None:
        pass


class Simulation:
    def __init__(self) -> None:
        self.operations = []
        self.signals = []
    
    def new_operation(self):
        raise NotImplementedError
    
    def new_signal(self):
        key = random.randbytes(32)
        print(key)
        self.signals.append(key)
        return key


if __name__ == "__main__":
    sim = Simulation()

    sim.new_signal()
