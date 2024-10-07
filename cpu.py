import combinator_operations as co
import make_blueprint as mb


registered_signals = {}
def new_sig(name, signal):
    registered_signals[name] = signal
    return signal

EACH_SIGNAL = new_sig("each", mb.Signal("signal-each", "virtual"))
EVERYTHING_SIGNAL = new_sig("everything", mb.Signal("signal-everything", "virtual"))
ANYTHING_SIGNAL = new_sig("anything", mb.Signal("signal-anything", "virtual"))

# remaining_virtual_signals = []
# remaining_virtual_signals.extend("0123456789ABCDEF")
# remaining_virtual_signals.reverse()
# remaining_virtual_signals = [mb.Signal("signal-"+i, "virtual") for i in remaining_virtual_signals]

CLOCK_SIGNAL = new_sig("clock", mb.Signal("signal-T", "virtual"))
PROGRAM_COUNTER_SIGNAL = new_sig("program_counter", mb.Signal("signal-I", "virtual"))
OPCODE_SIGNAL = new_sig("opcode", mb.Signal("signal-O", "virtual"))

WRITE_SIGNAL = new_sig("write", mb.Signal("signal-W", "virtual"))
READA_SIGNAL = new_sig("reada", mb.Signal("signal-A", "virtual"))
READB_SIGNAL = new_sig("readb", mb.Signal("signal-B", "virtual"))
SCALARA_SIGNAL = new_sig("scalara", mb.Signal("signal-X", "virtual"))
SCALARB_SIGNAL = new_sig("scalarb", mb.Signal("signal-Y", "virtual"))
RAM_SIGNAL = new_sig("scalarb", mb.Signal("signal-Z", "virtual"))

# WRITE_PROGRAM_COUNTER_SIGNAL = remaining_virtual_signals.pop()
# CLEAR_MEMORY_SIGNAL = remaining_virtual_signals.pop()
RESET_SIGNAL = new_sig("reset", mb.Signal("signal-R", "virtual"))


print()
for name, signal in registered_signals.items():
    print(name, " "*(20-len(name)), signal["name"])
print()








def add_RAM_cell(blueprint, x, y, index):
    offset = 0
    combinators = {}

    combinators["storage"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        RESET_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        0,
        True
    )))
    offset += 2

    combinators["writer"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        WRITE_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    combinators["reader_a"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READA_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    combinators["reader_b"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READB_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    blueprint.add_connection("red", combinators["storage"], combinators["storage"], 2, 1)
    blueprint.add_connection("red", combinators["storage"], combinators["writer"], 1, 2)
    blueprint.add_connection("red", combinators["writer"], combinators["reader_a"], 2, 1)
    blueprint.add_connection("red", combinators["reader_a"], combinators["reader_b"], 1, 1)

    return combinators

def link_RAM_cells(blueprint, a, b):
    blueprint.add_connection("green", a["writer"], b["writer"], 1, 1)
    blueprint.add_connection("green", a["reader_a"], b["reader_a"], 1, 1)
    blueprint.add_connection("green", a["reader_a"], b["reader_a"], 2, 2)
    blueprint.add_connection("green", a["reader_b"], b["reader_b"], 1, 1)
    blueprint.add_connection("green", a["reader_b"], b["reader_b"], 2, 2)

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

    cells = []
    index = 0
    for i in range(height):
        cells.extend(add_RAM_submodule(blueprint, x, y+i*18, length, index))
        if i > 0:
            link_RAM_cells(blueprint, cells[index], cells[index-length])
        index += length
        
        for j in range(width):
            blueprint.add_entity(mb.Substation(x+9+j*18, y+9+i*18))

        cells.extend(add_RAM_submodule(blueprint, x, y+i*18+10, length, index))
        link_RAM_cells(blueprint, cells[index], cells[index-length])
        index += length

    return cells


def create_instruction(opcode=0, write=0, reada=0, readb=0, scalara=0, scalarb=0):
    return (opcode, write, reada, readb, scalara, scalarb)

def add_ROM_cell(blueprint, x, y, index, instruction):
    opcode, write, reada, readb, scalara, scalarb = instruction

    offset = 0
    combinators = {}

    combinators["reader"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        PROGRAM_COUNTER_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    combinators["storage"] = blueprint.add_entity(mb.ConstantCombinator(x+0.5, y+offset+0.5, mb.ConstantCombinatorConditions((
        (OPCODE_SIGNAL, opcode),
        (WRITE_SIGNAL, write),
        (READA_SIGNAL, reada),
        (READB_SIGNAL, readb),
        (SCALARA_SIGNAL, scalara),
        (SCALARB_SIGNAL, scalarb),
    ))))
    offset += 1

    blueprint.add_connection("red", combinators["reader"], combinators["storage"], 1, 1)

    return combinators

def link_ROM_cells(blueprint, a, b):
    blueprint.add_connection("green", a["reader"], b["reader"], 1, 1)
    blueprint.add_connection("green", a["reader"], b["reader"], 2, 2)

def add_ROM_submodule(blueprint, x, y, length, starting_index, instructions):
    cells = []
    for i in range(length):
        if i < len(instructions):
            instruction = instructions[i]
        else:
            instruction = create_instruction()
        cells.append(add_ROM_cell(blueprint, x+i, y, i+starting_index, instruction))

        if i > 0:
            link_ROM_cells(blueprint, cells[-1], cells[-2])
    return cells

def add_ROM_module(blueprint, x, y, width, height, instructions):
    length = 18*width
    sublength = length//2 - 1

    cells = []
    index = 0
    for i in range(height):
        # row 1
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18, length, index, instructions[index:index+length]))
        if i > 0:
            link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += length

        # row 2
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+3, length, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += length

        # row 3a (before substation)
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+6, sublength, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += sublength

        # row 3b (after substation)
        cells.extend(add_ROM_submodule(blueprint, x+10, y+i*18+6, sublength, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-1])
        index += sublength

        # row 4a (before substation)
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+9, sublength, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-sublength*2])
        index += sublength

        # row 4b (after substation)
        cells.extend(add_ROM_submodule(blueprint, x+10, y+i*18+9, sublength, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-1])
        index += sublength

        # row 5
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+12, length, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-sublength*2])
        index += length

        # row 6
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+15, length, index, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += length
        
        for j in range(width):
            blueprint.add_entity(mb.Substation(x+9+j*18, y+9+i*18))
    
    return cells


