from utils import sq_to_index
from utils import opposite_color
from utils import full_color_name

class Board(object):
	EMPTY = ""

	def __init__(self):
		self.turn = "W"
		self._board = [
			["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
			["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
			["", "", "", "", "", "", "", ""],
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

				color = piece[0]
				if not color in self._piece_map:
					self._piece_map[color] = {}
				# could be 
				if not piece in self._piece_map[color]:
					self._piece_map[color][piece] = []
				self._piece_map[color][piece].append( (i, j) )

	def get_piece_location(self, color, piece):
		"""Return list of locations for the piece."""

		return self._piece_map[color][piece]

	def get_piece(self, sq):
		row, col = sq_to_index(sq)
		return self._board[row][col]

	def is_empty(self, row, col):
		return self._board[row][col] == Board.EMPTY

	def is_in_check(self, color):

		return False

	def show(self):
		print "%s to move" % full_color_name(self.turn)
		print ("*" * 26)
		for i, row in enumerate(self._board):
			print "%d" % (8 - i),
			for sq in row:
				if len(sq) != 2:
					print "  ",
				else:
					print sq,
			print ""
		print "   " + "  ".join([chr(i + 97) for i in range(8)])
		print ("*" * 26)

	def save(self):
		with open("game.txt", "w") as fp:
			for row in self._board:
				fp.write("".join(row) + "\n")

	def get_color(self, row, col):
		piece = self._board[row][col]
		return (None if piece == Board.EMPTY else piece[0])

	def can_move_this_turn(self, sq):
		row, col = sq_to_index(sq)
		return self.get_color(row, col) == self.turn

	def flip_turn(self):
		self.turn = opposite_color(self.turn)

	def move_piece(self, src, dest):
		"""Move a piece. No validity check."""

		src_row, src_col = sq_to_index(src)
		dest_row, dest_col = sq_to_index(dest)

		# update board
		piece = self._board[src_row][src_col]
		self._board[dest_row][dest_col] = piece
		self._board[src_row][src_col] = Board.EMPTY

		# update piece map
		self._piece_map[piece[0]][piece].remove((src_row, src_col))
		self._piece_map[piece[0]][piece].append((dest_row, dest_col))

if __name__ == "__main__":
	b = Board()
	b.show()
	b.move_piece("e2", "e4")
	b.show()