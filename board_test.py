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
        assert starter_board[sq_to_index("a1")] == "R"
        assert sq_to_index("a8") == 21
        assert starter_board[sq_to_index("a8")] == "r"
        assert sq_to_index("h1") == 98
        assert starter_board[sq_to_index("h1")] == "R"
        assert sq_to_index("h8") == 28
        assert starter_board[sq_to_index("h8")] == "r"
        assert sq_to_index("c1") == 93
        assert starter_board[sq_to_index("c1")] == "B"

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
        assert is_valid_square(idx)
        assert not is_valid_square(idx + 1)
        assert not is_valid_square(idx + 10)

    def test_load_board(self):
        sample_board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        # comparison by value
        assert load_board(sample_board) == starter_board

    def test_dump_board(self):
        sample_board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        # comparison by value
        assert dump_board(starter_board) == sample_board

    def test_piece_list(self):
        board = starter_board[:]
        starter_piece_list = [
            ("a1", "R"),
            ("a2", "P"),
            ("b1", "N"),
            ("b2", "P"),
            ("c1", "B"),
            ("c2", "P"),
            ("d1", "Q"),
            ("d2", "P"),
            ("e1", "K"),
            ("e2", "P"),
            ("f1", "B"),
            ("f2", "P"),
            ("g1", "N"),
            ("g2", "P"),
            ("h1", "R"),
            ("h2", "P"),
        ]
        pl = get_piece_list(board, "W")
        apl = [(index_to_sq(idx), piece) for idx, piece in pl]
        assert sorted(apl) == starter_piece_list

if __name__ == "__main__":
    T.main()
