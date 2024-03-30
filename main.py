import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
BALL_SIZE = 10
FPS = 60
FONT_SIZE = 30
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_SPACING = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ching-chong game")

# Load the font
font = pygame.font.Font(None, FONT_SIZE)

# Score class
class Score:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0

    def draw(self, surface):
        score_text = f"{self.score1}:{self.score2}"
        text_surface = font.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(text_surface, text_rect)

    def increase_score(self, player):
        if player == 1:
            self.score1 += 1
        elif player == 2:
            self.score2 += 1

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5

    def move(self, up=True):
        if up:
            self.rect.y = max(self.rect.y - self.speed, 0)  # Prevent going above the screen
        else:
            self.rect.y = min(self.rect.y + self.speed, SCREEN_HEIGHT - PADDLE_HEIGHT)  # Prevent going below the screen

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.velocity = pygame.math.Vector2(5, 5)

    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

    def bounce(self):
        self.velocity.x *= -1

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity.x *= -1  # Reverse the horizontal direction

# Button class
class Button:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        surface.blit(self.text, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Label:
    def __init__(self, text, y):
        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, y))

    def draw(self, surface):
        surface.blit(self.text, self.text_rect)
# Function to draw the game
def draw_game(surface, paddle1, paddle2, ball, score):
    surface.fill(BLACK)
    pygame.draw.aaline(surface, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    paddle1.draw(surface)
    paddle2.draw(surface)
    ball.draw(surface)
    score.draw(surface)
    pygame.display.flip()

# Function to draw the menu
def draw_menu(surface, buttons, label):
    surface.fill(BLACK)
    label.draw(surface)  # Draw the label
    for button in buttons:
        button.draw(surface)
    pygame.display.flip()

# Function to handle paddle movement
def handle_paddle_movement(keys, paddle1, paddle2):
    if keys[pygame.K_w]:
        paddle1.move(up=True)
    if keys[pygame.K_s]:
        paddle1.move(up=False)
    if keys[pygame.K_UP]:
        paddle2.move(up=True)
    if keys[pygame.K_DOWN]:
        paddle2.move(up=False)

# Function to handle ball collision with paddles and walls
def handle_collision(ball, paddle1, paddle2, score):
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.bounce()
    if ball.rect.left <= 0:
        score.increase_score(2)
        ball.reset()
    if ball.rect.right >= SCREEN_WIDTH:
        score.increase_score(1)
        ball.reset()
    if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
        ball.velocity.y *= -1

# Function to handle bot movement
def handle_bot_movement(paddle, ball):
    if ball.rect.y < paddle.rect.y + 10:
        paddle.move(up=True)
    elif ball.rect.y > paddle.rect.y - 20:
        paddle.move(up=False)

# Main game loop
# Main game loop
def main():
    clock = pygame.time.Clock()
    paddle1 = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)
    score = Score()
    buttons = [
        Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH - BUTTON_SPACING // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, "2 Player"),
        Button(SCREEN_WIDTH // 2 + BUTTON_SPACING // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, "Play vs Bot")
    ]
    label = Label("Ching-chong game!", 85)

    game_mode = None
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode is None:
                    # Check if a button was clicked
                    for i, button in enumerate(buttons):
                        if button.is_clicked(event.pos):
                            game_mode = i  # 0 for 2-player, 1 for bot

        if game_mode is None:
            # Draw the menu
            draw_menu(screen, buttons, label)
        else:
            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, paddle1, paddle2)

            if game_mode == 1:
                # Bot movement
                handle_bot_movement(paddle2, ball)

            ball.move()
            handle_collision(ball, paddle1, paddle2, score)

            draw_game(screen, paddle1, paddle2, ball, score)

    pygame.quit()

if __name__ == "__main__":
    main()