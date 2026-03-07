import pygame
import random

# --- Config ---
WIDTH = 1920
HEIGHT = 1080
FPS = 60

GRAVITY = 0.5
FLAP_STRENGTH = -8

PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3
PIPE_SPAWN_TIME = 1500  # ms

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (Simple)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# --- Bird ---
bird_rect = pygame.Rect(100, HEIGHT // 2, 30, 30)
bird_velocity = 0

# --- Pipes ---
pipes = []
last_pipe_spawn = pygame.time.get_ticks()

score = 0
alive = True


def spawn_pipe():
    gap_y = random.randint(150, HEIGHT - 150)

    top_pipe = pygame.Rect(
        WIDTH,
        0,
        PIPE_WIDTH,
        gap_y - PIPE_GAP // 2
    )

    bottom_pipe = pygame.Rect(
        WIDTH,
        gap_y + PIPE_GAP // 2,
        PIPE_WIDTH,
        HEIGHT
    )

    return top_pipe, bottom_pipe


def reset():
    global pipes, score, bird_velocity, alive
    pipes = []
    score = 0
    bird_rect.y = HEIGHT // 2
    bird_velocity = 0
    alive = True


# --- Game Loop ---
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if alive:
                    bird_velocity = FLAP_STRENGTH
                else:
                    reset()

    if alive:

        # Bird physics
        bird_velocity += GRAVITY
        bird_rect.y += bird_velocity

        # Spawn pipes
        now = pygame.time.get_ticks()
        if now - last_pipe_spawn > PIPE_SPAWN_TIME:
            pipes.extend(spawn_pipe())
            last_pipe_spawn = now

        # Move pipes
        for pipe in pipes:
            pipe.x -= PIPE_SPEED

        # Remove offscreen pipes
        pipes = [p for p in pipes if p.right > 0]

        # Collision
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                alive = False

        if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
            alive = False

        # Score (when passing pipes)
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx:
                score += 0.5

    # --- Draw ---
    screen.fill((135, 206, 235))

    pygame.draw.rect(screen, (255, 255, 0), bird_rect)

    for pipe in pipes:
        pygame.draw.rect(screen, (0, 200, 0), pipe)

    score_surface = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    if not alive:
        text = font.render("Game Over - SPACE to restart", True, (0, 0, 0))
        screen.blit(text, (40, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
