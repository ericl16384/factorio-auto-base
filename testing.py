import make_algorithm
import combinator_operations as co

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



    on_time = 1
    total_time = 4
    on_first = True
    increment_signal = None

    if increment_signal == None:
        increment_signal = sim.new_signal(1)

    t = sim.new_signal()
    t.add_operation(t, co.LESS_THAN, total_time)

    c_memory = sim.combinators[-1]

    if on_first:
        out = sim.new_operation(t, co.LESS_THAN_OR_EQUAL_TO, on_time)
    else:
        out = sim.new_operation(t, co.GREATER_THAN, total_time - on_time)
    
    pulse = out



    # pulse = sim.new_pulse_generator(1, 4)

    # print(pulse.inputs.first.inputs)

    print("start")

    while True:
        print(increment_signal.value)
        print(t.value)
        print(c_memory.output_value)
        print(pulse.value)
        input()

        sim.step()















    # make the next_move algorithm

    x = sim.new_signal()
    y = sim.new_signal()
    layer = sim.new_signal()

    next_move_x = sim.new_signal()
    next_move_y = sim.new_signal()
    new_layer = sim.new_signal()

    next_x = sim.new_operation(x, co.ADD, next_move_x)
    next_y = sim.new_operation(y, co.ADD, next_move_y)


    # start
        # if next_x == self.layer and next_y == 0:
        #     self.new_layer += 1
    new_layer.add_operation(
        sim.new_operation(next_x, co.EQUAL_TO, 0),
        co.AND,
        sim.new_operation(next_y, co.EQUAL_TO, 0)
    )




    while True:
        print("x", x.value)
        print("y", y.value)
        print("layer", layer.value)
        print()
        print("new layer", new_layer.value)
        print()
        print()

        input()

        sim.step()
