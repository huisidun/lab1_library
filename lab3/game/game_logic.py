# game/game_logic.py
import random
from typing import List


class MinesweeperGame:
    def __init__(self, rows: int, cols: int, mines: int):
        if rows <= 0 or cols <= 0 or mines < 0 or mines >= rows * cols:
            raise ValueError("Некорректные параметры поля.")
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mine_field: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]
        self.revealed: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self._place_mines()

    def _place_mines(self):
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_cells = random.sample(all_cells, self.mines)
        for r, c in mine_cells:
            self.mine_field[r][c] = True

    def count_adjacent_mines(self, row: int, col: int) -> int:
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.mine_field[nr][nc]:
                        count += 1
        return count

    def reveal(self, row: int, col: int) -> bool:
        if self.game_over or self.flagged[row][col]:
            return True
        if self.mine_field[row][col]:
            self.game_over = True
            return False
        self._reveal_recursive(row, col)
        if self._check_win():
            self.won = True
            self.game_over = True
        return not self.game_over

    def _reveal_recursive(self, row: int, col: int):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if self.revealed[row][col] or self.flagged[row][col]:
            return
        self.revealed[row][col] = True
        if self.count_adjacent_mines(row, col) == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr != 0 or dc != 0:
                        self._reveal_recursive(row + dr, col + dc)

    def toggle_flag(self, row: int, col: int):
        if not self.revealed[row][col] and not self.game_over:
            self.flagged[row][col] = not self.flagged[row][col]

    def _check_win(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.mine_field[r][c] and not self.revealed[r][c]:
                    return False
        return True

    def get_cell_state(self, row: int, col: int) -> str:
        if self.flagged[row][col]:
            return 'flag'
        if not self.revealed[row][col]:
            return 'hidden'
        if self.mine_field[row][col] and self.game_over:
            return 'mine'
        return str(self.count_adjacent_mines(row, col))