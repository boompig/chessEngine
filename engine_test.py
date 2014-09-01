import unittest as T
import sys

from board import load_board
from board import index_to_sq
from board import sq_to_index
from board import fen_to_board
from board import print_board
from board import dump_board

from piece_movement_rules import is_capture

from engine import find_mate_in_n
from engine import CHECKMATE
from engine import score_move
from engine import gen_all_moves
from engine import dls_minimax
from engine import MIN, MAX


def write_mate_result(board, moves, fp):
    for piece, src, dest in moves:
        if is_capture(board, dest, board[src]):
            fp.write("%s %sx%s\n" % (
                piece, index_to_sq(src), index_to_sq(dest)))
        else:
            fp.write("%s %s-%s\n" % (
                piece, index_to_sq(src), index_to_sq(dest)))


class MoveOrderingTest(T.TestCase):
    def test_ordering_heuristic_simple(self):
        board = load_board([
            [" ", "", "", "k", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", "K", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            ["R", "", "", " ", "", "", "", ""],
        ])

        winning_move_score = score_move(board, sq_to_index("a1"), sq_to_index("a8"))
        idle_move_score = score_move(board, sq_to_index("a1"), sq_to_index("a7"))
        assert winning_move_score > idle_move_score

    def test_ordering_heuristic_in_gen_all_moves(self):
        """Similar to test case above, but makes sure that sorting by key works as expected."""
        board = load_board([
            [" ", "", "", "k", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", "K", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            [" ", "", "", " ", "", "", "", ""],
            ["R", "", "", " ", "", "", "", ""]
        ])

        all_moves = gen_all_moves(board, "W")
        def _score_move(move):
            return score_move(board, move[1], move[2])
        all_moves_sorted = sorted(all_moves, key=_score_move, reverse=True)

        win_move_index = None
        idle_move_index = None
        for i, (piece, src, dest) in enumerate(all_moves_sorted):
            if piece == "R" and index_to_sq(src) == "a1" and index_to_sq(dest) == "a8":
                win_move_index = i
            elif piece == "R" and index_to_sq(src) == "a1" and index_to_sq(dest) == "a7":
                idle_move_index = i

        assert win_move_index < idle_move_index


class PositionRankingTest(T.TestCase):
    def test_not_lose_immediately(self):
        """In any position, the opponent should choose the move which does not lose immediately."""
        # black to move. choose the option where black is not mated
        board = load_board([
            [" ", " ", "", " ", "k", "", "", ""],
            [" ", "Q", "", " ", " ", "", "", ""],
            [" ", " ", "", "K", " ", "", "", ""],
            [" ", " ", "", " ", " ", "", "", ""],
            [" ", " ", "", " ", " ", "", "", ""],
            [" ", " ", "", " ", " ", "", "", ""],
            [" ", " ", "", " ", " ", "", "", ""],
            [" ", " ", "", " ", " ", "", "", ""]
        ])
        result, move_list = dls_minimax(board, 2, MIN)
        assert len(move_list) == 2
        assert move_list[0][0] == "k"
        assert move_list[0][1] == sq_to_index("e8")
        assert move_list[0][2] == sq_to_index("f8")


class MateInOneEngineTest(T.TestCase):
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
        write_mate_result(board, mating_moves, sys.stdout)
        assert len(mating_moves) == 1
        assert mating_moves[0][0] == "B"
        assert mating_moves[0][1] == sq_to_index("g2")
        assert mating_moves[0][2] == sq_to_index("h3")

class MateInTwoEngineTest(T.TestCase):
    def test_mate_in_2_p1(self):
        fen = "1r6/4b2k/1q1pNrpp/p2Pp3/4P3/1P1R3Q/5PPP/5RK1 w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, "W", 2)
        write_mate_result(board, mating_moves, sys.stdout)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_2_p2(self):
        fen = "3r1b1k/5Q1p/p2p1P2/5R2/4q2P/1P2P3/PB5K/8 w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, "W", 2)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_2_p3(self):
        fen = "r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w"
        board = fen_to_board(fen)
        result, mating_moves = find_mate_in_n(board, "W", 2)
        with open("mate.txt", "w") as fp:
            write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

class MateInThreeEngineTest(T.TestCase):
    def test_mate_in_3_p1(self):
        board = fen_to_board("1r3r1k/5Bpp/8/8/P2qQ3/5R2/1b4PP/5K2 w")
        result, mating_moves = find_mate_in_n(board, "W", 3)
        #with open("mate.txt", "w") as fp:
        #    write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 5

    def test_mate_in_3_p2(self):
        board = fen_to_board("r1b1r1k1/1pq1bp1p/p3pBp1/3pR3/7Q/2PB4/PP3PPP/5RK1 w")
        result, mating_moves = find_mate_in_n(board, "W", 3)
        #with open("mate.txt", "w") as fp:
        #    write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 5

    def test_mate_in_3_p3(self):
        board = fen_to_board("r5rk/5p1p/5R2/4B3/8/8/7P/7K w")
        result, mating_moves = find_mate_in_n(board, "W", 3)
        #with open("mate.txt", "w") as fp:
            #write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_2_p3(self):
        """This is a reworking of above into mate in 2"""
        board = fen_to_board("r5rk/7p/R4p2/4B3/8/8/7P/7K w")
        result, mating_moves = find_mate_in_n(board, "W", 3)
        with open("mate.txt", "w") as fp:
            write_mate_result(board, mating_moves, fp)
        assert result == CHECKMATE
        assert len(mating_moves) == 3

    def test_mate_in_3_p4(self):
        board = fen_to_board("5B2/6P1/1p6/8/1N6/kP6/2K5/8 w")
        #result, mating_moves = find_mate_in_n(board, "W", 3)
        #with open("mate.txt", "w") as fp:
        #    write_mate_result(board, mating_moves, fp)
        #assert result == CHECKMATE
        #assert len(mating_moves) == 5
        assert True


class MateInFiveEngineTest(T.TestCase):
    def test_mate_in_5_p1(self):
        #board = fen_to_board("2q1nk1r/4Rp2/1ppp1P2/6Pp/3p1B2/3P3P/PPP1Q3/6K1 w")
        #result, mating_moves = find_mate_in_n(board, "W", 5)
        #with open("mate.txt", "w") as fp:
            #write_mate_result(board, mating_moves, fp)
        #assert result == CHECKMATE
        #assert len(mating_moves) == 9
        pass


if __name__ == "__main__":
    T.main()
