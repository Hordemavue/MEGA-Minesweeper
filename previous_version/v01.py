import pygame
import random
import os
import sys

# ========== CONFIGURATION ==========
GRID_WIDTH = 30
GRID_HEIGHT = 16
NB_BOMBS = 40
RANGE_FIRST_CLICK = 3
TILE_SIZE = 32
# ===================================

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE + 40))
pygame.display.set_caption("MEGA-Minesweeper")

font = pygame.font.SysFont(None, 32)

# === Load Images ===
def load_image(name):
    return pygame.transform.smoothscale(
        pygame.image.load(os.path.join("data", name)).convert_alpha(),
        (TILE_SIZE, TILE_SIZE)
    )

img_discovery = load_image("discovery.png")
img_not_discovery = load_image("not_discovery.png")
img_flag = load_image("flag.png")
img_bomb = load_image("bomb.png")
img_bomb_click = load_image("bomb_click.png")
img_bomb_barre = load_image("bomb_barre.png")
img_numbers = [load_image(f"{i}.png") for i in range(1, 16)]

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
    # Set numbers
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
            px, py = x * TILE_SIZE, y * TILE_SIZE
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
    text = ""
    if win:
        text = "gg"
    elif game_over:
        text = "lose"

    if text:
        surf = font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(GRID_WIDTH * TILE_SIZE // 2, GRID_HEIGHT * TILE_SIZE + 20))
        screen.blit(surf, rect)

# === Main Loop ===
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    draw_grid()
    draw_status()
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over or win:
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // TILE_SIZE, my // TILE_SIZE
            if not in_bounds(gx, gy):
                continue

            if event.button == 1:  # Left click
                if not first_click_done:
                    place_bombs(gx, gy)
                    first_click_done = True
                if flagged[gy][gx]:
                    continue
                if grid[gy][gx] == -1:
                    game_over = True
                    clicked_bomb = (gx, gy)
                else:
                    reveal(gx, gy)
                    if check_win():
                        win = True

            elif event.button == 3:  # Right click
                if not revealed[gy][gx]:
                    flagged[gy][gx] = not flagged[gy][gx]

pygame.quit()
sys.exit()
