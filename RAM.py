import combinator_operations as co
import make_blueprint as mb




def add_memory_cell(blueprint, x, y, index):
    offset = 0

    storage = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset, mb.LogicCombinatorConditions(
        mb.Signal("signal-check", "virtual"),
        mb.Signal("signal-everything", "virtual"),
        co.EQUAL_TO,
        0,
        True
    )))
    offset += 2

    writer = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset, mb.LogicCombinatorConditions(
        mb.Signal("signal-info", "virtual"),
        mb.Signal("signal-everything", "virtual"),
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    reader_a = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset, mb.LogicCombinatorConditions(
        mb.Signal("signal-info", "virtual"),
        mb.Signal("signal-everything", "virtual"),
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    reader_b = blueprint.add_entity(mb.DeciderCombinator(x+0.5, y+offset, mb.LogicCombinatorConditions(
        mb.Signal("signal-info", "virtual"),
        mb.Signal("signal-everything", "virtual"),
        co.EQUAL_TO,
        index,
        True
    )))
    offset += 2

    blueprint.add_connection("red", storage, storage, 2, 1)
    blueprint.add_connection("red", storage, writer, 1, 2)
    blueprint.add_connection("red", writer, reader_a, 2, 1)
    blueprint.add_connection("red", reader_a, reader_b, 1, 1)

    return storage, writer, reader_a, reader_b

def link_memory_cells(blueprint, a, b):
    blueprint.add_connection("green", a[1], b[1], 1, 1)
    blueprint.add_connection("green", a[2], b[2], 1, 1)
    blueprint.add_connection("green", a[2], b[2], 2, 2)
    blueprint.add_connection("green", a[3], b[3], 1, 1)
    blueprint.add_connection("green", a[3], b[3], 2, 2)

def add_memory_block(blueprint, x, y, length, starting_index):
    cells = []
    for i in range(length):
        cells.append(add_memory_cell(blueprint, x+i, y, i+starting_index))

        if i > 0:
            link_memory_cells(blueprint, cells[-1], cells[-2])
    return cells

def add_folded_memory_block(blueprint, x, y, length, layers, layer_spacing, starting_offset):
    blocks = []
    for i in range(layers):
        blocks.append(add_memory_block(blueprint, x, y+i*(8+layer_spacing), length, i*length+starting_offset))

        if i > 0:
            link_memory_cells(blueprint, blocks[-1][0], blocks[-2][0])
    return blocks

def add_memory_module(blueprint, x, y, width, height):
    length = 18*width

    blocks = []
    index = 0
    for i in range(height):
        blocks.append(add_memory_block(blueprint, x, y+i*18, length, index))
        index += length

        if i > 0:
            link_memory_cells(blueprint, blocks[-1][0], blocks[-2][0])
        
        for j in range(width):
            blueprint.add_entity(mb.Substation(x+9+j*18, y+8+i*18))

        blocks.append(add_memory_block(blueprint, x, y+i*18+10, length, index))
        index += length

        link_memory_cells(blueprint, blocks[-1][0], blocks[-2][0])
    
    return blocks


if __name__ == "__main__":

    blueprint = mb.Blueprint()


    # add_memory_block(blueprint, 0, 0, 16, 0)
    # add_memory_block(blueprint, 0, 8, 16, 16)

    # add_folded_memory_block(blueprint, 0, 0, 36, 2, 0, 0)
    # add_folded_memory_block(blueprint, 40, 0, 36, 2, 1, 0)
    # add_folded_memory_block(blueprint, 80, 0, 36, 2, 2, 0)
    # add_folded_memory_block(blueprint, 120, 0, 36, 2, 3, 0)
    # add_folded_memory_block(blueprint, 160, 0, 36, 2, 4, 0)

    add_memory_module(blueprint, 0, 0, 4, 2)


    encoded = blueprint.to_encoded()
    print(encoded)
    with open("new_blueprint.txt", "w") as f:
        print(encoded, file=f)
    input()
