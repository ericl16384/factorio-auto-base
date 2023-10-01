import random

import combinator_operations as co

import make_blueprint

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
        def __init__(self, simulation, default_value, factorio_signal=None) -> None:
            self.simulation = simulation
            
            self.inputs = []

            self.default_value = default_value
            self.value = default_value

            self.factorio_signal = factorio_signal
    
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
    

    def assign_factorio_signals(self):
        # will override all set factorio_signal

        i = 0

        for s in self.signals:
            s.factorio_signal = make_blueprint.Signal(**FACTORIO_SIGNALS[i]["signal"])
            i += 1
    
    def make_blueprint(self, include_pole=True):
        self.assign_factorio_signals()

        blueprint = make_blueprint.Blueprint()

        x = 0.5
        y = 0

        entities = []

        
        # constant combinators

        default_signals = []
        for signal in self.signals:
            if signal.default_value:
                default_signals.append(signal)
        
        for i in range(0, len(default_signals), 20):
            signal_count_pairs = []
            for j in range(i, min(i + 20, len(default_signals))):
                signal = default_signals[j]
                signal_count_pairs.append((signal.factorio_signal, signal.default_value))

            c = blueprint.add_entity(make_blueprint.ConstantCombinator(x, y + 0.5, make_blueprint.ConstantCombinatorConditions(
                signal_count_pairs
            )))
            x += 1
            entities.append(c)
        

        # combinators

        for combinator in self.combinators:
            first = combinator.first.factorio_signal
            output = combinator.output.factorio_signal

            if isinstance(combinator.second, Simulation.Signal):
                second = combinator.second.factorio_signal
            else:
                second = combinator.second

            conditions = make_blueprint.LogicCombinatorConditions(
                first,
                output,
                combinator.operation,
                second
            )
            
            if combinator.operation in co.arithmetic:
                c = make_blueprint.ArithmeticCombinator(x, y, conditions)
            elif combinator.operation in co.decider:
                c = make_blueprint.DeciderCombinator(x, y, conditions)

            i = blueprint.add_entity(c)
            x += 1
            entities.append(i)

            blueprint.add_connection("red", i, i, 1, 2)
        

        # lamps 

        # i = blueprint.add_entity(make_blueprint.Lamp(x, y, make_blueprint.CircuitCondition(
        #     t.factorio_signal, co.GREATER_THAN_OR_EQUAL_TO, 60
        # )))
        # x += 1
        # entities.append(i)


        # pole

        if include_pole:
            entities.append(blueprint.add_entity(make_blueprint.SmallElectricPole(x, y + 0.5)))
        

        for i in range(len(entities) - 1):
            A = entities[i]
            B = entities[i + 1]

            blueprint.add_connection("red", A, B, 1, 1)

        return blueprint
