import pygame
import random
import math
import heapq

pygame.init()
map_width = 300
map_height = 300
num_obstacles = 10
grid_size = 10
obstacles = []
map_color = (255, 255, 255)
obstacle_color = (0, 0, 0)
grid_color = (125, 125, 125)
display_surface = pygame.display.set_mode((map_width, map_height))

robot_size = 20
robot_radius = robot_size
robot_space = []
for x in range(-robot_size, robot_size + grid_size, grid_size):
   for y in range(-robot_size, robot_size + grid_size, grid_size):
       if math.sqrt(x ** 2 + y ** 2) <= robot_radius:
           robot_space.append((x, y))

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
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, end):
    open_set = {start}
    closed_set = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = min(open_set, key=f_score.get)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        open_set.remove(current)
        closed_set.add(current)

        for dx, dy in [(0, grid_size), (0, -grid_size), (grid_size, 0), (-grid_size, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor[0] < 0 or neighbor[0] >= map_width or neighbor[1] < 0 or neighbor[1] >= map_height:
                continue
            if is_point_in_robot_space(neighbor):
                continue
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + math.sqrt(dx ** 2 + dy ** 2)

            if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None
def is_point_in_robot_space(point):
   for x, y in robot_space:
       if is_point_in_obstacle((point[0] + x, point[1] + y)):
           return True
   return False

def discretize_point(point):
   x = int(round(point[0] / grid_size)) * grid_size
   y = int(round(point[1] / grid_size)) * grid_size
   return (x, y)


def draw_map():

   display_surface.fill(map_color)


   for obstacle in obstacles:
       pygame.draw.rect(display_surface, obstacle_color, obstacle)


   for x in range(0, map_width, grid_size):
       pygame.draw.line(display_surface, grid_color, (x, 0), (x, map_height))
   for y in range(0, map_height, grid_size):
       pygame.draw.line(display_surface, grid_color, (0, y), (map_width, y))


   config_space_color = (200, 200, 200)
   for x in range(0, map_width, grid_size):
       for y in range(0, map_height, grid_size):
           point = (x, y)
           if is_point_in_obstacle(point):
               continue
           in_config_space = True
           for dx, dy in robot_space:
               if is_point_in_obstacle((x + dx, y + dy)):
                   in_config_space = False
                   break
           if in_config_space:
               pygame.draw.rect(display_surface, config_space_color, (x, y, grid_size, grid_size))


   pygame.display.update()
while True:
    start = input("Enter the starting point of the robot (in x,y format): ")
    end = input("Enter the ending point of the robot (in x,y format): ")
    if start.lower() == 'exit' or end.lower() == 'exit':
        break
    try:
        start = tuple(map(int, start.split(",")))
        end = tuple(map(int, end.split(",")))
        if start[0] < 0 or start[0] >= map_width or start[1] < 0 or start[1] >= map_height:
            raise ValueError("Starting point is outside the map")
        if end[0] < 0 or end[0] >= map_width or end[1] < 0 or end[1] >= map_height:
            raise ValueError("Ending point is outside the map")

        pygame.draw.circle(display_surface, (255, 0, 0), start, 5)
        pygame.draw.circle(display_surface, (0, 255, 0), end, 5)
        config_space_color = (200, 200, 200)
        for x in range(0, map_width, grid_size):
            for y in range(0, map_height, grid_size):
                point = (x, y)
                if is_point_in_obstacle(point):
                    continue
                robot_radius = 20
                in_config_space = True
                for dx in range(-robot_radius, robot_radius + 1):
                    for dy in range(-robot_radius, robot_radius + 1):
                        if is_point_in_obstacle((x + dx, y + dy)):
                            in_config_space = False
                            break
                    if not in_config_space:
                        break
                if in_config_space:
                    pygame.draw.rect(display_surface, config_space_color, (x, y, grid_size, grid_size))

        start_disc = discretize_point(start)
        end_disc = discretize_point(end)
        pygame.draw.circle(display_surface, (255, 0, 0), start_disc, 5)
        pygame.draw.circle(display_surface, (0, 255, 0), end_disc, 5)

        path = a_star(start_disc, end_disc)
        if path is not None:
            for i in range(len(path) - 1):
                pygame.draw.line(display_surface, (0, 0, 255), path[i], path[i + 1], 2)
            pygame.display.update()
        else:
            print("No path found")
    except Exception as e:
        print("Error:", e)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    else:
        continue
    break