def add_ALU_cells(blueprint, x, y, index, is_arithmetic, logic:mb.LogicCombinatorConditions):
    offset = 0
    combinators = {}

    assert is_arithmetic # TODO

    combinators["indexer"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        OPCODE_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    combinators["operator"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+offset+1, logic))
    offset += 2

    blueprint.add_connection("red", combinators["indexer"], combinators["operator"], 1, 2)

    return combinators

def link_ALU_cells(blueprint, a, b):
    blueprint.add_connection("green", a["indexer"], b["indexer"], 1, 1)
    blueprint.add_connection("green", a["indexer"], b["indexer"], 2, 2)
    blueprint.add_connection("green", a["operator"], b["operator"], 1, 1)

def add_ALU_controller(blueprint, x, y, clock_interval):
    offset = 0
    combinators = {}


    # accumulator register
        # program counter

    combinators["accumulator_register"] = blueprint.add_entity(mb.DeciderCombinator(x+17.5, y+offset+1, mb.LogicCombinatorConditions(
        RESET_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        0,
        True
    )))
    offset += 2


    # clock

    combinators["clock"] = blueprint.add_entity(mb.DeciderCombinator(x+17.5, y+offset+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.EQUAL_TO,
        clock_interval
    )))
    offset += 2

    combinators["modulus"] = blueprint.add_entity(mb.ArithmeticCombinator(x+17.5, y+offset+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.MOD,
        clock_interval
    )))
    offset += 2

    combinators["constant"] = blueprint.add_entity(mb.ConstantCombinator(x+17.5, y+offset+0.5, mb.ConstantCombinatorConditions((
        (CLOCK_SIGNAL, 1),
    ))))
    offset += 1

    blueprint.add_connection("red", combinators["constant"], combinators["modulus"], 1, 2)
    blueprint.add_connection("red", combinators["modulus"], combinators["modulus"], 1, 2)
    blueprint.add_connection("red", combinators["modulus"], combinators["clock"], 1, 1)


    return combinators

def add_ALU_module(blueprint, opcodes, x, y, RAM_refresh_length):
    max_operation_length = RAM_refresh_length * 10 # tbd of course

    blocks = {}
    blocks["controller"] = add_ALU_controller(blueprint, x, y, max_operation_length)

    blocks["operations"] = []
    for i, opcode in enumerate(opcodes):
        blocks["operations"].append(add_ALU_cells(blueprint, x+i, y, i, True, mb.LogicCombinatorConditions(*opcode)))
        if i > 0:
            link_ALU_cells(blueprint, blocks["operations"][-1], blocks["operations"][-2])

    blueprint.add_entity(mb.Substation(x+9, y+9))

    return blocks



def link_ALU_ROM(blueprint, alu, rom):
    blueprint.add_connection("green", alu["controller"]["accumulator_register"], rom[0]["reader"], 2, 1)

def link_ROM_RAM(blueprint, rom, ram, rom_index, ram_index):
    blueprint.add_connection("green", rom[rom_index]["reader"], ram[ram_index]["reader_a"], 2, 1)
    blueprint.add_connection("green", ram[ram_index]["reader_a"], ram[ram_index]["reader_b"], 1, 1)





# connect rom output to ram input (reada readb)



def main(program_instructions):

    print("running main cpu program")

    blueprint = mb.Blueprint()

    RAM_refresh_length = 10 # tbd of course :)

    # ALU
    opcodes = [
        [
            SCALARA_SIGNAL,
            RAM_SIGNAL,
            operation,
            SCALARB_SIGNAL
        ] for operation in co.arithmetic
    ]
    alu = add_ALU_module(blueprint, opcodes, 0, 0, RAM_refresh_length)

    # ROM
    rom = add_ROM_module(blueprint, 18, 0, 1, 1, program_instructions)

    link_ALU_ROM(blueprint, alu, rom)

    # RAM
    ram = add_RAM_module(blueprint, 36, 0, 1, 1)
    # blueprint.add_connection( wire

    link_ROM_RAM(blueprint, rom, ram, 103, 18)


    encoded = blueprint.to_encoded()
    # print(encoded)
    with open("new_blueprint.txt", "w") as f:
        print(encoded, file=f)
    # input()

    print("finished")






if __name__ == "__main__":
    instructions = [
        create_instruction(2, 1, 0, 0, 123, 456),
        create_instruction(6, 5, 4, 3, 2, 1),
        
        create_instruction(6, 0, 0, 0, 0, 0),
        create_instruction(0, 5, 0, 0, 0, 0),
        create_instruction(0, 0, 4, 0, 0, 0),
        create_instruction(0, 0, 0, 3, 0, 0),
        create_instruction(0, 0, 0, 0, 2, 0),
        create_instruction(0, 0, 0, 0, 0, 1),
    ]
    main(instructions)
