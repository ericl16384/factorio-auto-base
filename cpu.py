import combinator_operations as co
import make_blueprint as mb



class Combinator_System:
    def __init__(self, combinator_behaviors, wire_links, tick_length) -> None:
        self.combinator_behaviors = combinator_behaviors
        self.wire_links = wire_links
        self.tick_length = tick_length

class Combinator_CPU:
    def __init__(self) -> None:
        self.signals = {}
        self.alu_operations = []
        self.rom_instructions = []
        self.ram_size = 0
        
        self.EACH_SIGNAL = self.add_signal("each", mb.Signal("signal-each", "virtual"))
        self.EVERYTHING_SIGNAL = self.add_signal("everything", mb.Signal("signal-everything", "virtual"))
        self.ANYTHING_SIGNAL = self.add_signal("anything", mb.Signal("signal-anything", "virtual"))

    def add_signal(self, name, signal):
        assert name not in self.signals, name
        self.signals[name] = signal
        return signal
    
    def add_alu_operation(self, operation:Combinator_System):
        self.alu_operations.append(operation)
    
    def add_rom_instruction(self, instruction):
        self.rom_instructions.append(instruction)
    
    def init_basic_signals(self):
        self.add_signal("clock", mb.Signal("signal-T", "virtual"))
        self.add_signal("program_counter", mb.Signal("signal-I", "virtual"))
        self.add_signal("opcode", mb.Signal("signal-O", "virtual"))
        self.add_signal("write", mb.Signal("signal-W", "virtual"))
        self.add_signal("reada", mb.Signal("signal-A", "virtual"))
        self.add_signal("readb", mb.Signal("signal-B", "virtual"))
        self.add_signal("scalara", mb.Signal("signal-X", "virtual"))
        self.add_signal("scalarb", mb.Signal("signal-Y", "virtual"))
        self.add_signal("data", mb.Signal("signal-Z", "virtual"))
        self.add_signal("reset", mb.Signal("signal-R", "virtual"))
    
    def init_basic_operations(self):
        for operation in co.arithmetic:
            self.add_alu_operation(Combinator_System([
                [
                    self.signals["scalara"],
                    self.signals["data"],
                    operation,
                    self.signals["scalarb"]
                ]
            ], [], 1))
    
    def get_minimum_clock_interval(self):
        # raise NotImplementedError
        return 7
    
        # for i in self.alu_operations

    def assemble_encoded_blueprint(self):
        self.blueprint = mb.Blueprint()
        
        alu = add_ALU_module(self.blueprint,
            [op.combinator_behaviors[0] for op in self.alu_operations],
        0, 0, self.get_minimum_clock_interval())

        # ROM
        rom = add_ROM_module(self.blueprint, -18, 0, 1, 1, self.rom_instructions)
        link_ALU_ROM(self.blueprint, alu, rom, 17)

        # RAM
        ram = add_RAM_module(self.blueprint, 18, 0, 1, 1)
        link_ALU_RAM(self.blueprint, alu, ram, 0)

        # link_ROM_RAM(blueprint, rom, ram, 103, 18)


        return self.blueprint.to_encoded()

    # class Signals:
    #     def __init__(self) -> None:
    #         self.registered_signals = {}

    #     def add_signal(self, name, signal):
    #         self.registered_signals[name] = signal
    #         return signal
        
    #     def init_metasignals(self):
    #         self.EACH_SIGNAL = self.add_signal("each", mb.Signal("signal-each", "virtual"))
    #         self.EVERYTHING_SIGNAL = self.add_signal("everything", mb.Signal("signal-everything", "virtual"))
    #         self.ANYTHING_SIGNAL = self.add_signal("anything", mb.Signal("signal-anything", "virtual"))

    #         # self.remaining_virtual_signals = []
    #         # self.remaining_virtual_signals.extend("0123456789ABCDEF")
    #         # self.remaining_virtual_signals.reverse()
    #         # self.remaining_virtual_signals = [mb.Signal("signal-"+i, "virtual") for i in remaining_virtual_signals]

    #         self.CLOCK_SIGNAL = self.add_signal("clock", mb.Signal("signal-T", "virtual"))
    #         self.PROGRAM_COUNTER_SIGNAL = self.add_signal("program_counter", mb.Signal("signal-I", "virtual"))
    #         self.OPCODE_SIGNAL = self.add_signal("opcode", mb.Signal("signal-O", "virtual"))

    #         self.WRITE_SIGNAL = self.add_signal("write", mb.Signal("signal-W", "virtual"))
    #         self.READA_SIGNAL = self.add_signal("reada", mb.Signal("signal-A", "virtual"))
    #         self.READB_SIGNAL = self.add_signal("readb", mb.Signal("signal-B", "virtual"))
    #         self.SCALARA_SIGNAL = self.add_signal("scalara", mb.Signal("signal-X", "virtual"))
    #         self.SCALARB_SIGNAL = self.add_signal("scalarb", mb.Signal("signal-Y", "virtual"))
    #         self.RAM_SIGNAL = self.add_signal("scalarb", mb.Signal("signal-Z", "virtual"))

    #         # self.WRITE_PROGRAM_COUNTER_SIGNAL = remaining_virtual_signals.pop()
    #         # self.CLEAR_MEMORY_SIGNAL = remaining_virtual_signals.pop()
    #         self.RESET_SIGNAL = self.add_signal("reset", mb.Signal("signal-R", "virtual"))

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

    combinators["reada"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READA_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    combinators["readb"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        READB_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    blueprint.add_connection("red", combinators["storage"], combinators["storage"], 2, 1)
    blueprint.add_connection("red", combinators["storage"], combinators["writer"], 1, 2)
    blueprint.add_connection("red", combinators["writer"], combinators["reada"], 2, 1)
    blueprint.add_connection("red", combinators["reada"], combinators["readb"], 1, 1)

    return combinators

def link_RAM_cells(blueprint, a, b):
    blueprint.add_connection("green", a["writer"], b["writer"], 1, 1)
    blueprint.add_connection("green", a["reada"], b["reada"], 1, 1)
    blueprint.add_connection("green", a["reada"], b["reada"], 2, 2)
    blueprint.add_connection("green", a["readb"], b["readb"], 1, 1)
    blueprint.add_connection("green", a["readb"], b["readb"], 2, 2)

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
    index = 1
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
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18, length, index+1, instructions[index:index+length]))
        if i > 0:
            link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += length

        # row 2
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+3, length, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += length

        # row 3a (before substation)
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+6, sublength, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-length])
        index += sublength

        # row 3b (after substation)
        cells.extend(add_ROM_submodule(blueprint, x+10, y+i*18+6, sublength, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-1])
        index += sublength

        # row 4a (before substation)
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+9, sublength, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-sublength*2])
        index += sublength

        # row 4b (after substation)
        cells.extend(add_ROM_submodule(blueprint, x+10, y+i*18+9, sublength, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-1])
        index += sublength

        # row 5
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+12, length, index+1, instructions[index:index+length]))
        link_ROM_cells(blueprint, cells[index], cells[index-sublength*2])
        index += length

        # row 6
        cells.extend(add_ROM_submodule(blueprint, x, y+i*18+15, length, index+1, instructions[index:index+length]))
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

