
import pygame
import numpy as np

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prime Counts Animation for k=11, k=17")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Data from Table 5
n_max = [337, 2191, 8881]
actual_k11 = [139, 743, 2677]
actual_k17 = [137, 738, 2668]
max_n = max(n_max)
max_count = max(max(actual_k11), max(actual_k17))

# Scaling
x_scale = (WIDTH - 100) / max_n
y_scale = (HEIGHT - 100) / max_count
points_k11 = []
points_k17 = []
current_point = 0

# Font
font = pygame.font.SysFont('arial', 20)

# Animation loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False

    screen.fill(WHITE)

    # Draw axes
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

    # Draw labels
    label_x = font.render("n_max", True, BLACK)
    screen.blit(label_x, (WIDTH-50, HEIGHT-30))
    label_y = font.render("Prime Counts", True, BLACK)
    screen.blit(label_y, (10, 10))

    # Animate points
    if current_point < len(n_max):
        points_k11.append((50 + n_max[current_point] * x_scale, HEIGHT - 50 - actual_k11[current_point] * y_scale))
        points_k17.append((50 + n_max[current_point] * x_scale, HEIGHT - 50 - actual_k17[current_point] * y_scale))
        current_point += 1
        pygame.time.wait(1000)

    # Draw points and lines
    for i in range(len(points_k11)-1):
        pygame.draw.line(screen, BLUE, points_k11[i], points_k11[i+1], 2)
        pygame.draw.line(screen, RED, points_k17[i], points_k17[i+1], 2)
    for point in points_k11:
        pygame.draw.circle(screen, BLUE, (int(point[0]), int(point[1])), 5)
    for point in points_k17:
        pygame.draw.circle(screen, RED, (int(point[0]), int(point[1])), 5)

    # Draw legend
    pygame.draw.line(screen, BLUE, (600, 50), (650, 50), 2)
    pygame.draw.line(screen, RED, (600, 80), (650, 80), 2)
    screen.blit(font.render("k=11", True, BLACK), (660, 45))
    screen.blit(font.render("k=17", True, BLACK), (660, 75))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
input("Press Enter to close the animation...")
