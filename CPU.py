import combinator_operations as co
import make_blueprint as mb



EACH_SIGNAL = mb.Signal("signal-each", "virtual")
EVERYTHING_SIGNAL = mb.Signal("signal-everything", "virtual")
ANYTHING_SIGNAL = mb.Signal("signal-anything", "virtual")

remaining_virtual_signals = []
remaining_virtual_signals.extend("0123456789ABCDEF")
remaining_virtual_signals.reverse()
remaining_virtual_signals = [mb.Signal("signal-"+i, "virtual") for i in remaining_virtual_signals]

CLOCK_SIGNAL = remaining_virtual_signals.pop()
# PROGRAM_COUNTER_SIGNAL = remaining_virtual_signals.pop()
OPCODE_SIGNAL = remaining_virtual_signals.pop()
WRITE_SIGNAL = remaining_virtual_signals.pop()
READA_SIGNAL = remaining_virtual_signals.pop()
READB_SIGNAL = remaining_virtual_signals.pop()
SCALARA_SIGNAL = remaining_virtual_signals.pop()
SCALARB_SIGNAL = remaining_virtual_signals.pop()
# WRITE_PROGRAM_COUNTER_SIGNAL = remaining_virtual_signals.pop()
# CLEAR_MEMORY_SIGNAL = remaining_virtual_signals.pop()



def add_RAM_cell(blueprint, x, y, index):
    offset = 0
    combinators = []

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        ANYTHING_SIGNAL,
        EVERYTHING_SIGNAL,
        co.NOT_EQUAL_TO,
        0,
        True
    ))))
    offset += 2
    storage = combinators[-1]

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        WRITE_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    ))))
    offset += 2
    writer = combinators[-1]

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READA_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    ))))
    offset += 2
    reader_a = combinators[-1]

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READB_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    ))))
    offset += 2
    reader_b = combinators[-1]

    blueprint.add_connection("red", storage, storage, 2, 1)
    blueprint.add_connection("red", storage, writer, 1, 2)
    blueprint.add_connection("red", writer, reader_a, 2, 1)
    blueprint.add_connection("red", reader_a, reader_b, 1, 1)

    return combinators

def link_RAM_cells(blueprint, a, b):
    blueprint.add_connection("green", a[1], b[1], 1, 1)
    blueprint.add_connection("green", a[2], b[2], 1, 1)
    blueprint.add_connection("green", a[2], b[2], 2, 2)
    blueprint.add_connection("green", a[3], b[3], 1, 1)
    blueprint.add_connection("green", a[3], b[3], 2, 2)

def add_RAM_submodule(blueprint, x, y, length, starting_index):
    cells = []
    for i in range(length):
        cells.append(add_RAM_cell(blueprint, x+i, y, i+starting_index))

        if i > 0:
            link_RAM_cells(blueprint, cells[-1], cells[-2])
    return cells

# def add_folded_memory_block(blueprint, x, y, length, layers, layer_spacing, starting_offset):
#     blocks = []
#     for i in range(layers):
#         blocks.append(add_RAM_submodule(blueprint, x, y+i*(8+layer_spacing), length, i*length+starting_offset))

#         if i > 0:
#             link_RAM_cells(blueprint, blocks[-1][0], blocks[-2][0])
#     return blocks

def add_RAM_module(blueprint, x, y, width, height):
    length = 18*width

    blocks = []
    index = 0
    for i in range(height):
        blocks.append(add_RAM_submodule(blueprint, x, y+i*18, length, index))
        index += length

        if i > 0:
            link_RAM_cells(blueprint, blocks[-1][0], blocks[-2][0])
        
        for j in range(width):
            blueprint.add_entity(mb.Substation(x+9+j*18, y+9+i*18))

        blocks.append(add_RAM_submodule(blueprint, x, y+i*18+10, length, index))
        index += length

        link_RAM_cells(blueprint, blocks[-1][0], blocks[-2][0])
    
    return blocks


def add_ROM_cell(blueprint, x, y, index, opcode, write, reada, readb):
    offset = 0
    combinators = []

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READA_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    ))))
    offset += 2
    reader = combinators[-1]

    combinators.append(blueprint.add_entity(mb.ConstantCombinator(x+0.5, y+offset+0.5, mb.ConstantCombinatorConditions((
        (OPCODE_SIGNAL, opcode),
        (WRITE_SIGNAL, write),
        (READA_SIGNAL, reada),
        (READB_SIGNAL, readb)
    )))))
    offset += 1
    storage = combinators[-1]

    blueprint.add_connection("red", reader, storage, 1, 1)

    return combinators

def link_ROM_cells(blueprint, a, b):
    blueprint.add_connection("green", a[0], b[0], 1, 1)
    blueprint.add_connection("green", a[0], b[0], 2, 2)

