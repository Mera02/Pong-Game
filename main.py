import pygame
import sys
import random

# Inicijalizacija Pygame-a
pygame.init()

# Dimenzije prozora
WIDTH, HEIGHT = 800, 600

# Boje
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GLOW_COLOR = (200, 200, 0)

# Kreiranje prozora
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Clock za kontrolu FPS-a
clock = pygame.time.Clock()
FPS = 60

# Fontovi
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)

# Dimenzije elemenata
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 5

# Postavke za težinu
AI_SPEEDS = {"easy": 3, "medium": 4, "hard": 6}
AI_ERROR_MARGINS = {"easy": 50, "medium": 30, "hard": 10}

# Početna težina (podrazumevano medium)
difficulty = "medium"

# Faktor ubrzanja loptice
ball_speed_increment = 0.1

# Poeni
player1_score = 0
player2_score = 0
WINNING_SCORE = 3

# Glow efekti
left_paddle_glow = 0
right_paddle_glow = 0

# Inicijalizacija muzike
pygame.mixer.init()
pygame.mixer.music.load("assets/background_music.mp3")  # Ubaci svoj fajl ovde
pygame.mixer.music.set_volume(0.1)  # Postavi glasnoću (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Reprodukuje muziku u petlji

# Početni ekran
def show_home_screen():
    global difficulty, player1_score, player2_score
    player1_score = 0
    player2_score = 0
    difficulty = "medium"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Naslov
        title_text = font_large.render("Pong", True, WHITE)
        by_text = font_small.render("by Mera", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(by_text, (WIDTH // 2 - by_text.get_width() // 2, 180))

        # Opcije za težinu (prikaz koji je trenutno selektovan)
        easy_color = WHITE if difficulty == "easy" else (150, 150, 150)
        medium_color = WHITE if difficulty == "medium" else (150, 150, 150)
        hard_color = WHITE if difficulty == "hard" else (150, 150, 150)

        easy_text = font_medium.render("Easy", True, easy_color)
        medium_text = font_medium.render("Medium", True, medium_color)
        hard_text = font_medium.render("Hard", True, hard_color)
        start_text = font_medium.render("Start Game", True, WHITE)

        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 250))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 320))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 390))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 460))

        # Detekcija klika miša
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 250 <= mouse[1] <= 250 + easy_text.get_height() and click[0]:
            difficulty = "easy"
        if 320 <= mouse[1] <= 320 + medium_text.get_height() and click[0]:
            difficulty = "medium"
        if 390 <= mouse[1] <= 390 + hard_text.get_height() and click[0]:
            difficulty = "hard"
        if 460 <= mouse[1] <= 460 + start_text.get_height() and click[0]:
            return difficulty

        pygame.display.flip()
        clock.tick(FPS)

# Prikaz ekrana za pobedu ili poraz
def show_end_screen(message):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Poruka
        end_text = font_large.render(message, True, WHITE)
        home_text = font_medium.render("Go to Home Page", True, WHITE)

        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 250))
        screen.blit(home_text, (WIDTH // 2 - home_text.get_width() // 2, 350))

        # Detekcija klika miša
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 350 <= mouse[1] <= 350 + home_text.get_height() and click[0]:
            show_home_screen()
            return

        pygame.display.flip()
        clock.tick(FPS)

# Dimenzije palica i loptice
left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Brzina loptice
ball_speed_x = 4
ball_speed_y = 4

# Početna težina i AI postavke
difficulty = show_home_screen()
ai_speed = AI_SPEEDS[difficulty]
ai_error_margin = AI_ERROR_MARGINS[difficulty]

# Glavna petlja igre
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Kontrola muzike (mute/unmute)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    # Kontrole za levu palicu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # AI logika za desnu palicu
    target_y = ball.centery + random.randint(-ai_error_margin, ai_error_margin)
    if target_y < right_paddle.centery and right_paddle.top > 0:
        right_paddle.y -= ai_speed
    if target_y > right_paddle.centery and right_paddle.bottom < HEIGHT:
        right_paddle.y += ai_speed

    # Pomicanje loptice
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Sudar loptice sa zidovima
    if ball.top <= 0:
        ball.top = 0
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_speed_y *= -1

    # Sudar loptice sa palicama
    if ball.colliderect(left_paddle):
        ball.left = left_paddle.right
        ball_speed_x *= -1
        ball_speed_x += ball_speed_increment if ball_speed_x > 0 else -ball_speed_increment
        ball_speed_y += ball_speed_increment if ball_speed_y > 0 else -ball_speed_increment
        left_paddle_glow = 5  # Aktiviraj glow efekat
    if ball.colliderect(right_paddle):
        ball.right = right_paddle.left
        ball_speed_x *= -1
        ball_speed_x += ball_speed_increment if ball_speed_x > 0 else -ball_speed_increment
        ball_speed_y += ball_speed_increment if ball_speed_y > 0 else -ball_speed_increment
        right_paddle_glow = 5  # Aktiviraj glow efekat

    # Resetovanje pozicije loptice ako neko osvoji poen
    if ball.left <= 0:
        player2_score += 1
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x = 4 * (1 if ball_speed_x > 0 else -1)
        ball_speed_y = 4 * (1 if ball_speed_y > 0 else -1)
    if ball.right >= WIDTH:
        player1_score += 1
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x = 4 * (1 if ball_speed_x > 0 else -1)
        ball_speed_y = 4 * (1 if ball_speed_y > 0 else -1)

    # Provera za pobedu
    if player1_score >= WINNING_SCORE:
        show_end_screen("You won!")
    if player2_score >= WINNING_SCORE:
        show_end_screen("Los si jarane!")

    # Popunjavanje pozadine
    screen.fill(BLACK)

    # Crtanje elemenata sa glow efektom
    if left_paddle_glow > 0:
        pygame.draw.rect(screen, GLOW_COLOR, left_paddle)
        left_paddle_glow -= 1
    else:
        pygame.draw.rect(screen, WHITE, left_paddle)

    if right_paddle_glow > 0:
        pygame.draw.rect(screen, GLOW_COLOR, right_paddle)
        right_paddle_glow -= 1
    else:
        pygame.draw.rect(screen, WHITE, right_paddle)

    pygame.draw.ellipse(screen, WHITE, ball)

    # Prikaz rezultata
    player1_text = font_small.render(f"Player 1: {player1_score}", True, WHITE)
    player2_text = font_small.render(f"Player 2: {player2_score}", True, WHITE)
    screen.blit(player1_text, (50, 10))
    screen.blit(player2_text, (WIDTH - player2_text.get_width() - 50, 10))

    # Ažuriranje prozora
    pygame.display.flip()

    # Kontrola brzine igre
    clock.tick(FPS)

# Zatvaranje Pygame-a
pygame.quit()
sys.exit()
