"""
GUI Module
Premium Tkinter interface for the Tic-Tac-Toe game.
Two-column horizontal layout: controls on the left, canvas board on the right.
Features a dark theme, canvas-drawn marks, hover effects, win-line highlight,
and persistent score tracking.
"""

import tkinter as tk
from tkinter import font as tkfont
from game import (
    create_board, make_move, check_winner, is_draw,
    get_available_moves, PLAYER_X, PLAYER_O
)
from minimax import find_best_move


# ─── Color Palette ────────────────────────────────────────────────
COLORS = {
    'bg':          '#0f0e17',
    'surface':     '#1a1a2e',
    'panel':       '#16213e',
    'grid':        '#2d3561',
    'x':           '#ff6b6b',
    'o':           '#4ecdc4',
    'text':        '#fffffe',
    'text_dim':    '#94a1b2',
    'accent':      '#e53170',
    'win':         '#ffd803',
    'draw':        '#94a1b2',
    'btn_normal':  '#1a1a2e',
    'btn_hover':   '#2d3561',
    'btn_active':  '#e53170',
    'success':     '#2cb67d',
    'separator':   '#2d3561',
}

# ─── Difficulty Presets ───────────────────────────────────────────
DIFFICULTIES = {
    'Easy':   {'depth': 1,  'desc': 'Depth 1\nLooks 1 move ahead'},
    'Medium': {'depth': 3,  'desc': 'Depth 3\nLooks 3 moves ahead'},
    'Hard':   {'depth': 9,  'desc': 'Depth 9\nPlays perfectly'},
}

# ─── Board Dimensions ────────────────────────────────────────────
CELL_SIZE   = 110
BOARD_PAD   = 20
LINE_WIDTH  = 3
MARK_PAD    = 24
MARK_WIDTH  = 6
BOARD_PX    = CELL_SIZE * 3 + BOARD_PAD * 2   # 370


