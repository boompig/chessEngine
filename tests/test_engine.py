"""
Some of the puzzles are fetched from here: http://wtharvey.com/m8n4.txt
"""

import unittest as T

from chess_engine.core.board import (ROOK, WHITE,
                                     index_to_sq, load_board,
                                     sq_to_index)
from chess_engine.core.move import Move
from chess_engine.engine import (MIN, dls_minimax,
                                 gen_all_moves, score_move)



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

        m1 = Move(board[sq_to_index("a1")], sq_to_index("a1"), sq_to_index("a8"))
        winning_move_score = score_move(board, m1)
        m2 = Move(board[sq_to_index("a1")], sq_to_index("a1"), sq_to_index("a7"))
        idle_move_score = score_move(board, m2)
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

        all_moves = gen_all_moves(board, WHITE)

        def _score_move(move):
            return score_move(board, move)

        all_moves_sorted = sorted(all_moves, key=_score_move, reverse=True)

        win_move_index = None
        idle_move_index = None
        for i, move in enumerate(all_moves_sorted):
            if move.piece == ROOK and index_to_sq(move.src) == "a1" and index_to_sq(move.dest) == "a8":
                win_move_index = i
            elif move.piece == ROOK and index_to_sq(move.src) == "a1" and index_to_sq(move.dest) == "a7":
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
        _, move_list = dls_minimax(board, 2, MIN)
        assert len(move_list) == 2
        assert move_list[0].piece == "k"
        assert move_list[0].src == sq_to_index("e8")
        assert move_list[0].dest == sq_to_index("f8")

