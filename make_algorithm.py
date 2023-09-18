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
        self.signals = set()
        self.combinators = set()


    class Signal:
        def __init__(self, simulation, default_value) -> None:
            self.simulation = simulation
            
            self.inputs = set()

            self.default_value = default_value
            self.value = default_value
    
        def add_operation(self, first, operation, second):
            return self.simulation.new_operation(first, operation, second, self)

        def step(self):
            self.value = self.default_value

            for combinator in self.inputs:
                self.value += combinator.output_value
    
    class Combinator:
        lambda_operations = {
            co.ADD: lambda a, b: a + b,

            co.AND: lambda a, b: a and b,

            co.LESS_THAN: lambda a, b: a < b,
            co.EQUAL_TO: lambda a, b: a == b,

            co.LESS_THAN_OR_EQUAL_TO: lambda a, b: a <= b
        }

        def __init__(self, first, operation, second, output) -> None:
            self.first = first
            self.operation = operation
            self.second = second
            
            self.output = output

            self.output_value = 0
        
        def step(self):
            if not self.operation in self.lambda_operations:
                raise NotImplementedError(self.operation)
            
            func = self.lambda_operations[self.operation]

            if isinstance(self.first, Simulation.Signal):
                a = self.first.value
            else:
                assert False, a
            
            if isinstance(self.second, Simulation.Signal):
                b = self.second.value
            else:
                b = self.second
            
            self.output_value = func(a, b)

    
    def new_signal(self, default_value=0):
        signal = self.Signal(self, default_value)
        self.signals.add(signal)
        return signal
    
    def new_operation(self, first, operation, second, output=None):
        if output == None:
            output = self.new_signal()

        combinator = self.Combinator(first, operation, second, output)

        output.inputs.add(combinator)
        self.combinators.add(combinator)

        return output
    

    def step(self):
        for combinator in self.combinators:
            combinator.step()
        
        for signal in self.signals:
            signal.step()

    
    def new_pulse_generator(self, time_on, total_time, on_first=True, increment_signal=None):
        if increment_signal == None:
            increment_signal = self.new_signal(1)

        t = self.new_signal()
        t.add_operation(t, co.LESS_THAN, total_time)

        if on_first:
            out = self.new_operation(t, co.LESS_THAN_OR_EQUAL_TO, time_on)
        else:
            out = self.new_operation(t, co.GREATER_THAN, total_time - time_on)
        
        return out

