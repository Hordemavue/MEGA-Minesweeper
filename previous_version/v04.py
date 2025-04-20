import pygame
import random
import os
import sys
import time

# ========== CONFIGURATION ========== 
GRID_WIDTH = 30
GRID_HEIGHT = 16
NB_BOMBS = 40
RANGE_FIRST_CLICK = 3
TILE_SIZE = 32
MENU_HEIGHT = 50  # Espace réservé pour le menu
zoom_factor = 1.0  # Facteur de zoom initial
start_time = None
end_time = None
# ===================================

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
window_width = screen_width
window_height = screen_height - 50

screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("MEGA-Minesweeper")

font = pygame.font.SysFont(None, 32)

# Chargement initial avec des images vides (remplacées plus tard)
img_discovery = img_not_discovery = img_flag = img_bomb = img_bomb_click = img_bomb_barre = None
img_numbers = []

def load_image(name, size):
    return pygame.transform.smoothscale(
        pygame.image.load(os.path.join("data", name)).convert_alpha(),
        (size, size)
    )

def update_tile_size_and_images():
    global TILE_SIZE, img_discovery, img_not_discovery, img_flag
    global img_bomb, img_bomb_click, img_bomb_barre, img_numbers, offset_x, offset_y

    available_width = window_width - 40  # 20px padding de chaque côté
    available_height = window_height - MENU_HEIGHT - 90  # 70px top padding + 20px bottom

    max_tile_w = available_width / GRID_WIDTH
    max_tile_h = available_height / GRID_HEIGHT

    TILE_SIZE = int(min(max_tile_w, max_tile_h) * zoom_factor)
    TILE_SIZE = max(8, TILE_SIZE)  # Pour éviter des tailles trop petites

    grid_width_px = TILE_SIZE * GRID_WIDTH
    grid_height_px = TILE_SIZE * GRID_HEIGHT

    offset_x = (window_width - grid_width_px) // 2
    offset_y = MENU_HEIGHT + 50 + ((window_height - MENU_HEIGHT - 90 - grid_height_px) // 2)

    img_discovery = load_image("discovery.png", TILE_SIZE)
    img_not_discovery = load_image("not_discovery.png", TILE_SIZE)
    img_flag = load_image("flag.png", TILE_SIZE)
    img_bomb = load_image("bomb.png", TILE_SIZE)
    img_bomb_click = load_image("bomb_click.png", TILE_SIZE)
    img_bomb_barre = load_image("bomb_barre.png", TILE_SIZE)
    img_numbers = [load_image(f"{i}.png", TILE_SIZE) for i in range(1, 16)]

update_tile_size_and_images()

# === Data Structures ===
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
flagged = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
bombs = []
first_click_done = False
game_over = False
win = False
clicked_bomb = None

def in_bounds(x, y):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

def get_neighbors(x, y, distance=2):
    return [(x+dx, y+dy) for dx in range(-distance, distance+1)
                           for dy in range(-distance, distance+1)
                           if (dx != 0 or dy != 0) and in_bounds(x+dx, y+dy)]

def place_bombs(safe_x, safe_y):
    global bombs
    forbidden = {(safe_x+dx, safe_y+dy)
                 for dx in range(-RANGE_FIRST_CLICK, RANGE_FIRST_CLICK+1)
                 for dy in range(-RANGE_FIRST_CLICK, RANGE_FIRST_CLICK+1)
                 if in_bounds(safe_x+dx, safe_y+dy)}

    all_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
    valid_positions = [pos for pos in all_positions if pos not in forbidden]
    bombs = random.sample(valid_positions, NB_BOMBS)
    for (bx, by) in bombs:
        grid[by][bx] = -1
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[y][x] == -1:
                continue
            count = sum((nx, ny) in bombs for (nx, ny) in get_neighbors(x, y, 2))
            grid[y][x] = count

def reveal(x, y):
    if not in_bounds(x, y) or revealed[y][x] or flagged[y][x]:
        return
    revealed[y][x] = True
    if grid[y][x] == 0:
        for nx, ny in get_neighbors(x, y, 2):
            reveal(nx, ny)

def check_win():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != -1 and not revealed[y][x]:
                return False
    return True

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            px, py = offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE
            if game_over:
                if grid[y][x] == -1:
                    if (x, y) == clicked_bomb:
                        screen.blit(img_bomb_click, (px, py))
                    elif flagged[y][x]:
                        screen.blit(img_flag, (px, py))
                    else:
                        screen.blit(img_bomb, (px, py))
                elif flagged[y][x] and (x, y) not in bombs:
                    screen.blit(img_bomb_barre, (px, py))
                elif revealed[y][x]:
                    screen.blit(img_discovery, (px, py))
                    if grid[y][x] > 0:
                        screen.blit(img_numbers[grid[y][x]-1], (px, py))
                else:
                    screen.blit(img_not_discovery, (px, py))
            else:
                if revealed[y][x]:
                    screen.blit(img_discovery, (px, py))
                    if grid[y][x] > 0:
                        screen.blit(img_numbers[grid[y][x]-1], (px, py))
                else:
                    screen.blit(img_not_discovery, (px, py))
                    if flagged[y][x]:
                        screen.blit(img_flag, (px, py))

def draw_status():
    global font

    # === Texte de fin ===
    text = ""
    if win:
        text = "gg"
    elif game_over:
        text = "lose"

    if text:
        surf = font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(window_width // 2, offset_y + GRID_HEIGHT * TILE_SIZE + 20))
        screen.blit(surf, rect)

    # === Compteur de bombes restantes (à gauche) ===
    flag_count = sum(flagged[y][x] for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH))
    remaining = NB_BOMBS - flag_count

    bomb_icon = pygame.transform.smoothscale(img_bomb, (32, 32))
    bomb_x = offset_x
    bomb_y = offset_y - 40

    bomb_text = font.render(f"{remaining}", True, (0, 0, 0))
    icon_rect = bomb_icon.get_rect(topleft=(bomb_x, bomb_y))
    text_rect = bomb_text.get_rect()
    text_y = bomb_y + (icon_rect.height - text_rect.height) // 2

    screen.blit(bomb_icon, icon_rect.topleft)
    screen.blit(bomb_text, (bomb_x + 40, text_y))

    # === Chrono (à droite) ===
    if first_click_done and not game_over and not win:
        elapsed_time = int(time.time() - start_time)
    elif first_click_done:
        elapsed_time = int(end_time - start_time)
    else:
        elapsed_time = 0

    clock_icon = pygame.transform.smoothscale(pygame.image.load("data/clock.png").convert_alpha(), (32, 32))
    time_text = font.render(f"{elapsed_time}s", True, (0, 0, 0))

    clock_x = offset_x + GRID_WIDTH * TILE_SIZE - 32
    clock_y = offset_y - 40

    time_rect = time_text.get_rect()
    clock_rect = clock_icon.get_rect(topleft=(clock_x, clock_y))
    time_x = clock_x - time_rect.width - 10
    time_y = clock_y + (clock_rect.height - time_rect.height) // 2

    screen.blit(time_text, (time_x, time_y))
    screen.blit(clock_icon, clock_rect.topleft)


# === Main Loop ===
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((238, 238, 238))
    pygame.draw.rect(screen, (23, 85, 126), (0, 0, window_width, MENU_HEIGHT))

    draw_grid()
    draw_status()
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            update_tile_size_and_images()

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                zoom_factor = min(zoom_factor + 0.1, 3.0)
                update_tile_size_and_images()
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                zoom_factor = max(zoom_factor - 0.1, 0.5)
                update_tile_size_and_images()

        if game_over or win:
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx = (mx - offset_x) // TILE_SIZE
            gy = (my - offset_y) // TILE_SIZE
            if not in_bounds(gx, gy):
                continue

            if event.button == 1:  # Left click
                if not first_click_done:
                    place_bombs(gx, gy)
                    first_click_done = True
                    start_time = time.time()


                if revealed[gy][gx] and grid[gy][gx] > 0:
                    flags_around = sum(
                        flagged[ny][nx]
                        for nx, ny in get_neighbors(gx, gy, 2)
                        if in_bounds(nx, ny)
                    )

                    if flags_around != grid[gy][gx]:
                        # Ne montre le flash que si le nombre de drapeaux est incorrect
                        to_flash = [
                            (nx, ny)
                            for nx, ny in get_neighbors(gx, gy, 2)
                            if in_bounds(nx, ny) and not flagged[ny][nx] and not revealed[ny][nx]
                        ]

                        # === Flash temporaire ===
                        for _ in range(1):
                            for x, y in to_flash:
                                px, py = offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE
                                pygame.draw.rect(screen, (200, 200, 200), (px, py, TILE_SIZE, TILE_SIZE))
                            pygame.display.flip()
                            pygame.time.delay(80)

                            draw_grid()
                            pygame.display.flip()
                            pygame.time.delay(80)

                    else:
                        # Si le bon nombre de drapeaux est présent, on révèle
                        for nx, ny in get_neighbors(gx, gy, 2):
                            if in_bounds(nx, ny) and not revealed[ny][nx] and not flagged[ny][nx]:
                                if grid[ny][nx] == -1:
                                    game_over = True
                                    end_time = time.time()
                                    clicked_bomb = (nx, ny)
                                else:
                                    reveal(nx, ny)

                        if check_win():
                            win = True
                            end_time = time.time()


                else:
                    if not flagged[gy][gx]:
                        if grid[gy][gx] == -1:
                            game_over = True
                            end_time = time.time()
                            clicked_bomb = (gx, gy)
                        else:
                            reveal(gx, gy)
                            if check_win():
                                win = True
                                end_time = time.time()


            elif event.button == 3:  # Right click
                if not revealed[gy][gx]:
                    flagged[gy][gx] = not flagged[gy][gx]

pygame.quit()
sys.exit()