class GameApp:
    """Main application class for the XO Game."""

    def __init__(self, root):
        self.root = root
        self.root.title("XO Game AI")
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(False, False)

        # ── State ──────────────────────────────────
        self.board        = create_board()
        self.human        = PLAYER_X
        self.ai           = PLAYER_O
        self.current_turn = self.human
        self.game_active  = True
        self.difficulty   = 'Medium'
        self.scores       = {'human': 0, 'ai': 0, 'draw': 0}
        self.win_line_ids = []

        # ── Fonts ──────────────────────────────────
        self.font_title  = tkfont.Font(family='Segoe UI', size=18, weight='bold')
        self.font_sub    = tkfont.Font(family='Segoe UI', size=9)
        self.font_status = tkfont.Font(family='Segoe UI', size=12, weight='bold')
        self.font_score  = tkfont.Font(family='Segoe UI', size=20, weight='bold')
        self.font_slabel = tkfont.Font(family='Segoe UI', size=8)
        self.font_btn    = tkfont.Font(family='Segoe UI', size=9, weight='bold')

        self._build_ui()

    # ══════════════════════════════════════════════════════════════
    #  UI CONSTRUCTION
    # ══════════════════════════════════════════════════════════════

    def _build_ui(self):
        """Build two-column layout: left panel + right canvas."""

        # ── Outer wrapper ──────────────────────────
        outer = tk.Frame(self.root, bg=COLORS['bg'])
        outer.pack(padx=18, pady=18, fill=tk.BOTH, expand=True)

        # ── Left Panel ─────────────────────────────
        left = tk.Frame(outer, bg=COLORS['panel'], width=220)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        left.pack_propagate(False)          # keep fixed width

        # ── Right Panel (canvas) ───────────────────
        right = tk.Frame(outer, bg=COLORS['bg'])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_left_panel(left)
        self._build_right_panel(right)

    # ── Left Panel Sections ───────────────────────

    def _build_left_panel(self, parent):
        """Title, scores, status, difficulty, restart — stacked vertically."""

        # Title
        tk.Label(
            parent, text="✕  XO GAME  ○",
            font=self.font_title, fg=COLORS['text'], bg=COLORS['panel']
        ).pack(pady=(18, 2))

        tk.Label(
            parent, text="Human vs AI",
            font=self.font_sub, fg=COLORS['text_dim'], bg=COLORS['panel']
        ).pack(pady=(0, 12))

        self._separator(parent)

        # Score board
        self._build_scoreboard(parent)

        self._separator(parent)

        # Status
        self.status_label = tk.Label(
            parent, text="Your Turn  (X)",
            font=self.font_status, fg=COLORS['x'],
            bg=COLORS['panel'], wraplength=200, justify=tk.CENTER
        )
        self.status_label.pack(pady=14)

        self._separator(parent)

        # Difficulty
        tk.Label(
            parent, text="DIFFICULTY",
            font=self.font_slabel, fg=COLORS['text_dim'], bg=COLORS['panel']
        ).pack(pady=(12, 6))

        self._build_difficulty_buttons(parent)

        # Difficulty description
        self.diff_desc = tk.Label(
            parent,
            text=DIFFICULTIES[self.difficulty]['desc'],
            font=self.font_sub, fg=COLORS['text_dim'],
            bg=COLORS['panel'], justify=tk.CENTER
        )
        self.diff_desc.pack(pady=(6, 0))

        self._separator(parent)

        # Restart
        self.restart_btn = tk.Label(
            parent, text="⟳  NEW GAME",
            font=self.font_btn, fg=COLORS['text'],
            bg=COLORS['btn_normal'], padx=16, pady=7, cursor='hand2'
        )
        self.restart_btn.pack(pady=14)
        self.restart_btn.bind('<Button-1>', lambda e: self._restart_game())
        self.restart_btn.bind('<Enter>',   lambda e: self.restart_btn.config(bg=COLORS['btn_hover']))
        self.restart_btn.bind('<Leave>',   lambda e: self.restart_btn.config(bg=COLORS['btn_normal']))

    def _separator(self, parent):
        tk.Frame(parent, bg=COLORS['separator'], height=1).pack(fill=tk.X, padx=14)

    # ── Score Board ───────────────────────────────

    def _build_scoreboard(self, parent):
        frame = tk.Frame(parent, bg=COLORS['panel'])
        frame.pack(pady=10, fill=tk.X)

        items = [
            ('human', 'YOU\n(X)', COLORS['x']),
            ('draw',  'DRAW',    COLORS['draw']),
            ('ai',    'AI\n(O)', COLORS['o']),
        ]
        self.score_labels = {}
        for key, title, color in items:
            col = tk.Frame(frame, bg=COLORS['panel'])
            col.pack(side=tk.LEFT, expand=True)
            tk.Label(col, text=title, font=self.font_slabel,
                     fg=color, bg=COLORS['panel'], justify=tk.CENTER).pack()
            lbl = tk.Label(col, text='0', font=self.font_score,
                           fg=COLORS['text'], bg=COLORS['panel'])
            lbl.pack()
            self.score_labels[key] = lbl

    def _update_scores(self):
        for key, lbl in self.score_labels.items():
            lbl.config(text=str(self.scores[key]))

    # ── Difficulty Buttons ────────────────────────

    def _build_difficulty_buttons(self, parent):
        frame = tk.Frame(parent, bg=COLORS['panel'])
        frame.pack()
        self.diff_buttons = {}

        for name in DIFFICULTIES:
            btn = tk.Label(
                frame, text=name, font=self.font_btn,
                fg=COLORS['text'], bg=COLORS['btn_normal'],
                padx=10, pady=4, cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=3)
            btn.bind('<Button-1>', lambda e, n=name: self._set_difficulty(n))
            btn.bind('<Enter>',   lambda e, b=btn, n=name: b.config(
                bg=COLORS['btn_hover'] if n != self.difficulty else COLORS['btn_active']))
            btn.bind('<Leave>',   lambda e, b=btn, n=name: b.config(
                bg=COLORS['btn_active'] if n == self.difficulty else COLORS['btn_normal']))
            self.diff_buttons[name] = btn

        self._highlight_difficulty()

    def _highlight_difficulty(self):
        for name, btn in self.diff_buttons.items():
            bg = COLORS['btn_active'] if name == self.difficulty else COLORS['btn_normal']
            btn.config(bg=bg)

    def _set_difficulty(self, name):
        self.difficulty = name
        self._highlight_difficulty()
        self.diff_desc.config(text=DIFFICULTIES[name]['desc'])
        self._restart_game()

    # ── Right Panel (Canvas Board) ─────────────────

    def _build_right_panel(self, parent):
        self.canvas = tk.Canvas(
            parent,
            width=BOARD_PX, height=BOARD_PX,
            bg=COLORS['surface'], highlightthickness=0
        )
        self.canvas.pack(expand=True)
        self._draw_grid()
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<Motion>',   self._on_canvas_hover)

    # ══════════════════════════════════════════════════════════════
    #  CANVAS DRAWING
    # ══════════════════════════════════════════════════════════════

    def _cell_bbox(self, index):
        """Return (x1, y1, x2, y2) pixel coords for a cell index (0-8)."""
        row, col = divmod(index, 3)
        x1 = BOARD_PAD + col * CELL_SIZE
        y1 = BOARD_PAD + row * CELL_SIZE
        return x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE

    def _draw_grid(self):
        for i in range(1, 3):
            x = BOARD_PAD + i * CELL_SIZE
            self.canvas.create_line(
                x, BOARD_PAD, x, BOARD_PAD + 3 * CELL_SIZE,
                fill=COLORS['grid'], width=LINE_WIDTH, capstyle=tk.ROUND
            )
            y = BOARD_PAD + i * CELL_SIZE
            self.canvas.create_line(
                BOARD_PAD, y, BOARD_PAD + 3 * CELL_SIZE, y,
                fill=COLORS['grid'], width=LINE_WIDTH, capstyle=tk.ROUND
            )

    def _draw_x(self, index, color=None):
        color = color or COLORS['x']
        x1, y1, x2, y2 = self._cell_bbox(index)
        p = MARK_PAD
        self.canvas.create_line(x1+p, y1+p, x2-p, y2-p,
                                fill=color, width=MARK_WIDTH, capstyle=tk.ROUND)
        self.canvas.create_line(x2-p, y1+p, x1+p, y2-p,
                                fill=color, width=MARK_WIDTH, capstyle=tk.ROUND)

    def _draw_o(self, index, color=None):
        color = color or COLORS['o']
        x1, y1, x2, y2 = self._cell_bbox(index)
        p = MARK_PAD
        self.canvas.create_oval(x1+p, y1+p, x2-p, y2-p,
                                outline=color, width=MARK_WIDTH)

    def _draw_mark(self, index, player, color=None):
        if player == PLAYER_X:
            self._draw_x(index, color)
        else:
            self._draw_o(index, color)

    def _draw_win_line(self, pattern):
        start, _, end = pattern
        sx1, sy1, sx2, sy2 = self._cell_bbox(start)
        ex1, ey1, ex2, ey2 = self._cell_bbox(end)
        self.canvas.create_line(
            (sx1+sx2)/2, (sy1+sy2)/2,
            (ex1+ex2)/2, (ey1+ey2)/2,
            fill=COLORS['win'], width=5, capstyle=tk.ROUND
        )

    # ── Hover Ghost ───────────────────────────────

    def _on_canvas_hover(self, event):
        self.canvas.delete('hover')
        if not self.game_active or self.current_turn != self.human:
            return
        index = self._pixel_to_index(event.x, event.y)
        if index is not None and self.board[index] == ' ':
            x1, y1, x2, y2 = self._cell_bbox(index)
            self.canvas.create_rectangle(
                x1+2, y1+2, x2-2, y2-2,
                fill=COLORS['grid'], outline='', tags='hover'
            )
            self.canvas.tag_lower('hover')

    def _pixel_to_index(self, px, py):
        col = int((px - BOARD_PAD) // CELL_SIZE)
        row = int((py - BOARD_PAD) // CELL_SIZE)
        if 0 <= col < 3 and 0 <= row < 3:
            return row * 3 + col
        return None

    # ══════════════════════════════════════════════════════════════
    #  GAME LOGIC
    # ══════════════════════════════════════════════════════════════

    def _on_canvas_click(self, event):
        if not self.game_active or self.current_turn != self.human:
            return
        index = self._pixel_to_index(event.x, event.y)
        if index is None or not make_move(self.board, index, self.human):
            return

        self._draw_mark(index, self.human)
        self.canvas.delete('hover')

        win_pattern = check_winner(self.board, self.human)
        if win_pattern:
            self._end_game('human', win_pattern)
            return
        if is_draw(self.board):
            self._end_game('draw')
            return

        self.current_turn = self.ai
        self.status_label.config(text="AI is thinking…", fg=COLORS['o'])
        self.root.update_idletasks()
        self.root.after(250, self._ai_turn)

    def _ai_turn(self):
        if not self.game_active:
            return

        depth = DIFFICULTIES[self.difficulty]['depth']
        move  = find_best_move(self.board, self.ai, self.human, depth)

        if move is None:
            return

        make_move(self.board, move, self.ai)
        self._draw_mark(move, self.ai)

        win_pattern = check_winner(self.board, self.ai)
        if win_pattern:
            self._end_game('ai', win_pattern)
            return
        if is_draw(self.board):
            self._end_game('draw')
            return

        self.current_turn = self.human
        self.status_label.config(text="Your Turn  (X)", fg=COLORS['x'])

    def _end_game(self, result, win_pattern=None):
        self.game_active = False

        if result == 'human':
            self.scores['human'] += 1
            self.status_label.config(text="🎉 You Win!", fg=COLORS['success'])
        elif result == 'ai':
            self.scores['ai'] += 1
            self.status_label.config(text="AI Wins!", fg=COLORS['accent'])
        else:
            self.scores['draw'] += 1
            self.status_label.config(text="It's a Draw!", fg=COLORS['draw'])

        if win_pattern:
            self._draw_win_line(win_pattern)

        self._update_scores()

    def _restart_game(self):
        self.board        = create_board()
        self.current_turn = self.human
        self.game_active  = True
        self.status_label.config(text="Your Turn  (X)", fg=COLORS['x'])
        self.canvas.delete('all')
        self.win_line_ids.clear()
        self._draw_grid()
