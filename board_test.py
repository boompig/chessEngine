import unittest as T

from board import sq_to_index
from board import index_to_sq
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

if __name__ == "__main__":
	T.main()