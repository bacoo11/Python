import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
INITIAL_SPAWN_INTERVAL = 15000
ENEMIES_PER_LEVEL = 10
INITIAL_ENEMY_SIZE = 64
INITIAL_ENEMY_SPEED = 1
PLAYER_SPEED = 4
MAX_HEALTH = 5


background = pygame.image.load(r"Background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load(r"Necromancer.png")
player_img = pygame.transform.scale(player_img, (80, 80))
attack_img = pygame.image.load(r"Attack.png")
attack_img = pygame.transform.scale(attack_img, (40, 40))
music = r"Background Music.mp3"
intro_img = pygame.image.load(r"Intro.png")
intro_img = pygame.transform.scale(intro_img, (1200, 100))
lose_img = pygame.image.load(r"Lose.png")
win_img = pygame.image.load(r"Win.png")


enemy_images = {i: pygame.image.load(fr"Level{i}.png") for i in range(1, 11)}


level_img = pygame.image.load(r"Level.png")
level_img = pygame.transform.scale(level_img, (120, 32))
demons_killed_img = pygame.image.load(r"Demons killed.png")
demons_killed_img = pygame.transform.scale(demons_killed_img, (200, 32))


number_images = {str(i): pygame.transform.scale(pygame.image.load(fr"{i}.png"), (32, 32)) for i in range(11)}


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeons and Demons")
clock = pygame.time.Clock()


pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


def show_screen(image):
    screen.fill((0, 0, 0))
    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(image, image_rect.topleft)
    pygame.display.flip()
    time.sleep(3)


def get_enemy_speed(level):
    return min(PLAYER_SPEED - 1, INITIAL_ENEMY_SPEED + level * 0.3)

def get_spawn_interval(level):
    return max(2000, INITIAL_SPAWN_INTERVAL - level * 1000)

def get_enemy_size(level):
    return min(128, INITIAL_ENEMY_SIZE + level * 5)

def get_player_speed(level):
    return PLAYER_SPEED + level * 0.2


def display_level_transition(level):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render(f"Get Ready for Level {level}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
    pygame.display.flip()
    time.sleep(1)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        countdown = font.render(str(i), True, (255, 255, 255))
        screen.blit(countdown, (WIDTH // 2 - 10, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(1)


show_screen(intro_img)


level = 1
enemies = []
killed_enemies = 0
last_spawn_time = pygame.time.get_ticks()
health = MAX_HEALTH
player = pygame.Rect(WIDTH // 2, HEIGHT - 100, 64, 64)


attack = None
attack_speed = 7

running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(player_img, (player.x, player.y))

    screen.blit(level_img, (10, 10))
    if str(level) in number_images:
        screen.blit(number_images[str(level)], (140, 10))

    screen.blit(demons_killed_img, (10, 50))
    if str(killed_enemies) in number_images:
        screen.blit(number_images[str(killed_enemies)], (230, 50))
    if str(ENEMIES_PER_LEVEL) in number_images:
        screen.blit(number_images[str(ENEMIES_PER_LEVEL)], (275, 50))

    for i in range(health):
        pygame.draw.rect(screen, (255, 0, 0), (10 + i * 30, 90, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and attack is None:
                attack = pygame.Rect(player.x + 20, player.y, 40, 40)

    keys = pygame.key.get_pressed()
    player_speed = get_player_speed(level)
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y < HEIGHT - player.height:
        player.y += player_speed

    current_time = pygame.time.get_ticks()
    if len(enemies) < ENEMIES_PER_LEVEL and (
            current_time - last_spawn_time > get_spawn_interval(level) or len(enemies) < 3):
        size = get_enemy_size(level)
        enemy_rect = pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2), size, size)
        enemies.append(enemy_rect)
        last_spawn_time = current_time

    for enemy in enemies[:]:
        speed = get_enemy_speed(level)
        if enemy.x < player.x:
            enemy.x += speed
        elif enemy.x > player.x:
            enemy.x -= speed
        if enemy.y < player.y:
            enemy.y += speed
        elif enemy.y > player.y:
            enemy.y -= speed

        size = enemy.width
        enemy_img = pygame.transform.scale(enemy_images[min(level, 10)], (size, size))
        screen.blit(enemy_img, (enemy.x, enemy.y))

        if player.colliderect(enemy):
            enemies.remove(enemy)
            health -= 1
            if health <= 0:
                show_screen(lose_img)
                running = False

    if attack:
        screen.blit(attack_img, (attack.x, attack.y))
        attack.y -= attack_speed
        if attack.y < 0:
            attack = None

    for enemy in enemies[:]:
        if attack and attack.colliderect(enemy):
            enemies.remove(enemy)
            killed_enemies += 1
            attack = None

    if killed_enemies >= ENEMIES_PER_LEVEL:
        level += 1
        killed_enemies = 0
        enemies.clear()
        health = MAX_HEALTH
        if level > 10:
            show_screen(win_img)
            running = False
        else:
            display_level_transition(level)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
