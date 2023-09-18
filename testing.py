import make_algorithm
import combinator_operations as co

if __name__ == "__main__":
    sim = make_algorithm.Simulation()



    pulse = sim.new_pulse_generator(1, 60)

    while True:
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
