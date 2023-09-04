import generate_map, base_controller

BASE_START = (7, 7)

def reload():
    global map, base
    map = generate_map.Map()
    base = base_controller.Base(map, *BASE_START)
reload()


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
            dx = x * TILE_DISPLAY_SIZE + 50
            dy = y * TILE_DISPLAY_SIZE + 50
            tile_area = ((dx, dy), (TILE_DISPLAY_SIZE, TILE_DISPLAY_SIZE))

            t = map.get_tile(x, y)

            if t == map.NO_ORE:
                pygame.draw.rect(SCREEN, "green", tile_area)
            elif t == map.IRON_ORE:
                pygame.draw.rect(SCREEN, "blue", tile_area)
            elif t == map.COPPER_ORE:
                pygame.draw.rect(SCREEN, "orange", tile_area)
            else:
                pygame.draw.rect(SCREEN, "pink", tile_area)


            rail_width = int(TILE_DISPLAY_SIZE / 10)
            node_area = (
                (tile_area[0][0] + rail_width*2, tile_area[0][1] + rail_width*2),
                (TILE_DISPLAY_SIZE - rail_width*4, TILE_DISPLAY_SIZE - rail_width*4)
            )

            n = base.get_node(x, y)

            if n == base.UNTOUCHED:
                pass
            elif n == base.EMPTY:
                pygame.draw.rect(SCREEN, "dark grey", tile_area, rail_width)
            elif n == base.CONTROL_LOGIC:
                pygame.draw.rect(SCREEN, "red", node_area)
                pygame.draw.rect(SCREEN, "dark grey", tile_area, rail_width)

    pygame.display.flip()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reload()
            
            elif event.key == pygame.K_SPACE:
                base.next()