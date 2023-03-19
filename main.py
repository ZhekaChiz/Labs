import pygame
import random

pygame.init()
map_width = 300
map_height = 300
num_obstacles = 10
obstacles = []
map_color = (255, 255, 255)
obstacle_color = (0, 0, 0)
display_surface = pygame.display.set_mode((map_width, map_height))
for i in range(num_obstacles):
    obstacle_x = random.randint(0, map_width)
    obstacle_y = random.randint(0, map_height)
    obstacle_width = random.randint(10, 50)
    obstacle_height = random.randint(10, 50)
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill(map_color)

    for obstacle in obstacles:
        pygame.draw.rect(display_surface, obstacle_color, obstacle)

    pygame.display.update()

pygame.quit()
