import unittest as T

from board import sq_to_index
from board import index_to_sq
from board import Board

from piece_movement_rules import get_rook_valid_squares
from piece_movement_rules import get_bishop_valid_squares
from piece_movement_rules import get_queen_valid_squares
from piece_movement_rules import get_king_valid_squares
from piece_movement_rules import get_pawn_valid_squares
from piece_movement_rules import get_knight_valid_squares
from piece_movement_rules import get_piece_valid_squares


class EngineTest(T.TestCase):
	def test_sq_to_index(self):
		assert sq_to_index("a1") == (7, 0)
		assert sq_to_index("h1") == (7, 7)
		assert sq_to_index("a8") == (0, 0)
		assert sq_to_index("h8") == (0, 7)

	def test_index_to_sq(self):
		assert index_to_sq(7, 0) == "a1"
		assert index_to_sq(7, 7) == "h1"
		assert index_to_sq(0, 0) == "a8"
		assert index_to_sq(0, 7) == "h8"

	def test_board_color(self):
		board = Board()
		row, col = sq_to_index("b1")
		assert board.get_color(row, col) == "W"
		row, col = sq_to_index("e7")
		assert board.get_color(row, col) == "B"

	def test_rook_valid_squares(self):
		board = Board()
		row, col = sq_to_index("a1")
		assert get_rook_valid_squares(board, row, col, "WR") == []

	def test_bishop_valid_squares(self):
		board = Board()
		row, col = sq_to_index("c1")
		assert get_bishop_valid_squares(board, row, col, "WB") == []

	def test_queen_valid_squares(self):
		board = Board()
		row, col = sq_to_index("d1")
		assert get_queen_valid_squares(board, row, col, "WQ") == []

	def test_king_valid_squares(self):
		board = Board()
		row, col = sq_to_index("e1")
		assert get_king_valid_squares(board, row, col, "WK") == []

	def test_pawn_valid_squares(self):
		board = Board()
		row, col = sq_to_index("e2")
		assert sorted(get_pawn_valid_squares(board, row, col, "WP")) == ["e3", "e4"]

	def test_knight_valid_squares(self):
		board = Board()
		row, col = sq_to_index("b1")
		assert sorted(get_knight_valid_squares(board, row, col, "WN")) == ["a3", "c3"]

	def test_piece_valid_squares(self):
		board = Board()
		assert get_piece_valid_squares(board, "e1") == []
		assert get_piece_valid_squares(board, "a1") == []
		assert get_piece_valid_squares(board, "a8") == []
		assert sorted(get_piece_valid_squares(board, "e2")) == ["e3", "e4"]

if __name__ == "__main__":
	T.main()