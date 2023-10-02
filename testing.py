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

    # t = sim.new_signal()
    # t.add_operation(t, co.ADD, 1)

    # out = sim.new_operation(t, co.MULTIPLY, 10)




    # t1 = sim.new_signal()
    # t1.add_operation(t1, co.ADD, 1)

    # b.add_operation(t1, co.EQUAL_TO, 0)


    # a1, b1 = sim.time_step_signals((a, b), 3)
    # a1 = a1[0]
    # b1 = b1[0]

    # sim.time_step_signals([out], 5)

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




    propagation_delay = 30

    propagation_clock = sim.new_signal(1)

    # IMPORTANT! TURN THIS ON FOR AUTO DEPLOY
    propagation_clock.add_operation(propagation_clock, co.MOD, propagation_delay)

    node = sim.new_signal()

    x = sim.new_signal()
    y = sim.new_signal()
    layer = sim.new_signal()

    next_move_x = sim.new_signal()
    next_move_y = sim.new_signal()
    # north = sim.new_signal()
    # east = sim.new_signal()
    # south = sim.new_signal()
    # west = sim.new_signal()
    new_layer = sim.new_signal()


    # memory
    node.add_operation(node, co.ADD, 0)
    x.add_operation(x, co.ADD, 0)
    y.add_operation(y, co.ADD, 0)
    layer.add_operation(layer, co.ADD, 0)
    # next_move_x.add_operation(next_move_x, co.ADD, 0)
    # next_move_y.add_operation(next_move_y, co.ADD, 0)

    # step
    step_flag = sim.new_operation(propagation_clock, co.EQUAL_TO, propagation_delay)
    # negative_step_flag = sim.new_operation(step_flag, co.MULTIPLY, -1)
    node.add_operation(step_flag, co.ADD, 0)
    x.add_operation(next_move_x, co.MULTIPLY, step_flag)
    y.add_operation(next_move_y, co.MULTIPLY, step_flag)
    # y.add_operation(north, co.MULTIPLY, negative_step_flag)
    # x.add_operation(east, co.MULTIPLY, step_flag)
    # y.add_operation(south, co.MULTIPLY, step_flag)
    # x.add_operation(west, co.MULTIPLY, negative_step_flag)
    layer.add_operation(new_layer, co.MULTIPLY, step_flag)

    # usefuls
    negative_layer = sim.new_operation(layer, co.MULTIPLY, -1)



    # next_x = sim.new_operation(x, co.ADD, next_move_x)
    # next_y = sim.new_operation(y, co.ADD, next_move_y)


    # if node 0 (start)
    new_layer.add_operation(node, co.EQUAL_TO, 0)

    # if layer finished
    new_layer_conditions = sim.new_signal()
    new_layer_conditions.add_operation(x, co.EQUAL_TO, layer)
    new_layer_conditions.add_operation(y, co.EQUAL_TO, -1)
    # new_layer_conditions.add_operation(next_move_x, co.EQUAL_TO, 0)
    # new_layer_conditions.add_operation(next_move_y, co.EQUAL_TO, 1)
    new_layer.add_operation(new_layer_conditions, co.EQUAL_TO, 2)

    # new layer
    next_move_x.add_operation(new_layer, co.MULTIPLY, 1)


    # side checks
    right_side = sim.new_operation(x, co.EQUAL_TO, layer)
    bottom_side = sim.new_operation(y, co.EQUAL_TO, layer)
    left_side = sim.new_operation(x, co.EQUAL_TO, negative_layer)
    top_side = sim.new_operation(y, co.EQUAL_TO, negative_layer)

    # corner checks
    right_bottom = sim.new_operation(bottom_side, co.AND, right_side)
    bottom_left = sim.new_operation(bottom_side, co.AND, left_side)
    left_top = sim.new_operation(top_side, co.AND, left_side)
    top_right = sim.new_operation(top_side, co.AND, right_side)

    # move on sides
    next_move_y.add_operation(right_side, co.MULTIPLY, 1)
    next_move_x.add_operation(bottom_side, co.MULTIPLY, -1)
    next_move_y.add_operation(left_side, co.MULTIPLY, -1)
    next_move_x.add_operation(top_side, co.MULTIPLY, 1)

    # cancel on corners
    next_move_y.add_operation(right_bottom, co.MULTIPLY, -1)
    next_move_x.add_operation(bottom_left, co.MULTIPLY, 1)
    next_move_y.add_operation(left_top, co.MULTIPLY, 1)
    next_move_x.add_operation(top_right, co.MULTIPLY, -1)


    # output
    output_x = sim.new_operation(x, co.ADD, 0)
    output_y = sim.new_operation(y, co.ADD, 0)


    # set important signals
    output_x.factorio_signal = make_blueprint.Signal("signal-X", "virtual")
    output_y.factorio_signal = make_blueprint.Signal("signal-Y", "virtual")
    sim.new_signal().factorio_signal = make_blueprint.Signal("signal-W", "virtual")
    sim.new_signal().factorio_signal = make_blueprint.Signal("signal-H", "virtual")
    step_flag.factorio_signal = make_blueprint.Signal("transport-belt", "item")
    


    blueprint = sim.make_blueprint()

    # print(a.factorio_signal)
    # print(b.factorio_signal)
    # print()
    # print(a1.factorio_signal)
    # print(b1.factorio_signal)
    

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

        if propagation_clock.value == propagation_delay:
            for signal, name in (
                (propagation_clock, "c"),
                (step_flag, "step"),
                (node, "node"),
                (x, "x"),
                (y, "y"),
                (layer, "layer"),
                (next_move_x, "nx"),
                (next_move_y, "ny"),
                (new_layer, "nl"),
                (right_bottom, "rb"),
                (bottom_left, "bl"),
                (left_top, "lt"),
                (top_right, "tr"),
            ):
                print(name, "\t", signal.value, "\t", signal.factorio_signal)
            input()

        # for signal in sim.signals:
        #     print("\t", signal.value, "\t", signal.factorio_signal)


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
