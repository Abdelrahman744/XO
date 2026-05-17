"""
XO Game AI — Entry Point
Run this file to start the game.
"""

import tkinter as tk
from gui import GameApp


def main():
    root = tk.Tk()
    GameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
