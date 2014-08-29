from board import get_piece_list
from board import starter_board
from board import sq_to_index
from board import index_to_sq
from board import move_piece

from piece_movement_rules import _get_piece_valid_squares


piece_scores = {
	"N": 3,
	"B": 3,
	"R": 5,
	"P": 1,
	"Q": 9,
	"K": 1000
}
CHECKMATE = 10000


def gen_all_moves(board, color):
	"""Generate all valid moves by given color. This is a list."""
	moves = []

	for location, piece in get_piece_list(board, color):
		for dest in _get_piece_valid_squares(board, location):
			# the destination here is chess notation, rather than index
			moves.append( (location, sq_to_index(dest), piece) )

	return moves


def apply_moves(board, moves):
	new_board = board[:]
	for move in moves:
		move_piece(new_board, move[0], move[1])

	return new_board


def score_piece(piece, location):
	return piece_scores[piece[1]]


def score_board(board):
	"""My heuristic for determining value of a position."""

	white_pts = sum([score_piece(piece, location) 
		             for location, piece in get_piece_list(board, "W")])

	black_pts = sum([score_piece(piece, location) 
		             for location, piece in get_piece_list(board, "B")])

	return white_pts - black_pts


if __name__ == "__main__":
	for move in sorted(gen_all_moves(starter_board, "W")):
		print "%s%s-%s" % (
			move[2][1],
			index_to_sq(move[0]),
			index_to_sq(move[1])
		)

		new_board = apply_moves(starter_board, [move])
		print score_board(new_board)

	#print score_board(starter_board)
