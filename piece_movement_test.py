import unittest as T

from utils import sq_to_index
from utils import index_to_sq
from board import Board

from piece_movement_rules import get_rook_valid_squares
from piece_movement_rules import get_bishop_valid_squares
from piece_movement_rules import get_queen_valid_squares
from piece_movement_rules import get_king_valid_squares
from piece_movement_rules import get_pawn_valid_squares
from piece_movement_rules import get_knight_valid_squares
from piece_movement_rules import get_piece_valid_squares
from piece_movement_rules import is_legal_move
from piece_movement_rules import is_in_check


class PieceMovementTest(T.TestCase):

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

	def test_is_legal_pawn_move(self):
		board = Board()
		assert is_legal_move(board, "e2", "e3")
		assert is_legal_move(board, "e2", "e4")
		assert not is_legal_move(board, "e2", "e5")
		assert not is_legal_move(board, "e2", "f3")
		assert is_legal_move(board, "e7", "e6")
		assert is_legal_move(board, "e7", "e5")
		assert not is_legal_move(board, "e7", "e4")

	def test_is_in_check(self):
		board = Board()
		assert not is_in_check(board, "W")
		assert not is_in_check(board, "B")

if __name__ == "__main__":
	T.main()