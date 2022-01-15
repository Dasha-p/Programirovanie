import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        y, x = cell
        sosedi = []
        if x == 0 and y == 0:
            sosedi = [self.curr_generation[y][x + 1], self.curr_generation[y + 1][x], self.curr_generation[y + 1][x + 1]]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == 0:
            sosedi = [self.curr_generation[y][x + 1], self.curr_generation[y + 1][x], self.curr_generation[y + 1][x + 1], self.curr_generation[y][x - 1],
                      self.curr_generation[y + 1][x - 1]]
        if x == len(self.curr_generation[0]) - 1 and y == 0:
            sosedi = [self.curr_generation[y][x - 1], self.curr_generation[y + 1][x], self.curr_generation[y + 1][x - 1]]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:
            sosedi = [self.curr_generation[y][x + 1], self.curr_generation[y - 1][x], self.curr_generation[y - 1][x + 1], self.curr_generation[y][x - 1],
                      self.curr_generation[y - 1][x - 1]]
        if x == 0 and y == len(self.curr_generation) - 1:
            sosedi = [self.curr_generation[y][x + 1], self.curr_generation[y - 1][x], self.curr_generation[y - 1][x + 1]]
        if x == len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:
            sosedi = [self.curr_generation[y][x - 1], self.curr_generation[y - 1][x], self.curr_generation[y - 1][x - 1]]
        if x == 0 and 0 < y < len(self.curr_generation) - 1:
            sosedi = [self.curr_generation[y][x + 1], self.curr_generation[y + 1][x], self.curr_generation[y + 1][x + 1], self.curr_generation[y - 1][x],
                      self.curr_generation[y - 1][x + 1]]
        if x == len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:
            sosedi = [self.curr_generation[y][x - 1], self.curr_generation[y + 1][x], self.curr_generation[y + 1][x - 1], self.curr_generation[y - 1][x],
                      self.curr_generation[y - 1][x - 1]]
        if 0 < x < len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    sosedi.append(self.curr_generation[y + i][x + j])
            del sosedi[4]

        return sosedi

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        pokolenie = copy.deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                n = self.get_neighbours((i, j)).count(1)
                if self.curr_generation[i][j] == 1:
                    if n < 2 or n > 3:
                        pokolenie[i][j] = 0
                else:
                    if n == 3:
                        pokolenie[i][j] = 1

        return pokolenie

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        shag = self.get_next_generation()
        self.curr_generation = shag
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        a = open(filename)
        stroki = a.readlines()
        a.close()
        grid = []
        for i in range(len(stroki)):
            rad = []
            for j in range(len(stroki[0])):
                rad.append(int(stroki[i][j]))
            grid.append(rad)
        igra = GameOfLife((len(grid), len(grid[0])))
        igra.curr_generation = grid
        return igra


    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        a = open(filename, "w")
        for i in range(len(self.curr_generation)):
            rad = ""
            for j in range(len(self.curr_generation)):
                rad += str(self.curr_generation[i][j])
            a.write(rad)
        a.close