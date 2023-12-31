# all_previous = set()

# MOVE_LOOKUP = ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1))

def get_next_move_generator():
    def g():
        node = 0

        x = 0
        y = 0
        layer = 0

        next_move_x = 0
        next_move_y = 0
        new_layer = 0

        while True:
            # print(f"move=\t({next_move_x},\t{next_move_y})")

            # print(f"node={n}\t({x},\t{y})\t{layer}")
            # yield (next_move_x, next_move_y)


            # assert (x, y) not in all_previous
            # all_previous.add((x, y))


            # input()
            # print()


            # new layer
            if new_layer:
                next_move_y -= next_move_y
                new_layer -= new_layer


            # right side
            if x == layer and next_move_x > 0:
                next_move_x -= 1
                next_move_y += 1
                # print(f"move switched")
            
            # top side
            if y == layer and next_move_y > 0:
                next_move_x -= 1
                next_move_y -= 1
                # print(f"move switched")
            
            # left side
            if x == -layer and next_move_x < 0:
                next_move_x += 1
                next_move_y -= 1
                # print(f"move switched")
            
            # bottom side
            if y == -layer and next_move_y < 0:
                next_move_x += 1
                next_move_y += 1
                # print(f"move switched")


            # start
            if next_move_x == 0 and next_move_y == 0:
                new_layer += 1
            
            # new layer
            if x == layer and y == -1:
                new_layer += 1
            
            if new_layer:
                next_move_x -= next_move_x
                next_move_y -= next_move_y
                layer += 1
                next_move_x = layer - x
                next_move_y = -y
            
            
            yield (node, (x, y))

            x += next_move_x
            y += next_move_y

            node += 1
    
    return g
            
next_move = get_next_move_generator()

for n, pos in next_move():
    print(n)
    print(pos)
    input()
    