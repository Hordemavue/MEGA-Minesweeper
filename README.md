# MEGA-Minesweeper

Not Minesweeper, MEGA-Minesweeper !!! The same game but numbers dont indicate the number on the 8 surrounding cells (3x3 square -1, the center) but the 24 surrounding cells (5x5 -1, the center) !! NO, YOU ARE NOT DREAMING, THATS MEGA-MINESWEEPER !!! 

## 🚀 Features 

**For the moment, to change in code, line 5 to 13 :**
- **GRID_WIDTH and GRID_HEIGHT:** To change the size of the grid.
- **NB_BOMBS:** To change the number of the bomb.
- **RANGE_FIRST_CLICK:** Bombs are never placed within a square radius around the first click. (I recommand at least 2, 3 should be better, more is too much)
- **SHOW_MILLISECONDS:** To have a better information about the timer.
- **ACTIVATE_FLASH_LIGHT:** To see which case influence the number where you just click at.
- **AUTO_CLICK_ON_NUMBER:** An Auto Reveal. Click on a number with the correct number of flags to auto-reveal surrounding cells.

** Already in game :**
- **Pause/Resume:** Hit `P` to pause/resume at any time.
- **Dynamic Scaling:** Automatically adjusts tile size when resizing the window.
- **Zoom In/Out:** Use `+` or `-` to zoom the board.
- **Difficulty Presets:** Beginner, Intermediate, Expert.
- **Flag Counter & Timer:** Displays remaining bombs and elapsed time.

## 🎮 Controls

- **Left Click:** Reveal a tile.
- **Right Click:** Flag/Unflag a tile.
- **P key:** Pause or resume the game.
- **+ / - keys:** Zoom in and out.

## 🧱 Difficulty Presets

| Level        | Width | Height | Bombs |
|--------------|-------|--------|-------|
| Beginner     | 10    | 10     | 8     |
| Intermediate | 16    | 16     | 30    |
| Expert       | 30    | 16     | 70    |

## 🧩 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/mega-minesweeper.git
   cd mega-minesweeper

2. Install dependencies:
pip install pygame

3. Make sure the data/ folder contains the required image assets:
discovery.png
not_discovery.png
flag.png
bomb.png
bomb_click.png
bomb_barre.png
playing.png
clock.png
param.png
1.png - 15.png

4. Run the game:
py minesweeper.py

