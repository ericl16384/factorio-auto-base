import make_blueprint, random

import combinator_operations as co

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
        self.signals = []
        self.combinators = []

        self.stationary = True


    class Signal:
        def __init__(self, simulation, default_value) -> None:
            self.simulation = simulation
            
            self.inputs = []

            self.default_value = default_value
            self.value = default_value
    
        def add_operation(self, first, operation, second):
            return self.simulation.new_operation(first, operation, second, self)

        def step(self):
            self.value = self.default_value

            for combinator in self.inputs:
                self.value += combinator.output_value
    
    class Combinator:
        def __init__(self, first, operation, second, output, boolean=False) -> None:
            self.first = first
            self.operation = operation
            self.second = second
            
            self.output = output

            self.boolean = boolean

            self.output_value = 0
        
        def step(self):
            if isinstance(self.first, Simulation.Signal):
                a = self.first.value
            else:
                assert False, a
            
            if isinstance(self.second, Simulation.Signal):
                b = self.second.value
            else:
                b = self.second

            if self.operation in co.arithmetic:
                self.output_value = co.arithmetic[self.operation](a, b)
            elif self.operation in co.decider:
                self.output_value = co.decider[self.operation](a, b)
                if not self.boolean:
                    if self.first == self.output:
                        self.output_value = self.first.value
                    elif self.second == self.output:
                        self.output_value = self.second.value
            else:
                assert False, self.operation

    
    def new_signal(self, default_value=0):
        signal = self.Signal(self, default_value)
        self.signals.append(signal)
        return signal
    
    def new_operation(self, first, operation, second, output=None):
        self.stationary = False

        if output == None:
            output = self.new_signal()

        combinator = self.Combinator(first, operation, second, output)

        output.inputs.append(combinator)
        self.combinators.append(combinator)

        return output
    

    def step(self):
        stationary = True

        for combinator in self.combinators:
            combinator.step()
        
        for signal in self.signals:
            v = signal.value

            signal.step()

            if v != signal.value:
                stationary = False
        
        self.stationary = stationary
