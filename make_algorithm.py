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
    
        def add_operation(self, first, operation, second, copy_count=False):
            return self.simulation.new_operation(first, operation, second, self, copy_count)

        def step(self):
            self.value = self.default_value

            for combinator in self.inputs:
                self.value += combinator.output_value
    
    class Combinator:
        def __init__(self, first, operation, second, output, copy_count) -> None:
            
            self.first = first
            self.operation = operation
            self.second = second

            self.output = output

            self.copy_count = copy_count

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
                assert not self.copy_count

            elif self.operation in co.decider:
                self.output_value = co.decider[self.operation](a, b)
                if self.copy_count:
                    # if self.first == self.output:
                    #     self.output_value = self.first.value
                    # elif self.second == self.output:
                    #     self.output_value = self.second.value
                    self.output_value = self.output.value

            else:
                assert False, self.operation

    
    def new_signal(self, default_value=0):
        signal = self.Signal(self, default_value)
        self.signals.append(signal)
        return signal
    
    def new_operation(self, first, operation, second, output=None, copy_count=False):
        self.stationary = False

        if output == None:
            output = self.new_signal()

        combinator = self.Combinator(first, operation, second, output, copy_count)

        output.inputs.append(combinator)
        self.combinators.append(combinator)

        return output
    

    # def add_single_memory(self, write_signal, memory_signal=None, read_signal=None):
    #     raise NotImplementedError
    #     if memory_signal == None:
    #         memory_signal = self.new_signal()
        
    #     memory_signal.add_operation(write_signal, co.EQUAL_TO, 0, True)
    #     memory_signal.add_operation(write_signal, co.MULTIPLY, memory_signal)


    # def time_step_signals(self, signals, delay_length):
    #     # control logic

    #     t = self.new_signal(1)
    #     t.add_operation(t, co.MOD, delay_length)

    #     do_step = self.new_operation(t, co.EQUAL_TO, delay_length)
    #     do_not_step = self.new_operation(t, co.NOT_EQUAL_TO, delay_length)


    #     # find signals to replace

    #     inbound_outbound_pairs = []

    #     for signal in signals:
    #         inbound = self.new_signal()
    #         outbound = signal

    #         inbound_outbound_pairs.append((inbound, outbound))

    #         while outbound.inputs:
    #             combinator = outbound.inputs.pop()
    #             combinator.output = inbound


    #     # replace individually

    #     for inbound, outbound in inbound_outbound_pairs:
    #         # step
    #         outbound.add_operation(do_step, co.MULTIPLY, inbound)
            
    #         # memory
    #         outbound.add_operation(do_not_step, co.MULTIPLY, outbound)


    #     inbounds = []
    #     for i, o in inbound_outbound_pairs:
    #         inbounds.append(i)
    #     return inbounds
    

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
    

    def assign_factorio_signals(self, override=False):
        taken_signals = set()
        for s in self.signals:
            taken_signals.add(s.factorio_signal)

        i = 0

        for s in self.signals:
            while s.factorio_signal == None or override:
                f_signal = make_blueprint.Signal(**FACTORIO_SIGNALS[i]["signal"])
                if f_signal in taken_signals:
                    i += 1
                    continue
                s.factorio_signal = f_signal
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
                second,
                combinator.copy_count
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
