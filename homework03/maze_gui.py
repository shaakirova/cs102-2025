import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from maze import add_path_to_grid, bin_tree_maze, solve_maze

CELL_SIZE = 10
N, M = 51, 77


def generate_maze_with_path(rows=N, cols=M):
    while True:
        grid = bin_tree_maze(rows, cols)
        _, path = solve_maze(grid)
        if path:
            return grid, path


def draw_cell(x, y, color, size: int = 10):
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[str]], size: int = 10):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "purple"
            draw_cell(y, x, color, size)


def show_solution():
    maze_with_path = add_path_to_grid(GRID, PATH)
    draw_maze(maze_with_path)


if __name__ == "__main__":
    GRID, PATH = generate_maze_with_path(N, M)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{M * CELL_SIZE + 100}x{N * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
