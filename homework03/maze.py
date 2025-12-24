from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    last_col = len(grid[0]) - 1
    direction = choice(("up", "right"))
    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < last_col - 1:
            grid[x][y + 1] = " "
    else:
        if y < last_col - 1:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    exits: List[Tuple[int, int]] = []

    for j in range(cols):
        if grid[0][j] == "X":
            exits.append((0, j))
        if grid[rows - 1][j] == "X":
            exits.append((rows - 1, j))

    for i in range(1, rows - 1):
        if grid[i][0] == "X":
            exits.append((i, 0))
        if grid[i][cols - 1] == "X":
            exits.append((i, cols - 1))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows, cols = len(grid), len(grid[0])
    next_k = k + 1
    new_grid = deepcopy(grid)

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] != k:
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and new_grid[nx][ny] == 0:
                    new_grid[nx][ny] = next_k
    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    rows, cols = len(grid), len(grid[0])
    path = []
    x, y = exit_coord
    k = grid[x][y]

    if not isinstance(k, int) or k <= 0:
        return None

    path.append((x, y))
    while isinstance(k, int) and k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if isinstance(grid[nx][ny], int) and grid[nx][ny] == k - 1:
                path.append((nx, ny))
                x, y = nx, ny
                k -= 1
                found = True
                break
        if not found:
            grid[path[-1][0]][path[-1][1]] = " "
            path.pop()
            if not path:
                return None
            x, y = path[-1]
            k = grid[x][y]

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    if x not in (0, rows - 1) and y not in (0, cols - 1):
        return False

    walls = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "■":
            walls += 1

    return walls == 2 if (x in (0, rows - 1) and y in (0, cols - 1)) else walls == 3


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    grid = deepcopy(grid)
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits[0]
    elif encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return grid, None

    start, end = min(exits), max(exits)

    grid[start[0]][start[1]] = 1
    grid[end[0]][end[1]] = 0

    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == " ":
                grid[x][y] = 0

    path_len = 0
    while grid[end[0]][end[1]] == 0:
        path_len += 1
        grid = make_step(grid, path_len)
        if path_len > (rows - 2) * (cols - 2):
            return grid, None

    path = shortest_path(grid, end)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    grid = bin_tree_maze(15, 15)
    print(pd.DataFrame(grid))
    _, path = solve_maze(grid)
    maze_with_path = add_path_to_grid(grid, path)
    print(pd.DataFrame(maze_with_path))
