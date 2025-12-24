import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        height, width = self.life.rows, self.life.cols
        for x in range(height + 2):
            for y in range(width + 2):
                if x == 0 or x == height + 1:
                    screen.addch(x, y, "-")
                elif y == 0 or y == width + 1:
                    screen.addch(x, y, "|")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                char = "█" if cell else " "
                screen.addch(y, x, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                key = screen.getch()
                if key == ord("q"):
                    break

                screen.clear()
                screen.addstr(0, 0, "Press 'q' to quit")
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                self.life.step()
                time.sleep(0.1)
        finally:
            curses.endwin()


if __name__ == "__main__":
    from life import GameOfLife

    life = GameOfLife((10, 30), randomize=True, max_generations=100)
    console_ui = Console(life)
    console_ui.run()
