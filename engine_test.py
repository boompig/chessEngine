import unittest as T

from board import load_board
from board import index_to_sq

from engine import find_mate
from engine import CHECKMATE

class EngineTest(T.TestCase):
    def test_simple_rook_mate_in_one(self):
        board = load_board([
            ["", "", "", "BK", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "WK", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WR", "", "", "", "", "", "", ""],
        ])

        mate_result = find_mate(board, "W")
        assert mate_result[0] == CHECKMATE
        assert len(mate_result[1]) == 1
        winning_move = mate_result[1][0]
        assert winning_move[0] == "WR"
        assert index_to_sq(winning_move[1]) == "a1"
        assert index_to_sq(winning_move[2]) == "a8"

    def test_simple_board_no_mate_in_one(self):
        board = load_board([
            ["", "", "", "BK", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "WK", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "WR", "", "", "", "", ""],
        ])
        mate_result = find_mate(board, "W")
        assert mate_result[0] == 0
        assert len(mate_result[1]) == 1

if __name__ == "__main__":
    T.main()
