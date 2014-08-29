import unittest as T

from board import sq_to_index
from board import index_to_sq
from board import is_valid_square
from board import starter_board

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

if __name__ == "__main__":
	T.main()