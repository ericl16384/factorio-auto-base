import generate_map, base_controller

def reload():
    global map
    map = generate_map.Map()
reload()

# print(map.lookup)
# map.get_tile(0, 0)

# print(map.lookup)
# map.get_tile(10, 10)

# print(map.lookup)

MAP_SIZE = (15, 15)
TILE_DISPLAY_SIZE = 40






import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
pygame.display.set_caption("main.py")
CLOCK = pygame.time.Clock()


while pygame.get_init():
    CLOCK.tick(60)


    SCREEN.fill("black")

    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            t = map.get_tile(x, y)

            if t == map.NO_ORE:
                c = "green"
            elif t == map.IRON_ORE:
                c = "blue"
            elif t == map.COPPER_ORE:
                c = "orange"
            else:
                c = "pink"

            dx = x * TILE_DISPLAY_SIZE + 50
            dy = y * TILE_DISPLAY_SIZE + 50
            
            pygame.draw.rect(SCREEN, c, ((dx, dy), (TILE_DISPLAY_SIZE,TILE_DISPLAY_SIZE)))

    pygame.display.flip()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reload()