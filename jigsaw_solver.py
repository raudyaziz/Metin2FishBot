"""Optimal strategy for the fishing jigsaw, backed by the precomputed lookup
table exported by https://github.com/aguunu/fishing-jigsaw
(`cargo run --release --bin export`, gzip the result into data/jigsaw_table.bin.gz).

The table holds one byte per (board, piece): the action that minimizes the
expected number of pieces needed to fill the board. Layout: row = board bitmask,
column = figure index, value = (column << 2) | row of the piece's top-left cell,
or SKIP_ACTION to throw the piece away.
"""
import gzip
import os
import shutil

import numpy as np

ROWS = 4
COLS = 6
CELLS = ROWS * COLS
SKIP_ACTION = CELLS

# PuzzleBot piece type -> figure index used by the table.
FIGURE_INDEX = {1: 0, 2: 1, 5: 2, 6: 3, 3: 4, 4: 5}

TABLE_PATH = os.path.join('data', 'jigsaw_table.bin')


class JigsawSolver:

    def __init__(self, path=TABLE_PATH):
        shape = (1 << CELLS, len(FIGURE_INDEX))
        expected_size = shape[0] * shape[1]

        if not os.path.isfile(path) and os.path.isfile(path + '.gz'):
            # first run: unpack the committed table (written atomically so an
            # interrupted unpack can't leave a truncated file behind)
            with gzip.open(path + '.gz', 'rb') as src, open(path + '.tmp', 'wb') as dst:
                shutil.copyfileobj(src, dst)
            os.replace(path + '.tmp', path)

        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Puzzle table not found: {path}(.gz). Generate it with "
                f"`cargo run --release --bin export` in the fishing-jigsaw "
                f"repo and copy it there.")
        if os.path.getsize(path) != expected_size:
            raise ValueError(
                f"{path} has the wrong size (expected {expected_size} bytes). "
                f"Regenerate it with the fishing-jigsaw export binary.")

        self.table = np.memmap(path, dtype=np.uint8, mode='r', shape=shape)

    @staticmethod
    def board_to_bits(board):
        bits = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col]:
                    bits |= 1 << (CELLS - 1 - (col * ROWS + row))
        return bits

    def best_move(self, board, piece_type):
        """Return (row, col) for the piece's top-left cell, or None to throw it away."""
        action = int(self.table[self.board_to_bits(board), FIGURE_INDEX[piece_type]])
        if action == SKIP_ACTION:
            return None
        return action & 0b11, action >> 2
