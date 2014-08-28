import unittest as T

from utils import sq_to_index
from utils import index_to_sq
from board import Board

class BoardTest(T.TestCase):
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

	def test_in_check(self):
		board = Board()
		assert board.is_in_check("W") == False
		assert board.is_in_check("B") == False

	def test_move_pawn(self):
		board = Board()
		board.move_piece("e2", "e4")
		assert board.is_empty(*sq_to_index("e2"))
		assert board.get_piece("e4") == "WP"

		board.move_piece("e7", "e5")
		assert board.is_empty(*sq_to_index("e7"))
		assert board.get_piece("e5") == "BP"

	def test_move_knight(self):
		board = Board()
		board.move_piece("b1", "c3")
		assert board.is_empty(*sq_to_index("b1"))
		assert board.get_piece("c3") == "WN"

if __name__ == "__main__":
	T.main()