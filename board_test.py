import unittest as T

from board import sq_to_index
from board import index_to_sq
from board import is_valid_square
from board import starter_board
from board import load_board
from board import dump_board
from board import get_piece_list


class BoardTest(T.TestCase):
    def test_sq_to_index(self):
        assert sq_to_index("a1") == 91
        assert starter_board[sq_to_index("a1")] == "WR"
        assert sq_to_index("a8") == 21
        assert starter_board[sq_to_index("a8")] == "BR"
        assert sq_to_index("h1") == 98
        assert starter_board[sq_to_index("h1")] == "WR"
        assert sq_to_index("h8") == 28
        assert starter_board[sq_to_index("h8")] == "BR"
        assert sq_to_index("c1") == 93
        assert starter_board[sq_to_index("c1")] == "WB"

    def test_index_to_sq(self):
        assert index_to_sq(91) == "a1"
        assert index_to_sq(21) == "a8"
        assert index_to_sq(98) == "h1"
        assert index_to_sq(28) == "h8"

    def test_valid_sq(self):
        idx = sq_to_index("a8")
        assert is_valid_square(idx)
        assert not is_valid_square(idx - 1)
        assert not is_valid_square(idx - 10)
        idx = sq_to_index("h8")
        assert is_valid_square(idx)
        assert not is_valid_square(idx + 1)
        assert not is_valid_square(idx + 2)
        idx = sq_to_index("h1")
        print starter_board[idx]
        assert is_valid_square(idx)
        assert not is_valid_square(idx + 1)
        assert not is_valid_square(idx + 10)

    def test_load_board(self):
        sample_board = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"],
        ]
        # comparison by value
        assert load_board(sample_board) == starter_board

    def test_dump_board(self):
        sample_board = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"],
        ]
        # comparison by value
        assert dump_board(starter_board) == sample_board

    def test_piece_list(self):
        board = starter_board[:]
        starter_piece_list = [
            ("a1", "WR"),
            ("a2", "WP"),
            ("b1", "WN"),
            ("b2", "WP"),
            ("c1", "WB"),
            ("c2", "WP"),
            ("d1", "WQ"),
            ("d2", "WP"),
            ("e1", "WK"),
            ("e2", "WP"),
            ("f1", "WB"),
            ("f2", "WP"),
            ("g1", "WN"),
            ("g2", "WP"),
            ("h1", "WR"),
            ("h2", "WP"),
        ]
        pl = get_piece_list(board, "W")
        apl = [(index_to_sq(idx), piece) for idx, piece in pl]
        assert sorted(apl) == starter_piece_list

if __name__ == "__main__":
    T.main()
