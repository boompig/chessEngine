def sq_to_index(sq):
	"""Expects sq to be a 2-character string.
	First character is lower case [a-h], second character is number [1-8]"""

	# goal: A -> 0, H -> 7
	col = ord(sq[0]) - 97
	# black is at the top
	# goal: 1 -> 7, 8 -> 0
	row = 8 - int(sq[1])

	return (row, col)

def index_to_sq(row, col):
	pt1 = chr(col + 97)
	pt2 = 8 - row
	return "%s%d" % (pt1, pt2)

def is_valid_square(row, col):
	return 0 <= row and row < 8 and 0 <= col and col < 8


class Board(object):
	EMPTY = ""

	def __init__(self):
		self._board = [
			["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
			["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
			[ "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
			["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]
		]

		self._piece_map = {}
		for i, row in enumerate(self._board):
			for j, piece in enumerate(row):
				# could be 
				if not piece in self._piece_map:
					self._piece_map[piece] = []
				self._piece_map[piece].append( (i, j) )

	def is_empty(self, row, col):
		return self._board[row][col] == Board.EMPTY

	def show(self):
		print ("*" * 24)
		for row in self._board:
			for sq in row:
				if len(sq) != 2:
					print "  ",
				else:
					print sq,
			print ""
		print "  ".join([str(i + 1) for i in range(8)])
		print ("*" * 24)

	def get_color(self, row, col):
		piece = self._board[row][col]
		return (None if piece == Board.EMPTY else piece[0])

	def move_piece(self, src, dest):
		src_row, src_col = sq_to_index(src)
		dest_row, dest_col = sq_to_index(dest)

		piece = self._board[src_row][src_col]
		self._board[dest_row][dest_col] = piece
		self._board[src_row][src_col] = Board.EMPTY

if __name__ == "__main__":
	b = Board()
	b.show()
	b.move_piece("e2", "e4")
	b.show()