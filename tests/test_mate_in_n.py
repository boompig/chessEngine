import sys
import unittest as T
from typing import List

from chess_engine.core.board import (BISHOP, WHITE, Board, fen_to_board,
                                     index_to_sq, load_board, print_board,
                                     sq_to_index)
from chess_engine.core.move import Move
from chess_engine.engine import CHECKMATE, find_mate_in_n


def write_mate_result(board: Board, moves: List[Move], fp) -> None:
    for i, move in enumerate(moves):
        fp.write("%d. %s\n" % (
            i,
            move.show(board)
        ))

class MateInOneTest(T.TestCase):
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

        mate_result = find_mate_in_n(board, WHITE, 1)
        assert mate_result[0] == CHECKMATE
        assert len(mate_result[1]) == 1
        winning_move = mate_result[1][0]
        assert winning_move.piece == "R"
        assert index_to_sq(winning_move.src) == "a1"
        assert index_to_sq(winning_move.dest) == "a8"

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
        mate_result = find_mate_in_n(board, WHITE, 1)
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
        mate_result = find_mate_in_n(board, WHITE, 2)

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
        result, mating_moves = find_mate_in_n(board, WHITE, 1)
        assert result == CHECKMATE
        write_mate_result(board, mating_moves, sys.stdout)
        assert len(mating_moves) == 1
        assert mating_moves[0].piece == BISHOP
        assert mating_moves[0].src == sq_to_index("g2")
        assert mating_moves[0].dest == sq_to_index("h3")


class MateInTwoTest(T.TestCase):
    def test_mate_in_2_p1(self):
        fen = "1r6/4b2k/1q1pNrpp/p2Pp3/4P3/1P1R3Q/5PPP/5RK1 w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, WHITE, 2)
        write_mate_result(board, mating_moves, sys.stdout)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_2_p2(self):
        fen = "3r1b1k/5Q1p/p2p1P2/5R2/4q2P/1P2P3/PB5K/8 w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, WHITE, 2)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_2_p3(self):
        fen = "r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, WHITE, 2)
        with open("mate.txt", "w") as fp:
            write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 3


class MateInThreeTest(T.TestCase):
    def assert_find_mate(self, fen: str):
        board = fen_to_board(fen)
        stats_dict = {}  # type: dict
        result, mating_moves = find_mate_in_n(board, WHITE, 3, stats_dict=stats_dict)
        with open("mate.txt", "w") as fp:
           write_mate_result(board, mating_moves, fp)
        print(stats_dict)
        assert result == CHECKMATE
        assert len(mating_moves) == 5

    def test_mate_in_3_p1(self):
        self.assert_find_mate("1r3r1k/5Bpp/8/8/P2qQ3/5R2/1b4PP/5K2 w")

    def test_mate_in_3_p2(self):
        self.assert_find_mate("r1b1r1k1/1pq1bp1p/p3pBp1/3pR3/7Q/2PB4/PP3PPP/5RK1 w")

    def test_mate_in_3_p3(self):
        """
        there is a variation which is not a mate in 3, but in 2
        because of ordering, it will return this variation, as the score
        is the same from the perspective of the engine
        """
        board = fen_to_board("r5rk/5p1p/5R2/4B3/8/8/7P/7K w")
        result, mating_moves = find_mate_in_n(board, WHITE, 3)
        # with open("mate.txt", "w") as fp:
        # write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) <= 5

    def test_mate_in_2_p3(self):
        """This is a reworking of above into mate in 2"""
        board = fen_to_board("r5rk/7p/R4p2/4B3/8/8/7P/7K w")
        result, mating_moves = find_mate_in_n(board, WHITE, 3)
        # with open("mate.txt", "w") as fp:
        #    write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_3_p4(self):
        self.assert_find_mate("5B2/6P1/1p6/8/1N6/kP6/2K5/8 w")


class MateInFourTest(T.TestCase):
    def assert_find_mate_in_4(self, fen: str):
        board = fen_to_board(fen)
        stats_dict = {}  # type: dict
        print_board(board)
        result, mating_moves = find_mate_in_n(board, WHITE, 4, stats_dict=stats_dict)
        with open("mate.txt", "w") as fp:
           write_mate_result(board, mating_moves, fp)
        print(stats_dict)
        assert result == CHECKMATE
        assert len(mating_moves) == 7

    def test_mate_in_4_p1(self):
        """Puzzles taken from here:
        http://wtharvey.com/m8n4.txt
        """
        self.assert_find_mate_in_4("r5rk/2p1Nppp/3p3P/pp2p1P1/4P3/2qnPQK1/8/R6R w")



# class MateInFiveTest(T.TestCase):
#     def test_mate_in_5_p1(self):
#         board = fen_to_board("2q1nk1r/4Rp2/1ppp1P2/6Pp/3p1B2/3P3P/PPP1Q3/6K1 w")
#         result, mating_moves = find_mate_in_n(board, WHITE, 5)
#         with open("mate.txt", "w") as fp:
#             write_mate_result(board, mating_moves, fp)
#         assert result == CHECKMATE
#         assert len(mating_moves) == 9
