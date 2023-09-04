import pygame





import generate_map

game_map = generate_map.Map()

print(game_map.lookup)
game_map.get_tile(0, 0)

print(game_map.lookup)
game_map.get_tile(10, 10)

print(game_map.lookup)





input()




screen = pygame.display.set_mode((1500, 750))

pygame.display.set_caption("main.py")

clock = pygame.time.Clock()

while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill("black")

    pygame.display.flip()


pygame.quit()