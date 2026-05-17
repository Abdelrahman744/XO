# ✕ XO Game AI ○

A Tic-Tac-Toe game where a human plays against an AI powered by the **Minimax algorithm**. Built with Python and a Tkinter GUI featuring a dark-themed, two-column layout, canvas-drawn marks, hover effects, win-line highlighting, and a persistent score tracker.

---

## 📸 Features at a Glance

- 🎮 **Human vs AI** — You play as **X**, the AI plays as **O**
- 🧠 **3 Difficulty Levels** — Easy, Medium, Hard (controlled via Minimax depth)
- 🎨 **Premium Dark GUI** — Canvas-based board with a two-column horizontal layout
- ✨ **Hover Preview** — Highlights a cell before you click
- 🏆 **Win Line** — A golden stripe drawn through the winning combination
- 📊 **Score Tracker** — Persists across rounds without closing the window
- ⟳ **Instant Restart** — New Game button or switching difficulty auto-resets

---

## 📁 Project Structure

```
XO/
├── main.py       ← Entry point — run this to launch the game
├── game.py       ← Board logic (create board, moves, win/draw checks)
├── minimax.py    ← Minimax AI algorithm (evaluate, search, best move)
├── gui.py        ← Full Tkinter GUI (layout, canvas drawing, event handling)
└── README.md     ← This file
```

Each file has a single, focused responsibility to keep the code clean and easy to extend.

---

## 🚀 How to Run

> **No external libraries required.** Tkinter comes pre-installed with Python on Windows.

```bash
cd c:\Users\Amoun\Desktop\XO
python main.py
```

Make sure you have **Python 3.8+** installed.

---

## 🧠 How the AI Works — Minimax Algorithm

### What is Minimax?

Minimax is a **recursive decision-making algorithm** used in two-player zero-sum games. Instead of guessing, the AI mentally simulates every possible sequence of moves from the current board state and picks the one that leads to the best outcome for itself.

It works on two alternating roles:
- **Maximizer (AI)** — tries to maximize its score (wants to win)
- **Minimizer (Human)** — tries to minimize the AI's score (wants the AI to lose)

### Scoring System

| Outcome        | Score           |
|----------------|-----------------|
| AI wins        | `+10 - depth`   |
| Human wins     | `-10 + depth`   |
| Draw           | `0`             |
| Depth limit    | `0`             |

The depth adjustment means the AI prefers **faster wins** and **slower losses**.

### Algorithm Flow

```
find_best_move()
   └─ for each empty cell:
         place AI mark → call minimax(depth=1, is_maximizing=False)
             └─ for each human response:
                   place human mark → call minimax(depth=2, is_maximizing=True)
                       └─ ... recurse until win / draw / depth limit
         remove mark, record score
   └─ return cell with highest score
```

### Pseudocode

```
function minimax(board, depth, max_depth, is_maximizing):
    if AI wins:     return +10 - depth
    if Human wins:  return -10 + depth
    if Draw:        return 0
    if depth >= max_depth: return 0

    if is_maximizing:
        best = -∞
        for each empty cell:
            place AI mark
            best = max(best, minimax(board, depth+1, max_depth, False))
            undo mark
        return best
    else:
        best = +∞
        for each empty cell:
            place Human mark
            best = min(best, minimax(board, depth+1, max_depth, True))
            undo mark
        return best
```

---

## ⚙️ Difficulty Levels

Difficulty is controlled by limiting how many moves ahead the AI is allowed to think (**max depth**).

| Level  | Depth | Behaviour |
|--------|-------|-----------|
| Easy   | 1     | Only looks 1 move ahead. No long-term strategy — makes obvious mistakes and is easily beaten. |
| Medium | 3     | Looks 3 moves ahead. Blocks immediate threats and creates simple traps, but can be outsmarted with good planning. |
| Hard   | 9     | Explores the entire game tree to the very end. Plays **perfectly** — the best possible result for a human is a draw. |

---

## 🗂️ Module Reference

### `game.py` — Board Logic

| Symbol / Function       | Description |
|-------------------------|-------------|
| `EMPTY`, `PLAYER_X`, `PLAYER_O` | Constants for cell values |
| `WIN_PATTERNS`          | All 8 winning combinations (rows, columns, diagonals) |
| `create_board()`        | Returns a fresh 9-cell list filled with `EMPTY` |
| `get_available_moves()` | Returns indices of all empty cells |
| `make_move()`           | Places a player mark; returns `True` if successful |
| `check_winner()`        | Returns the winning pattern tuple, or `None` |
| `is_draw()`             | Returns `True` if the board is full with no winner |
| `is_game_over()`        | Returns `True` if someone won or it's a draw |

---

### `minimax.py` — AI Engine

| Function          | Description |
|-------------------|-------------|
| `evaluate()`      | Scores a terminal board state (+10, -10, or 0) |
| `minimax()`       | Recursive search tree exploration |
| `find_best_move()`| Entry point — returns the index of the optimal cell to play |

---

### `gui.py` — Graphical Interface

| Component              | Description |
|------------------------|-------------|
| **Left Panel**         | Fixed 220px column: title, score tracker, status label, difficulty selector, restart button |
| **Right Panel**        | 370×370 Canvas: grid lines, X/O marks, hover ghost, win highlight line |
| `_draw_grid()`         | Draws the 3×3 grid lines on the canvas |
| `_draw_x()` / `_draw_o()` | Draws X (two crossing lines) or O (ellipse) in a cell |
| `_on_canvas_hover()`   | Shows a subtle cell highlight before the user clicks |
| `_on_canvas_click()`   | Handles the human's move |
| `_ai_turn()`           | Triggers Minimax and applies the AI's move after a 250ms delay |
| `_end_game()`          | Updates scores, sets status text, draws the win line |
| `_restart_game()`      | Clears board state and canvas for a new round |

---

## 🎨 GUI Layout

```
┌─────────────────────┬──────────────────────────┐
│   ✕  XO GAME  ○     │                          │
│   Human vs AI       │                          │
│  ───────────────    │     Canvas Board         │
│  YOU │ DRAW │ AI    │        3 × 3             │
│   0  │  0   │  0   │    (marks drawn via       │
│  ───────────────    │      Tkinter Canvas)      │
│  Your Turn (X)      │                          │
│  ───────────────    │                          │
│  DIFFICULTY         │                          │
│  [Easy][Med][Hard]  │                          │
│  ───────────────    │                          │
│  [ ⟳ NEW GAME ]    │                          │
└─────────────────────┴──────────────────────────┘
```

---

## 📝 Project Report Summary

| Item         | Details |
|--------------|---------|
| Language     | Python 3 |
| GUI Library  | Tkinter (built-in) |
| AI Algorithm | Minimax with depth limiting |
| Board Size   | 3 × 3 |
| Players      | Human (X) vs AI (O) |
| Difficulty   | 3 levels (depth 1 / 3 / 9) |
| Win Detection| All 8 patterns checked after every move |

---

## 💡 Possible Future Enhancements

- [ ] Alpha-Beta Pruning — prune redundant branches to speed up Hard mode
- [ ] Choose your symbol — let the human pick X or O
- [ ] First-move selector — let the human or AI go first
- [ ] Sound effects on win / draw
- [ ] Animated mark drawing (stroke-by-stroke canvas animation)
