import logging

from utils import opposite_color
from utils import full_color_name

logging.basicConfig(level=logging.DEBUG)

E = "E"
G = "G"

# the default board, with guard regions
starter_board = [
	G, G, G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G, G, G,
	G, "BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR", G,
	G, "BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP", G,
	G, E, E, E, E, E, E, E, E, G,
	G, E, E, E, E, E, E, E, E, G,
	G, E, E, E, E, E, E, E, E, G,
	G, E, E, E, E, E, E, E, E, G,
	G, "WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP", G,
	G, "WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR", G,
	G, G, G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G, G, G,
]

def get_piece_list(board, color):
	"""Return the mapping."""

	return [(index, piece) for index, piece in enumerate(board)
	        if piece[0] == color]


def index_to_sq(index):
	row, col = index_to_row_col(index)
	return "%s%d" % (chr(col + 97), 8 - row)


def index_to_row_col(index):
	row = index / 10 - 2
	col = index % 10 - 1
	return (row, col)


def sq_to_row_col(sq):
	row = 8 - int(sq[1])
	col = ord(sq[0]) - 97
	return (row, col)


def sq_to_index(sq):
	row, col = sq_to_row_col(sq)
	return (row + 2) * 10 + col + 1


def is_valid_square(index):
	return starter_board[index] != G


def is_empty_square(board, index):
	return board[index] == E


def get_color(board, index):
	if board[index] in set([E, G]):
		return None
	else:
		return board[index][0]


def slide_index(index, dx, dy):
	return index + (10 * dy) + dx


def move_piece(board, src, dest):
	"""No check on this."""

	piece = board[src]
	board[src] = E
	board[dest] = piece


def print_board(board):
	print ("*" * 25),
	for i, piece in enumerate(board):
		if not is_valid_square(i):
			continue
		if i % 10 == 1:
			print ""
			sq = index_to_sq(i)
			print sq[1],
		if piece == E:
			print "  ",
		else:
			print piece,

	print ""
	print " ",
	for i in range(8):
		print "%s " % (chr(i + 97)),
	print ""
	print ("*" * 25)


def save_board(board, fname="game.txt"):
	with open(fname, "w") as fp:
		for i, sq in enumerate(board):
			if i % 10 == 0:
				fp.write("\n")
			fp.write(sq)