all_previous = set()

MOVE_LOOKUP = ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1))

x = 0
y = 0

layer = 0
next_move = 0

for n in range(26):
    next_move_x, next_move_y = MOVE_LOOKUP[next_move]

    print(f"move={next_move}\t({next_move_x},\t{next_move_y})")

    x += next_move_x
    y += next_move_y

    print(f"node={n}\t({x},\t{y})\t{layer}")

    assert (x, y) not in all_previous
    all_previous.add((x, y))

    input()
    # print()


    # start
    if next_move == 0:
        next_move = 1
        layer += 1
        print(f"move switched: {next_move}")
    
    # new layer
    elif x == layer and y == -1:
        next_move = 5
        layer += 1
        print(f"move switched: {next_move}")
    
    # right side
    elif x == layer and next_move == 1 or next_move == 5:
        next_move = 2
        print(f"move switched: {next_move}")
    
    # top side
    elif y == layer and next_move == 2:
        next_move = 3
        print(f"move switched: {next_move}")
    
    # left side
    elif x == -layer and next_move == 3:
        next_move = 4
        print(f"move switched: {next_move}")
    
    # bottom side
    elif y == -layer and next_move == 4:
        next_move = 1
        print(f"move switched: {next_move}")

    