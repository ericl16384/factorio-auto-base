#x = 4
#y = 3
#maxSideLength = 4

#index = 0

#print(index)

## no negative
#index += x+maxSideLength/2

#print(index)

## make space
#index *= maxSideLength

#print(index)

## no negative
#index += y+maxSideLength/2

#print(index)

import math

def pack(x, y, maxSideLength, allowNegatives=True):
    # Init constants
    if allowNegatives:
        offset = maxSideLength//2
    else:
        offset = 0

    # Assertions
    assert allowNegatives or x >= 0 and y >= 0, "Negatives not allowed!"
    assert x >= -offset and x < maxSideLength-offset, [x, y]
    assert y >= -offset and y < maxSideLength-offset, [x, y]

    # Init out
    out = 0

    # Add x and offset, and then make space for y
    out += x
    out += offset
    out *= maxSideLength

    # Add y and offset
    out += y
    out += offset

    # Add 1, so that it can be indexed by circuit network
    out += 1

    # Return out
    return out

def unpack(i, maxSideLength, allowNegatives=True):
    # Init constants
    if allowNegatives:
        offset = maxSideLength//2
    else:
        offset = 0

    ## Assertions
    #assert allowNegatives or x >= 0 and y >= 0, "Negatives not allowed!"
    #assert x >= -offset and x < maxSideLength-offset, [x, y]
    #assert y >= -offset and y < maxSideLength-offset, [x, y]

    # Subtract 1
    i -= 1

    # Extract x and account for offset
    x = i // maxSideLength - offset

    # Extract y and account for offset
    y = i % maxSideLength - offset

    return [x, y]


tiles = set()
for y in range(-4, 4):
    for x in range(-4, 4):
        tile = pack(x, y, 8)
        assert tile not in tiles, [x, y]

        tiles.add(tile)
        print(f"{tile-1:06b}", x, y)

        assert unpack(tile, 8) == [x, y], [unpack(tile, 8), [x, y]]







#import math

##def tab(x, amount=4 -1):
##    x = str(x)
##    return x + " "*(amount-len(x))

##print(tab("i"), tab("r"), tab("o"))
##print()

##for i in range(1,  25  +1):
##    a = math.sqrt(i)
##    b = a - 1
##    c = b / 2
##    d = math.ceil(c)
##    #print(f"{i}  {a}  {b}  {c}  {d}")

##    #ring = math.ceil((math.sqrt(i) - 1) / 2)
##    ring = math.ceil((math.sqrt(i) - 1) / 2)
##    assert ring == d

##    offset = i - ring*8

##    print(tab(i), tab(ring), tab(offset))

#def tab(iterable, amount=4):
#    out = ""

#    for i in range(len(iterable)):
#        # Last item
#        if i == len(iterable) - 1:
#            return out + str(iterable[i])

#        length = len(str(iterable[i]))
#        out += str(iterable[i]) + " "*(amount-(length%amount))

#    return out

#print(tab([" x", " y", "r"]))
#print()

#for y in range(-1, 1+1):
#    for x in range(-1, 1+1):
#        out = [x, y]
#        if x >= 0:
#            out[0] = " "+str(x)
#        if y >= 0:
#            out[1] = " "+str(y)
        
#        out.append(max(abs(x), abs(y)))

#        if 

#        print(tab(out))
