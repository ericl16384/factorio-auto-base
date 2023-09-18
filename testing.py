import make_algorithm
import arithmetic_operations, decider_operations

if __name__ == "__main__":
    sim = make_algorithm.Simulation()


    # make the next_move algorithm

    x = sim.new_signal()
    y = sim.new_signal()
    layer = sim.new_signal()

    next_move_x = sim.new_signal()
    next_move_y = sim.new_signal()
    new_layer = sim.new_signal()

    # start
    # if next_move_x == 0 and next_move_y == 0:
    #     new_layer += 1
    is_start_move_x = sim.new_operation(next_move_x, decider_operations.EQUAL_TO, 0)
    is_start_move_y = sim.new_operation(next_move_y, decider_operations.EQUAL_TO, 0)
    new_layer.add_operation(is_start_move_x, arithmetic_operations.AND, is_start_move_y)
