from utils import sq_to_index

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
				if piece == Board.EMPTY:
					continue
				# could be 
				if not piece in self._piece_map:
					self._piece_map[piece] = []
				self._piece_map[piece].append( (i, j) )

	def get_piece(self, sq):
		row, col = sq_to_index(sq)
		return self._board[row][col]

	def is_empty(self, row, col):
		return self._board[row][col] == Board.EMPTY

	def is_in_check(self, color):

		return False

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