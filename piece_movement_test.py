import unittest as T

from board import sq_to_index
from board import index_to_sq
from board import starter_board
from board import load_board
from board import dump_board
from board import gen_successor

from piece_movement_rules import get_rook_valid_squares
from piece_movement_rules import get_bishop_valid_squares
from piece_movement_rules import get_queen_valid_squares
from piece_movement_rules import get_king_valid_squares
from piece_movement_rules import get_pawn_valid_squares
from piece_movement_rules import get_knight_valid_squares
from piece_movement_rules import get_piece_valid_squares
from piece_movement_rules import is_legal_move
from piece_movement_rules import is_in_check
from piece_movement_rules import is_in_checkmate
from piece_movement_rules import is_in_stalemate
from piece_movement_rules import _has_no_legal_moves


class PieceMovementTest(T.TestCase):

    def test_rook_starter_board_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("a1")
        assert get_rook_valid_squares(board, index) == []

    def test_rook_empty_board_valid_squares(self):
        board = load_board([
            ["", "", "", "", "", "", "", ""],
            ["", "R", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        rook_squares = ["a7", "b1", "b2", "b3", "b4", "b5", "b6", "b8",
                        "c7", "d7", "e7", "f7", "g7", "h7"]
        assert sorted(get_rook_valid_squares(board, sq_to_index("b7"))) == rook_squares

    def test_rook_blocked_capture_valid_squares(self):
        board = load_board([
            ["n", "R", "", "q", "", "", "", ""],
            ["", "r", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        rook_squares = ["a8", "b7", "c8", "d8"]
        assert sorted(get_rook_valid_squares(board, sq_to_index("b8"))) == rook_squares

    def test_rook_blocked_own_piece_valid_squares(self):
        board = load_board([
            ["", "R", "", "Q", "", "", "", ""],
            ["", "N", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        rook_squares = ["a8", "c8"]
        assert sorted(get_rook_valid_squares(board, sq_to_index("b8"))) == rook_squares

    def test_rook_valid_squares_capture_blocks_own_piece(self):
        board = load_board([
            ["R", "", "", "", "", "k", "", "K"],
            ["n", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        rook_squares = ["a7", "b8", "c8", "d8", "e8", "f8"]
        assert sorted(get_rook_valid_squares(board, sq_to_index("a8"))) == rook_squares

    def test_bishop_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("c1")
        assert get_bishop_valid_squares(board, index) == []

    def test_queen_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("d1")
        assert get_queen_valid_squares(board, index) == []

    def test_king_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("e1")
        assert get_king_valid_squares(board, index) == []

    def test_pawn_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("e2")
        assert sorted(get_pawn_valid_squares(board, index)) == ["e3", "e4"]

    def test_knight_valid_squares(self):
        board = starter_board[:]
        index = sq_to_index("b1")
        assert sorted(get_knight_valid_squares(board, index)) == ["a3", "c3"]

    def test_piece_valid_squares(self):
        board = starter_board[:]
        assert get_piece_valid_squares(board, "e1") == []
        assert get_piece_valid_squares(board, "a1") == []
        assert get_piece_valid_squares(board, "a8") == []
        assert sorted(get_piece_valid_squares(board, "e2")) == ["e3", "e4"]

    def test_is_legal_pawn_move(self):
        board = starter_board[:]
        assert is_legal_move(board, "e2", "e3")
        assert is_legal_move(board, "e2", "e4")
        assert not is_legal_move(board, "e2", "e5")
        assert not is_legal_move(board, "e2", "f3")
        assert is_legal_move(board, "e7", "e6")
        assert is_legal_move(board, "e7", "e5")
        assert not is_legal_move(board, "e7", "e4")

    def test_is_in_check_starter_board(self):
        board = starter_board[:]
        assert not is_in_check(board, "W")
        assert not is_in_check(board, "B")

    def test_is_in_check_basic_rook(self):
        board = load_board([
            ["R", "", "", "", "k", "", "K", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert is_in_check(board, "B")
        assert not is_in_check(board, "W")

    def test_is_in_check_basic_bishop(self):
        board = load_board([
            ["B", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "k", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "K", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert is_in_check(board, "B")
        assert not is_in_check(board, "W")

    def test_is_in_checkmate_simple_rook_mate(self):
        board = load_board([
            ["", "R", "", "k", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "K", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert is_in_checkmate(board, "B")
        assert not is_in_checkmate(board, "W")


    def test_is_in_checkmate_unprotected_attacker(self):
        board = load_board([
            ["k", "", "", "", "", "", "", ""],
            ["", "Q", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "K", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert not is_in_checkmate(board, "B")

    def test_is_in_checkmate_simple_rook_check(self):
        board = load_board([
            ["", "R", "", "", "k", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "K", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert not is_in_checkmate(board, "B")
        assert not is_in_checkmate(board, "W")

    def test_is_in_stalemate_with_rook(self):
        board = load_board([
            ["k", "", "", "", "", "", "", ""],
            ["", "R", "", "", "", "", "", ""],
            ["", "", "K", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ])
        assert is_in_stalemate(board, "B")
        assert not is_in_checkmate(board, "B")

    def test_not_in_mate_1(self):
        board = load_board([
            [' ', ' ', ' ', ' ', 'r', 'b', 'Q', 'k'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p'],
            ['p', ' ', ' ', 'p', ' ', 'P', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'R', ' ', ' '],
            [' ', ' ', ' ', ' ', 'q', ' ', ' ', 'P'],
            [' ', 'P', ' ', ' ', 'P', ' ', ' ', ' '],
            ['P', 'B', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'K', ' ']
        ])

        b2 = gen_successor(board, sq_to_index("h8"), sq_to_index("g8"))
        for row in dump_board(b2):
            print row
        assert not is_in_check(b2, "B")

        assert not is_in_checkmate(board, "B")
        assert not is_in_checkmate(board, "W")
        assert not is_in_stalemate(board, "B")
        assert not is_in_stalemate(board, "W")
        assert not _has_no_legal_moves(board, "B")

if __name__ == "__main__":
    T.main()
