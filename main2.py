import pygame
import random

pygame.init()
map_width = 300
map_height = 300
num_obstacles = 10
grid_size = 10
obstacles = []
map_color = (255, 255, 255)
obstacle_color = (0, 0, 0)
grid_color = (200, 200, 200)
display_surface = pygame.display.set_mode((map_width, map_height))

for i in range(num_obstacles):
    obstacle_x = random.randint(0, map_width)
    obstacle_y = random.randint(0, map_height)
    obstacle_width = random.randint(10, 50)
    obstacle_height = random.randint(10, 50)
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

def is_point_in_obstacle(point):
    for obstacle in obstacles:
        if obstacle.collidepoint(point):
            return True
    return False

def discretize_point(point):
    x = int(round(point[0] / grid_size)) * grid_size
    y = int(round(point[1] / grid_size)) * grid_size
    return (x, y)

running = True


while True:
    start = input("Enter the starting point of the robot (in x,y format): ")
    end = input("Enter the ending point of the robot (in x,y format): ")
    try:
        start = tuple(map(int, start.split(",")))
        end = tuple(map(int, end.split(",")))
        if start[0] < 0 or start[0] >= map_width or start[1] < 0 or start[1] >= map_height:
            raise ValueError("Starting point is outside the map")
        if end[0] < 0 or end[0] >= map_width or end[1] < 0 or end[1] >= map_height:
            raise ValueError("Ending point is outside the map")
        if is_point_in_obstacle(start):
            raise ValueError("Starting point is inside an obstacle")
        if is_point_in_obstacle(end):
            raise ValueError("Ending point is inside an obstacle")
        break
    except ValueError as e:
        print("Error: ", str(e))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            sample_point = pygame.mouse.get_pos()
            discretized_point = discretize_point(sample_point)
            if is_point_in_obstacle(discretized_point):
                print("Sampled point is inside an obstacle!")
            else:
                print("Sampled point is not inside an obstacle.")
                print("Discretized point:", discretized_point)

    display_surface.fill(map_color)

    for x in range(0, map_width, grid_size):
        pygame.draw.line(display_surface, grid_color, (x, 0), (x, map_height))
    for y in range(0, map_height, grid_size):
        pygame.draw.line(display_surface, grid_color, (0, y), (map_width, y))

    for obstacle in obstacles:
        pygame.draw.rect(display_surface, obstacle_color, obstacle)

    pygame.draw.circle(display_surface, (255, 0, 0), start, 5)
    pygame.draw.circle(display_surface, (0, 255, 0), end, 5)

    pygame.display.update()

pygame.quit()