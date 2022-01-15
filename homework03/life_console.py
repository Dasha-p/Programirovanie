import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(len(self.life.curr_generation)):
            for j in range(len(self.life.curr_generation[0])):
                if self.life.curr_generation[i][j] == 1:
                    kletka = "*"
                else:
                    kletka = " "
                screen.adch(i + 1, j + 1, kletka)

    def run(self) -> None:
        screen = curses.initscr()
        curses.resizeterm(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            curses.napms(300)
        curses.endwin()


igra = GameOfLife((24, 80), max_generations=5)
ui = Console(igra)
ui.run()