def add_ROM_interface(blueprint, x, y):
    offset = 0
    combinators = {}


    # accumulator register
        # program counter

    combinators["accumulator_register"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset+1, mb.LogicCombinatorConditions(
        RESET_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        0,
        True
    )))
    blueprint.add_connection("green", combinators["accumulator_register"], combinators["accumulator_register"], 1, 2)
    offset += 2

    combinators["program_counter_increment"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        PROGRAM_COUNTER_SIGNAL,
        co.ADD,
        0
    )))
    offset += 1

    blueprint.add_connection("green", combinators["accumulator_register"], combinators["program_counter_increment"], 1, 2)


    return combinators

def add_clock(blueprint, x, y, clock_interval):
    offset = 0
    combinators = {}

    combinators["clock"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5+offset, y+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.EQUAL_TO,
        RAM_SIGNAL
    )))
    offset += 1

    combinators["modulus"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5+offset, y+1, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        CLOCK_SIGNAL,
        co.MOD,
        RAM_SIGNAL
    )))
    offset += 1

    combinators["constant"] = blueprint.add_entity(mb.ConstantCombinator(x+offset+0.5, y+0.5, mb.ConstantCombinatorConditions((
        (CLOCK_SIGNAL, 1),
        (RAM_SIGNAL, clock_interval)
    ))))
    offset += 1

    blueprint.add_connection("red", combinators["constant"], combinators["modulus"], 1, 2)
    blueprint.add_connection("red", combinators["modulus"], combinators["modulus"], 1, 2)
    blueprint.add_connection("red", combinators["modulus"], combinators["clock"], 1, 1)

    return combinators

