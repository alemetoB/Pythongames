import os
import sys
import random

try:
    import pygame
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Pygame is not installed. Run: py -3.13 -m pip install pygame\n"
        "Then start the game again."
    ) from exc


# make asset paths work even when running from a different cwd
BASE_DIR = os.path.dirname(__file__)

def asset_path(filename: str) -> str:
    candidates = [
        os.path.join(BASE_DIR, filename),
    ]

    if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
        base, ext = os.path.splitext(filename)
        alt_name = f"{base} (3){ext}"
        candidates.append(os.path.join(BASE_DIR, alt_name))

    for path in candidates:
        if os.path.exists(path):
            return path

    return candidates[0]

#create the window
pygame.init()
screen = pygame.display.set_mode((800, 600))

#Title icon
pygame.display.set_caption('Space Wars')

def load_image(filename: str, *, size=None, fallback_color=(0, 0, 0)) -> pygame.Surface:
    """Load an image from the assets folder, or return a solid surface if missing."""
    path = asset_path(filename)
    if not os.path.exists(path):
        print(f"WARNING: asset not found: {path}")
        surf = pygame.Surface(size if size else (64, 64))
        surf.fill(fallback_color)
        return surf

    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    return img

icon = load_image('space-shuttle.png', size=(32, 32), fallback_color=(255, 0, 0))
pygame.display.set_icon(icon)

#Background image
background = load_image('download.jpg', size=(800, 600), fallback_color=(0, 0, 64))
# If the file name differs on disk (like "download (3).jpg"), asset_path() will find it automatically.

#player 1
playerImg = load_image('craft.png', size=(64, 64), fallback_color=(0, 255, 0))
playerX = 480
playerY = 480
playerX_change = 0  # track horizontal movement
player_speed = 8  # pixels per frame

#Enemy
EnemyImg = load_image('spaceship.png', size=(64, 64), fallback_color=(255, 0, 255))
ENEMY_COUNT = 5
ENEMY_SPEED = 8  # pixels per frame

def spawn_enemy():
    return {
        'x': random.randint(0, 800 - EnemyImg.get_width()),
        'y': random.randint(50, 150),
        'dx': ENEMY_SPEED if random.choice([True, False]) else -ENEMY_SPEED,
    }

# start with a few enemies
enemies = [spawn_enemy() for _ in range(ENEMY_COUNT)]

# after all enemies are destroyed, wait 5 seconds before respawning
respawn_time = None

#Bullet
BulletImg = load_image('bullet.png', size=(32, 32), fallback_color=(255, 255, 255))
Bullet_speed = 15  # pixels per frame
bullets = []  # list of (x, y) tuples for active bullets

# scoring
score = 0
high_score = 0

game_state = 'menu'  # 'menu' or 'playing'

# font for text rendering
font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 56)

# control the frame rate
clock = pygame.time.Clock()

def player(x,y):
    screen.blit(playerImg, (x, y))
    
def Enemy(x, y):
    screen.blit(EnemyImg, (x, y))
    
def fire_bullet(x, y):
    # create a new bullet at the player's position
    bullets.append([x + 16, y + 10])
def isCollision(EnemyX, EnemyY, bulletX, bulletY):
    distance = ((EnemyX - bulletX) ** 2 + (EnemyY - bulletY) ** 2) ** 0.5
    return distance < 27


def show_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font.render(f"High: {high_score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 40))


def draw_menu():
    title = menu_font.render("Space Wars", True, (255, 255, 255))
    start = font.render("Press ENTER to start", True, (255, 255, 255))
    quit_text = font.render("Press Q to quit", True, (255, 255, 255))

    title_rect = title.get_rect(center=(400, 180))
    start_rect = start.get_rect(center=(400, 260))
    quit_rect = quit_text.get_rect(center=(400, 300))

    screen.blit(title, title_rect)
    screen.blit(start, start_rect)
    screen.blit(quit_text, quit_rect)


def reset_game():
    global score, bullets, enemies, respawn_time, playerX, playerX_change

    score = 0
    bullets = []
    enemies = [spawn_enemy() for _ in range(ENEMY_COUNT)]
    respawn_time = None
    playerX = 480
    playerX_change = 0

#Game loop
running = True
while running:
    # limit the frame rate for consistent movement speed
    clock.tick(60)

    #RGB
    screen.fill((0, 0, 255))
    #background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 'menu':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = 'playing'
                if event.key == pygame.K_q:
                    running = False
        elif game_state == 'playing':
            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    playerX_change = player_speed
                if event.key == pygame.K_SPACE:
                    fire_bullet(playerX, playerY)
                if event.key == pygame.K_ESCAPE:
                    # return to menu
                    game_state = 'menu'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # enemy movement
        for enemy in enemies:
            enemy['x'] += enemy['dx']
            if enemy['x'] <= 0:
                enemy['x'] = 0
                enemy['dx'] = ENEMY_SPEED
            elif enemy['x'] >= 800 - EnemyImg.get_width():
                enemy['x'] = 800 - EnemyImg.get_width()
                enemy['dx'] = -ENEMY_SPEED

        # keep player inside the screen
        playerX = max(0, min(playerX, 800 - playerImg.get_width()))

        # bullet movement (rapid fire)
        for bullet in bullets[:]:
            bullet[1] -= Bullet_speed
            screen.blit(BulletImg, (bullet[0], bullet[1]))

            # check for collision with any enemy
            for enemy in enemies[:]:
                if isCollision(enemy['x'], enemy['y'], bullet[0], bullet[1]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    if score > high_score:
                        high_score = score
                    break

            # remove bullets that fly off-screen
            if bullet in bullets and bullet[1] <= 0:
                bullets.remove(bullet)

        # if all enemies are dead, start respawn timer
        if not enemies and respawn_time is None:
            respawn_time = pygame.time.get_ticks() + 5000

        # respawn enemies after delay
        if respawn_time is not None and pygame.time.get_ticks() >= respawn_time:
            enemies = [spawn_enemy() for _ in range(ENEMY_COUNT)]
            respawn_time = None

        player(playerX, playerY)

        # draw enemies
        for enemy in enemies:
            Enemy(enemy['x'], enemy['y'])

        show_score()

    pygame.display.update()
    





