import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions (DOUBLED)
WIDTH, HEIGHT = 800, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone (Double Size)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 96)  # Double the font size too

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Bird setup (DOUBLED)
bird_x, bird_y = 200, 600
bird_width, bird_height = 60, 60
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Load bird image (scaled up)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # When running from EXE
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Then load the bird image like this:
bird_img = pygame.image.load(resource_path('BlappyFird.png'))
bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
message_timer = 0
show_pass_message = False

# Pipe setup (DOUBLED)
pipe_width = 120
pipe_gap = 300
pipes = []
pipe_timer = 0
scored_pipes = []

score = 0
game_over = False

def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def reset_game():
    global bird_y, bird_velocity, pipes, score, scored_pipes, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    scored_pipes.clear()
    score = 0
    game_over = False

# Main game loop
while True:
    clock.tick(60)  # 60 frames per second
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_velocity = jump_strength

    if not game_over:
        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_timer += 1
        if pipe_timer >= 90:
            pipe_timer = 0
            height = random.randint(200, 800)  # Adjusted for bigger height
            top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
            bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)
            scored_pipes.append(False)

        for pipe in pipes:
            pipe.x -= 6  # DOUBLE speed

        # Remove off-screen pipes and scores
        while pipes and pipes[0].x + pipe_width < 0:
            pipes.pop(0)
            pipes.pop(0)
            scored_pipes.pop(0)

        # Check collisions
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_over = True

        if bird_y + bird_height > HEIGHT or bird_y < 0:
            game_over = True

        # Update score
        for i in range(0, len(pipes), 2):
            pipe = pipes[i]
            if pipe.x + pipe_width < bird_x and not scored_pipes[i // 2]:
                score += 1
                scored_pipes[i // 2] = True
                show_pass_message = True
                message_timer = 60
                

    # Draw everything
    draw_bird()
    draw_pipes()

    # Display score
    score_surface = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_surface, (20, 20))

    # Display game over
    if game_over:
        game_over_surface = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

    # Display "Good Job!" message temporarily
    if show_pass_message:
        pass_message_surface = font.render("NICE!", True, (0, 0, 0))
        screen.blit(pass_message_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 300))
        message_timer -= 1
        if message_timer <= 0:
            show_pass_message = False


    pygame.display.flip()