def add_RAM_interface(blueprint, x, y):
    offset = 0
    combinators = {}


    # writing
    
    combinators["sender"] = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        CLOCK_SIGNAL,
        EVERYTHING_SIGNAL,
        co.EQUAL_TO,
        1,
        True
    )))
    offset += 2
    
    combinators["data_filter"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        RAM_SIGNAL,
        RAM_SIGNAL,
        co.ADD,
        0
    )))
    blueprint.add_connection("green", combinators["sender"], combinators["data_filter"], 1, 2)
    offset += 2
    
    combinators["write_filter"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        WRITE_SIGNAL,
        WRITE_SIGNAL,
        co.ADD,
        0
    )))
    blueprint.add_connection("green", combinators["sender"], combinators["write_filter"], 1, 2)
    offset += 2

    # blueprint.add_connection("green", combinators["data_filter"], combinators["write_filter"], 1, 1)


    # reading
    
    combinators["reada_filter"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        RAM_SIGNAL,
        SCALARA_SIGNAL,
        co.ADD,
        0
    )))
    offset += 2
    
    combinators["readb_filter"] = blueprint.add_entity(mb.ArithmeticCombinator(x+0.5, y+1+offset, mb.LogicCombinatorConditions(
        RAM_SIGNAL,
        SCALARB_SIGNAL,
        co.ADD,
        0
    )))
    offset += 2
    
    # blueprint.add_connection("green", combinators["write_filter"], combinators["reada_filter"], 1, 1)
    # blueprint.add_connection("green", combinators["reada_filter"], combinators["readb_filter"], 1, 1)
    
    blueprint.add_connection("green", combinators["write_filter"], combinators["reada_filter"], 1, 2)
    blueprint.add_connection("green", combinators["reada_filter"], combinators["readb_filter"], 2, 2)


    return combinators

def add_ALU_module(blueprint, opcodes, x, y, clock_interval):
    blocks = {}

    blocks["rom_interface"] = add_ROM_interface(blueprint, x, y)
    blocks["clock"] = add_clock(blueprint, x+7, y, clock_interval)
    blocks["ram_interface"] = add_RAM_interface(blueprint, x+17, y)

    blocks["operations"] = []
    for i, opcode in enumerate(opcodes):
        blocks["operations"].append(add_ALU_cells(blueprint, x+1+i, y+2, i+1, True, mb.LogicCombinatorConditions(*opcode)))
        if i > 0:
            link_ALU_cells(blueprint, blocks["operations"][-1], blocks["operations"][-2])
        
    blueprint.add_connection("green", blocks["ram_interface"]["data_filter"], blocks["operations"][10]["indexer"], 1, 2)
    blueprint.add_connection("green", blocks["ram_interface"]["write_filter"], blocks["operations"][10]["operator"], 1, 1)

    blueprint.add_connection("red", blocks["clock"]["clock"], blocks["rom_interface"]["program_counter_increment"], 2, 1)
    blueprint.add_connection("red", blocks["clock"]["clock"], blocks["ram_interface"]["sender"], 2, 1)

    blueprint.add_entity(mb.Substation(x+9, y+9))

    return blocks



def link_ALU_ROM(blueprint, alu, rom, rom_index):
    blueprint.add_connection("green", alu["rom_interface"]["accumulator_register"], rom[rom_index]["reader"], 1, 1)
    blueprint.add_connection("green", alu["operations"][0]["operator"], rom[rom_index]["reader"], 1, 2)
    blueprint.add_connection("green", alu["operations"][0]["indexer"], rom[rom_index]["reader"], 1, 2)

