import make_blueprint, random

import arithmetic_operations, decider_operations

import json
with open("factorio_signal_list.json", "r") as f:
    FACTORIO_SIGNALS = json.loads(f.read())


# class Combinator:
#     def __init__(self) -> None:
#         pass

# class Decider(Combinator):
#     def __init__(self) -> None:
#         super().__init__()

# class Arithmetic(Combinator):
#     def __init__(self) -> None:
#         super().__init__()


# class CombinatorOperation:
#     def __init__(self) -> None:
#         pass

#     def simulate(self, input_signals):
#         output_signals = {}
#         return output_signals


class Simulation:
    def __init__(self) -> None:
        self.combinators = set()
        self.signals = set()


    class Signal:
        def __init__(self, simulation) -> None:
            self.simulation = simulation
    
        def add_operation(self, first, operator, second):
            return self.simulation.new_operation(first, operator, second, self)
    
    class Combinator:
        def __init__(self, first, operator, second, output) -> None:
            self.first = first
            self.operator = operator
            self.second = second
            
            self.output = output
    

    # def new_operation(self):
    #     raise NotImplementedError

    # def new_identifier(self):
    #     return random.randbytes(32)

    # def new_operation(self, first, operator, second):
    #     output = self.new_signal()
    #     return self.add_operation(first, operator, second, output)
    
    def new_operation(self, first, operator, second, output=None):
        if output == None:
            output = self.new_signal()
        operation = self.Combinator(first, operator, second, output)
        self.combinators.add(operation)
        return output
    
    def new_signal(self):
        signal = self.Signal(self)
        self.signals.add(signal)
        return signal
