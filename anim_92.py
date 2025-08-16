
import pygame
import numpy as np

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zeta Function Convergence Animation for k=11")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Data from Table 6
n_max = [337, 2191, 8881]
abs_s = [0.6078, 1.1178, 1.7148]
max_n = max(n_max)
max_s = max(abs_s)

# Scaling
x_scale = (WIDTH - 100) / max_n
y_scale = (HEIGHT - 100) / max_s
points = []
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
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)

    # Draw labels
    label_x = font.render("n_max", True, BLACK)
    screen.blit(label_x, (WIDTH-50, HEIGHT-30))
    label_y = font.render("|zeta_11(s)|", True, BLACK)
    screen.blit(label_y, (10, 10))

    # Animate points
    if current_point < len(n_max):
        points.append((50 + n_max[current_point] * x_scale, HEIGHT - 50 - abs_s[current_point] * y_scale))
        current_point += 1
        pygame.time.wait(1000)

    # Draw points and lines
    for i in range(len(points)-1):
        pygame.draw.line(screen, GREEN, points[i], points[i+1], 2)
    for point in points:
        pygame.draw.circle(screen, GREEN, (int(point[0]), int(point[1])), 5)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
input("Press Enter to close the animation...")
