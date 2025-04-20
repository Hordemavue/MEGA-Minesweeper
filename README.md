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

**Already in game:**
- **Pause/Resume:** Hit `P` to pause/resume at any time.
- **Dynamic Scaling:** Automatically adjusts tile size when resizing the window.
- **Zoom In/Out:** Use `+` or `-` to zoom the board.
- **Difficulty Presets:** Beginner, Intermediate, Expert.
- **Flag Counter & Timer:** Displays remaining bombs and elapsed time.
- **START A NEW GAME :** Click on the smiley just above the grid 

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
   
   ```git clone https://github.com/yourusername/mega-minesweeper.git```
   
   ```cd mega-minesweeper```

3. Install dependencies:
   
   ```pip install pygame```

4. Make sure the data/ folder contains the required image assets:
   
   discovery.png
   not_discovery.png
   flag.png
   bomb.png
   bomb_click.png
   bomb_barre.png
   playing.png
   clock.png
   param.png
   1.png - 24.png

5. Run the game:

   ```py main.py```

## Some pictures

Open the game

![image](https://github.com/user-attachments/assets/e8bb6396-4ecb-411c-b9cf-2f8d24f2995e)

First click 

![image](https://github.com/user-attachments/assets/c1b46ea1-0717-45a4-a137-74687058374d)

About to finish 

![image](https://github.com/user-attachments/assets/128f8da8-7a75-44e2-a895-68b29a25b24e)

Win the game 

![image](https://github.com/user-attachments/assets/9fcb12d1-9e31-4357-94a8-f7e73e9fa7b0)

Lose the game 

![image](https://github.com/user-attachments/assets/20064394-ab89-470a-a98d-1d98d0c14b7f)

Pause the game (p)

![image](https://github.com/user-attachments/assets/6912db24-0231-4ac1-9696-cfa7185d54eb)

Zoom the game (+) (it miss a scroll bar)

![image](https://github.com/user-attachments/assets/b674d677-59ff-440a-8455-f39dedfda904)

Unzoom the game (-)

![image](https://github.com/user-attachments/assets/9483a262-7003-4846-8d2d-0be7ff96f665)

## My personal best 

Intermediate (16x16, 30 bombs)

![image](https://github.com/user-attachments/assets/ffceb178-e1e4-4712-8ecd-25c36b38eccf)

