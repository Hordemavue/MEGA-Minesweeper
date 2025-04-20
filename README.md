# MEGA-Minesweeper

A powerful and fully resizable Minesweeper clone built with `pygame`.  
Supports classic gameplay with additional features like zoom, pause, auto-reveal, and difficulty presets.

## 🚀 Features

- **Auto Reveal:** Click on a number with the correct number of flags to auto-reveal surrounding cells.
- **Smart First Click:** Bombs are never placed within a square radius around the first click.
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
| Intermediate | 16    | 16     | 25    |
| Expert       | 30    | 16     | 60    |

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

