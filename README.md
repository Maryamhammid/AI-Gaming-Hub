# 🎮 AI Gaming Hub

**AI Gaming Hub** is a Python-based collection of classic games powered by Artificial Intelligence (AI). Built using **Pygame**, each game demonstrates different AI strategies like **Minimax**, **Expectimax**, and heuristic-based decision making.

---

##  Included Games

| Game            | AI Used                     | File           |
|-----------------|-----------------------------|----------------|
| Tic-Tac-Toe     | Minimax + Alpha-Beta Pruning| `tic.py`       |
| Connect Four    | Minimax + Alpha-Beta Pruning| `four.py`      |
| 2048            | Expectimax                  | `g_2048.py`    |
| Dots and Boxes  | Heuristic AI                | `dotsboxes.py` |

---

##  Features

-  Smart AI opponents for each game
-  Modern UI with animations and smooth transitions
-  Game status indicators: player turns, win/draw states
-  Highscore tracking (JSON)

---

##  Tech Stack

- **Language**: Python
- **Game Engine**: Pygame
- **AI Techniques**: Minimax, Expectimax, Heuristics
- **Storage**: JSON

---

## 📦 How to Run

```bash
# Clone the repo
git clone https://github.com/Maryamhammid/AI-Gaming-Hub.git
cd AI-Gaming-Hub

# Install dependencies
pip install pygame

# Run the game hub
python menu.py
