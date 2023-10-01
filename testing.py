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

    a = sim.new_signal()
    b = sim.new_signal()

    a.add_operation(b, co.ADD, 0)
    b.add_operation(a, co.ADD, b)


    t1 = sim.new_signal()
    t1.add_operation(t1, co.ADD, 1)

    b.add_operation(t1, co.EQUAL_TO, 0)


    a1, b1 = sim.time_step_signals((a, b), 3)
    a1 = a1[0]
    b1 = b1[0]

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


    # # pulse generator

    # pulse_delay = 60

    # t = sim.new_signal(1)
    # t.add_operation(t, co.MOD, pulse_delay)


    # # fibonacci

    # # a = sim.new_signal()
    # # b = sim.new_signal()
    # a_outgoing = sim.new_signal()
    # b_outgoing = sim.new_signal()
    # a_incoming = sim.new_signal()
    # b_incoming = sim.new_signal()

    # # a.add_operation(b, co.ADD, 0)
    # # b.add_operation(a, co.ADD, b)
    # a_incoming.add_operation(b_outgoing, co.ADD, 0)
    # b_incoming.add_operation(a_outgoing, co.ADD, b_outgoing)

    # # b.value += 1


    # # logic stepper

    # do_step = sim.new_operation(t, co.EQUAL_TO, pulse_delay)
    # do_not_step = sim.new_operation(t, co.NOT_EQUAL_TO, pulse_delay)

    # # memory
    # a_outgoing.add_operation(do_not_step, co.MULTIPLY, a_outgoing)
    # b_outgoing.add_operation(do_not_step, co.MULTIPLY, b_outgoing)
    
    # # step
    # a_outgoing.add_operation(do_step, co.MULTIPLY, a_incoming)
    # b_outgoing.add_operation(do_step, co.MULTIPLY, b_incoming)


    # starter signal

    # t1 = sim.new_signal()
    # t1.add_operation(t1, co.ADD, 1)

    # b_outgoing.add_operation(t1, co.EQUAL_TO, 7)
    


    blueprint = sim.make_blueprint()

    print(a.factorio_signal)
    print(b.factorio_signal)
    print()
    print(a1.factorio_signal)
    print(b1.factorio_signal)
    

    with open("custom_blueprint.json", "w") as f:
        print(blueprint.to_json(), file=f)
    print(blueprint.to_encoded())

    input()

    # print(a_incoming.factorio_signal)
    # print(b_incoming.factorio_signal)


    print()
    print("START")
    print()

    tick = 0
    while True:
        print("t =", tick)
        tick += 1

        for signal in sim.signals:
            # if signal not in (
            #     a, b, a1, b1
            # ):
            #     continue

            print(signal.value, "\t", signal.factorio_signal)
        input()

        sim.step()

        if sim.stationary:
            print("STATIONARY")
            break
    




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
