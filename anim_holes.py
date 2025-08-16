
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prime Distribution Across Residue Classes")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

coprime_24 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 1]
prime_counts = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
max_count = max(prime_counts)

bar_width = (WIDTH - 100) / len(coprime_24)
y_scale = (HEIGHT - 100) / max_count
current_bars = [0] * len(coprime_24)

font = pygame.font.SysFont('arial', 20)

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

    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

    label_x = font.render("Residue Class k", True, BLACK)
    screen.blit(label_x, (WIDTH-100, HEIGHT-30))
    label_y = font.render("Prime Count", True, BLACK)
    screen.blit(label_y, (10, 10))

    for i in range(len(coprime_24)):
        if current_bars[i] < prime_counts[i]:
            current_bars[i] += max(1, prime_counts[i] // 50)
            if current_bars[i] > prime_counts[i]:
                current_bars[i] = prime_counts[i]

        height = current_bars[i] * y_scale
        pygame.draw.rect(screen, BLUE, (50 + i * bar_width, HEIGHT - 50 - height, bar_width - 2, height))
        label = font.render(str(coprime_24[i]), True, BLACK)
        screen.blit(label, (50 + i * bar_width + bar_width/4, HEIGHT-30))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
input("Press Enter to close the animation...")