def link_ALU_RAM(blueprint, alu, ram, ram_index):
    blueprint.add_connection("green", alu["ram_interface"]["sender"], ram[ram_index]["writer"], 2, 1)
    blueprint.add_connection("green", alu["ram_interface"]["write_filter"], ram[ram_index]["reada"], 1, 1)
    blueprint.add_connection("green", alu["ram_interface"]["write_filter"], ram[ram_index]["readb"], 1, 1)
    blueprint.add_connection("green", alu["ram_interface"]["reada_filter"], ram[ram_index]["reada"], 1, 2)
    blueprint.add_connection("green", alu["ram_interface"]["readb_filter"], ram[ram_index]["readb"], 1, 2)

# def link_ROM_RAM(blueprint, rom, ram, rom_index, ram_index):
#     blueprint.add_connection("green", rom[rom_index]["reader"], ram[ram_index]["reada"], 2, 1)
#     blueprint.add_connection("green", ram[ram_index]["reada"], ram[ram_index]["readb"], 1, 1)





# connect rom output to ram input (reada readb)



def main(program_instructions):

    print("running main cpu program")

    blueprint = mb.Blueprint()

    clock_interval = 7
    
    # fails if under 6
    assert clock_interval >= 7

    # ALU
    opcodes = [
        [
            SCALARA_SIGNAL,
            RAM_SIGNAL,
            operation,
            SCALARB_SIGNAL
        ] for operation in co.arithmetic
    ]
    alu = add_ALU_module(blueprint, opcodes, 0, 0, clock_interval)

    # ROM
    rom = add_ROM_module(blueprint, -18, 0, 1, 1, program_instructions)
    link_ALU_ROM(blueprint, alu, rom, 17)

    # RAM
    ram = add_RAM_module(blueprint, 18, 0, 1, 1)
    link_ALU_RAM(blueprint, alu, ram, 0)

    # link_ROM_RAM(blueprint, rom, ram, 103, 18)


    encoded = blueprint.to_encoded()
    # print(encoded)
    with open("new_blueprint.txt", "w") as f:
        print(encoded, file=f)
    # input()

    print("finished")






if __name__ == "__main__":
    instructions = [
        # create_instruction(2, 1, 0, 0, 123, 456),
        # create_instruction(6, 5, 4, 3, 2, 1),
        
        # create_instruction(6, 0, 0, 0, 0, 0),
        # create_instruction(0, 5, 0, 0, 0, 0),
        # create_instruction(0, 0, 4, 0, 0, 0),
        # create_instruction(0, 0, 0, 3, 0, 0),
        # create_instruction(0, 0, 0, 0, 2, 0),
        # create_instruction(0, 0, 0, 0, 0, 1),
    ]




    # for i in range(10):
    #     for j in range(1, 11):
    #         instructions.append(create_instruction(3, j, 0, 0, i*10+j, 0))

    # for i in range(100):
    #     instructions.append(create_instruction(3, 1, 0, 0, 1, 0))



    #     create_instruction(1, 0, 0, 0, 1, 1),
    #     create_instruction(1, 1, 0, 0, 1, 1),
    # ]

    # a = 1
    # b = 1
    # for i in range(30):
    #     instructions.append(create_instruction(3, i+3, 0, 0, a, b))
    #     a, b = b, a+b

    instructions.append(create_instruction(3, 1, 0, 0, 1, 0))
    instructions.append(create_instruction(3, 2, 0, 0, 1, 0))
    # for j in range(300):
    #     i = 0
    #     instructions.append(create_instruction(3, i+3, i+2, i+1, 0, 0))
    for i in range(30):
        instructions.append(create_instruction(3, i+3, i+2, i+1, 0, 0))



    cpu = Combinator_CPU()
    cpu.init_basic_signals()
    cpu.init_basic_operations()

    for x in instructions:
        cpu.add_rom_instruction(x)

    encoded = cpu.assemble_encoded_blueprint()

    # print(encoded)
    with open("new_blueprint.txt", "w") as f:
        print(encoded, file=f)
    # input()

    print("Combinator_CPU assembled")



    # main(instructions)
