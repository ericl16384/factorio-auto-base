import combinator_operations as co
import make_algorithm
import make_blueprint

def new_pulse_generator(sim, on_time, total_time, on_first):
    if increment_signal == None:
        increment_signal = sim.new_signal(1)

    t = sim.new_signal()
    t.add_operation(t, co.LESS_THAN, total_time)

    if on_first:
        out = sim.new_operation(t, co.LESS_THAN_OR_EQUAL_TO, on_time)
    else:
        out = sim.new_operation(t, co.GREATER_THAN, total_time - on_time)
    
    return out

if __name__ == "__main__":
    sim = make_algorithm.Simulation()




    # # fibonacci

    # a = sim.new_signal()
    # b = sim.new_signal()

    # a.add_operation(b, co.ADD, 0)
    # b.add_operation(a, co.ADD, b)

    # b.value += 1

    # print("START")
    # print()

    # for i in range(16):
    #     print(f"a = {a.value}")
    #     # print(f"b = {b.value}")
    #     # print(f"c = {c.value}")
    #     print()

    #     sim.step()

    #     if sim.stationary:
    #         print("STATIONARY")
    #         break



    # pulse generator

    t = sim.new_signal(1)
    t.add_operation(t, co.MOD, 60)
    



    sim.assign_factorio_signals()

    blueprint = make_blueprint.Blueprint()

    x = 0.5
    y = 0

    circuit_keys = []

    default_signals = []
    for signal in sim.signals:
        if signal.default_value:
            default_signals.append(signal)
    
    for i in range(0, len(default_signals), 20):
        signal_count_pairs = []
        for j in range(i, min(i + 20, len(default_signals))):
            signal = default_signals[j]
            signal_count_pairs.append((signal.factorio_signal, signal.default_value))

        c = blueprint.add_entity(make_blueprint.ConstantCombinator(x, y + 0.5, make_blueprint.ConstantCombinatorConditions(signal_count_pairs)))
        circuit_keys.append(c)
        x += 1

    for combinator in sim.combinators:
        first = combinator.first.factorio_signal
        output = combinator.output.factorio_signal

        if isinstance(combinator.second, make_algorithm.Simulation.Signal):
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
        x += 1

        i = blueprint.add_entity(c)
        blueprint.add_connection("red", i, i, 1, 2)
        # break

        circuit_keys.append(i)
    
    for i in range(len(circuit_keys) - 1):
        A = circuit_keys[i]
        B = circuit_keys[i + 1]

        blueprint.add_connection("red", A, B, 1, 1)

    with open("custom_blueprint.json", "w") as f:
        print(blueprint.to_json(), file=f)
    print(blueprint.to_encoded())




    # on_time = 1
    # total_time = 4
    # on_first = True
    # increment_signal = None

    # if increment_signal == None:
    #     increment_signal = sim.new_signal(1)

    # t = sim.new_signal()
    # t.add_operation(t, co.LESS_THAN, total_time)

    # c_memory = sim.combinators[-1]

    # if on_first:
    #     out = sim.new_operation(t, co.LESS_THAN_OR_EQUAL_TO, on_time)
    # else:
    #     out = sim.new_operation(t, co.GREATER_THAN, total_time - on_time)
    
    # pulse = out



    # # pulse = sim.new_pulse_generator(1, 4)

    # # print(pulse.inputs.first.inputs)

    # print("start")

    # while True:
    #     print(increment_signal.value)
    #     print(t.value)
    #     print(c_memory.output_value)
    #     print(pulse.value)
    #     input()

    #     sim.step()















    # # make the next_move algorithm

    # x = sim.new_signal()
    # y = sim.new_signal()
    # layer = sim.new_signal()

    # next_move_x = sim.new_signal()
    # next_move_y = sim.new_signal()
    # new_layer = sim.new_signal()

    # next_x = sim.new_operation(x, co.ADD, next_move_x)
    # next_y = sim.new_operation(y, co.ADD, next_move_y)


    # # start
    #     # if next_x == self.layer and next_y == 0:
    #     #     self.new_layer += 1
    # new_layer.add_operation(
    #     sim.new_operation(next_x, co.EQUAL_TO, 0),
    #     co.AND,
    #     sim.new_operation(next_y, co.EQUAL_TO, 0)
    # )




    # while True:
    #     print("x", x.value)
    #     print("y", y.value)
    #     print("layer", layer.value)
    #     print()
    #     print("new layer", new_layer.value)
    #     print()
    #     print()

    #     input()

    #     sim.step()