def add_ROM_submodule(blueprint, x, y, length, starting_index, instructions):
    cells = []
    for i in range(length):
        if i < len(instructions):
            instruction = instructions[i]
        else:
            instruction = (0, 0, 0, 0)
        cells.append(add_ROM_cell(blueprint, x+i, y, i+starting_index, *instruction))

        if i > 0:
            link_ROM_cells(blueprint, cells[-1], cells[-2])
    return cells

def add_ROM_module(blueprint, x, y, width, height, instructions):
    length = 18*width

    blocks = []
    index = 0
    for i in range(height):
        blocks.append(add_ROM_submodule(blueprint, x, y+i*18, length, index, instructions[index:index+length]))
        index += length
        if i > 0:
            link_ROM_cells(blueprint, blocks[-1][0], blocks[-2][0])

        blocks.append(add_ROM_submodule(blueprint, x, y+i*18+4, length, index, instructions[index:index+length]))
        index += length
        link_ROM_cells(blueprint, blocks[-1][0], blocks[-2][0])
        
        for j in range(width):
            blueprint.add_entity(mb.Substation(x+9+j*18, y+9+i*18))

        blocks.append(add_ROM_submodule(blueprint, x, y+i*18+10, length, index, instructions[index:index+length]))
        index += length
        link_ROM_cells(blueprint, blocks[-1][0], blocks[-2][0])

        blocks.append(add_ROM_submodule(blueprint, x, y+i*18+14, length, index, instructions[index:index+length]))
        index += length
        link_ROM_cells(blueprint, blocks[-1][0], blocks[-2][0])
    
    return blocks


def add_ALU_cells(blueprint, x, y, index, is_arithmetic, logic:mb.LogicCombinatorConditions):
    offset = 0
    combinators = []

    assert is_arithmetic # TODO

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        OPCODE_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    ))))
    offset += 2
    indexer = combinators[-1]

    combinators.append(blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+offset+1, logic)))
    offset += 2
    operator = combinators[-1]

    blueprint.add_connection("red", indexer, operator, 1, 2)

    return combinators

def link_ALU_cells(blueprint, a, b):
    blueprint.add_connection("green", a[0], b[0], 1, 1)
    blueprint.add_connection("green", a[0], b[0], 2, 2)
    blueprint.add_connection("green", a[1], b[1], 1, 1)

def add_ALU_controller(blueprint, x, y, clock_interval):
    offset = 0
    combinators = []


    # clock

    combinators.append(blueprint.add_entity(mb.ConstantCombinator(x+0.5, y+offset+0.5, mb.ConstantCombinatorConditions((
        (CLOCK_SIGNAL, 1),
    )))))
    offset += 1
    constant = combinators[-1]

    combinators.append(blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.MOD,
        clock_interval
    ))))
    offset += 2
    modulus = combinators[-1]

    combinators.append(blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.EQUAL_TO,
        clock_interval
    ))))
    offset += 2
    clock = combinators[-1]

    blueprint.add_connection("red", constant, modulus, 1, 2)
    blueprint.add_connection("red", modulus, modulus, 1, 2)
    blueprint.add_connection("red", modulus, clock, 1, 1)


    # program counter



def add_ALU_module(blueprint, opcodes, x, y, RAM_refresh_length):
    max_operation_length = RAM_refresh_length * 10 # tbd of course

    add_ALU_controller(blueprint, x, y, max_operation_length)

    cells = []
    for i, opcode in enumerate(opcodes):
        cells.append(add_ALU_cells(blueprint, x+i+2, y, i, True, mb.LogicCombinatorConditions(*opcode)))
        if i > 0:
            link_ALU_cells(blueprint, cells[-1], cells[-2])
    blueprint.add_entity(mb.Substation(x+9, y+9))
    return cells



if __name__ == "__main__":

    print("running main cpu program")

    blueprint = mb.Blueprint()

    RAM_refresh_length = 10 # tbd of course :)

    # ALU
    opcodes = [
        [
            SCALARA_SIGNAL,
            SCALARA_SIGNAL,
            operation,
            SCALARB_SIGNAL
        ] for operation in co.arithmetic
    ]
    add_ALU_module(blueprint, opcodes, 0, 0, RAM_refresh_length)

    # ROM
    instructions = [
        (2, 3, 4, 5)
    ]
    add_ROM_module(blueprint, 18, 0, 1, 1, instructions)

    # RAM
    add_RAM_module(blueprint, 0, 18, 2, 1)
    # blueprint.add_connection( wire


    encoded = blueprint.to_encoded()
    # print(encoded)
    with open("new_blueprint.txt", "w") as f:
        print(encoded, file=f)
    # input()

    print("finished")
