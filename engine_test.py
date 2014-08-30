import unittest as T
import sys

from board import load_board
from board import index_to_sq
from board import sq_to_index
from board import fen_to_board
from board import print_board

from engine import find_mate_in_n
from engine import CHECKMATE

class EngineTest(T.TestCase):
    def write_mate_result(self, moves, fp):
        for piece, src, dest in moves:
            fp.write("%s %s-%s\n" % (
                piece, index_to_sq(src), index_to_sq(dest)))

    def test_simple_rook_mate_in_1(self):
        board = load_board([
            ["", "", "", "k", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "K", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["R", "", "", "", "", "", "", ""],
        ])

        mate_result = find_mate_in_n(board, "W", 1)
        assert mate_result[0] == CHECKMATE
        assert len(mate_result[1]) == 1
        winning_move = mate_result[1][0]
        assert winning_move[0] == "R"
        assert index_to_sq(winning_move[1]) == "a1"
        assert index_to_sq(winning_move[2]) == "a8"

    def test_simple_board_no_mate_in_1(self):
        board = load_board([
            ["", "", "", "k", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "K", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "R", "", "", "", "", ""],
        ])
        mate_result = find_mate_in_n(board, "W", 1)
        assert mate_result[0] == 0
        assert len(mate_result[1]) == 1

    def test_simple_forced_rook_mate_in_2(self):
        board = load_board([
            ["", "k", "", "", "", "", "", ""],
            ["", "", "", "", "Q", "", "", ""],
            ["", "", "K", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        mate_result = find_mate_in_n(board, "W", 2)

        assert mate_result[0] == CHECKMATE

    def test_mate_in_1_p1(self):
        board = load_board([
            [""] * 8,
            [""] * 8,
            ["", "", "", "B", "", "r", "p", ""],
            ["", "", "P", "", "", "k", "b", ""],
            [""] * 7 + ["p"],
            ["", "p", "", "K", "", "", "", ""],
            ["", "P", "", "", "", "", "B", ""],
            [""] * 8,
        ])
        result, mating_moves = find_mate_in_n(board, "W", 1)
        assert result == CHECKMATE
        self.write_mate_result(mating_moves, sys.stdout)
        assert len(mating_moves) == 1
        assert mating_moves[0][0] == "B"
        assert mating_moves[0][1] == sq_to_index("g2")
        assert mating_moves[0][2] == sq_to_index("h3")

    def test_mate_in_2_p1(self):
        fen = "1r6/4b2k/1q1pNrpp/p2Pp3/4P3/1P1R3Q/5PPP/5RK1 w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, "W", 2)
        self.write_mate_result(mating_moves, sys.stdout)
        assert len(mating_moves) == 3

    def test_mate_in_2_p2(self):
        fen = "3r1b1k/5Q1p/p2p1P2/5R2/4q2P/1P2P3/PB5K/8 w"
        board = fen_to_board(fen)
        print_board(board)
        result, mating_moves = find_mate_in_n(board, "W", 2)
        self.write_mate_result(mating_moves, sys.stdout)
        assert len(mating_moves) == 3

    def test_mate_in_3_anderssen_leipzig_1885(self):
        board = load_board([
            [""  , "q", "  ", "", "r", "  ", "  ", "  "],
            ["k", "  ", "  ", "", ""  , "p", "  ", "  "],
            ["p", "r", "  ", "", ""  , "b", "  ", "p"],
            ["R", "  ", "  ", "", ""  , "  ", "  ", "  "],
            ["  ", "P", "P", "", "B", "  ", "p", "  "],
            ["  ", "  ", "  ", "", "  ", "  ", "P", "  "],
            ["P", "  ", "  ", "", "  ", "  ", "K", "  "],
            ["  ", "  ", "  ", "", "  ", "  ", "  ", "  "]
        ])
        #mate_result = find_mate_in_n(board, "W", 3)
        #TODO
        assert True


if __name__ == "__main__":
    T.main()
