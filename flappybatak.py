import os
import random
import pygame

GAME_WIDTH = 360
GAME_HEIGHT = 640
FPS = 60

BIRD_X = GAME_WIDTH // 8
BIRD_Y = GAME_HEIGHT // 2
BIRD_WIDTH = 36
BIRD_HEIGHT = 33

PIPE_WIDTH = 64
PIPE_HEIGHT = 512
PIPE_SPEED = -3
GRAVITY = 0.4
JUMP_STRENGTH = -6
PIPE_EVENT = pygame.USEREVENT + 1
PIPE_INTERVAL = 1500
PIPE_GAP = GAME_HEIGHT // 4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Bird(pygame.Rect):
    def __init__(self, image: pygame.Surface) -> None:
        super().__init__(BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT)
        self.image = image


class Pipe(pygame.Rect):
    def __init__(self, image: pygame.Surface, x: int, y: int, is_top: bool) -> None:
        super().__init__(x, y, PIPE_WIDTH, PIPE_HEIGHT)
        self.image = image
        self.is_top = is_top
        self.passed = False


def load_image(filename: str, size: tuple[int, int]) -> pygame.Surface:
    path = os.path.join(BASE_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Flappy Batak")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Comic Sans MS", 36)
    small_font = pygame.font.SysFont("Comic Sans MS", 22)

    background_image = load_image("Background.jpg", (GAME_WIDTH, GAME_HEIGHT))
    bird_image = load_image("Batak.png.jpeg", (BIRD_WIDTH, BIRD_HEIGHT))
    top_pipe_image = load_image("toppipe.png.jpg", (PIPE_WIDTH, PIPE_HEIGHT))
    bottom_pipe_image = load_image("bottompipe.png.jpg", (PIPE_WIDTH, PIPE_HEIGHT))

    bird = Bird(bird_image)
    pipes: list[Pipe] = []
    velocity_y = 0.0
    score = 0
    game_over = False

    def reset_game() -> None:
        nonlocal velocity_y, score, game_over
        bird.x = BIRD_X
        bird.y = BIRD_Y
        velocity_y = 0.0
        pipes.clear()
        score = 0
        game_over = False

    def create_pipes() -> None:
        gap_top_min = 70
        gap_top_max = GAME_HEIGHT - PIPE_GAP - 70
        gap_top = random.randint(gap_top_min, gap_top_max)
        pipes.append(Pipe(top_pipe_image, GAME_WIDTH, gap_top - PIPE_HEIGHT, True))
        pipes.append(Pipe(bottom_pipe_image, GAME_WIDTH, gap_top + PIPE_GAP, False))

    pygame.time.set_timer(PIPE_EVENT, PIPE_INTERVAL)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PIPE_EVENT and not game_over:
                create_pipes()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    if game_over:
                        reset_game()
                    else:
                        velocity_y = JUMP_STRENGTH
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                velocity_y = JUMP_STRENGTH

        if not game_over:
            velocity_y += GRAVITY
            bird.y = int(bird.y + velocity_y)

            if bird.top < 0 or bird.bottom >= GAME_HEIGHT:
                game_over = True

            for pipe in pipes:
                pipe.x += PIPE_SPEED
                if pipe.is_top and not pipe.passed and bird.left > pipe.right:
                    score += 1
                    pipe.passed = True
                if bird.colliderect(pipe):
                    game_over = True

            pipes = [pipe for pipe in pipes if pipe.right > 0]

        screen.blit(background_image, (0, 0))
        for pipe in pipes:
            screen.blit(pipe.image, pipe)
        screen.blit(bird.image, bird)

        score_surface = font.render(str(score), True, "white")
        screen.blit(score_surface, (10, 5))

        if game_over:
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            title = font.render("Game Over", True, "white")
            final_score = small_font.render(f"Score: {score}", True, "white")
            restart = small_font.render("Press SPACE to restart", True, "white")
            screen.blit(title, title.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 45)))
            screen.blit(final_score, final_score.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2)))
            screen.blit(restart, restart.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 40)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.time.set_timer(PIPE_EVENT, 0)
    pygame.quit()


if __name__ == "__main__":
    main()
