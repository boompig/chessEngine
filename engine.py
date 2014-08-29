import logging

from utils import opposite_color

from board import get_piece_list
from board import starter_board
from board import sq_to_index
from board import index_to_sq
from board import move_piece

from piece_movement_rules import _get_piece_valid_squares
from piece_movement_rules import is_in_checkmate


piece_scores = {
    "N": 3,
    "B": 3,
    "R": 5,
    "P": 1,
    "Q": 9,
    "K": 1000
}
CHECKMATE = 10000
MAX = 0
MIN = 1


def find_mate(board, color):
    """Return the winning move for the given color, in the given position."""

    return dls_minimax(board, 1, MAX, opposite_color(color))

def find_mate_in_two(board, color):
    """Return the winning sequence of moves by adopting a mini-max approach.
    Depth-limit to 2."""

    pass


def dls_minimax(board, limit, turn, target_player, last_move=None, depth=0):
    """Return whether or not there exists a winning combination of moves.
    Return this combination.
    target_player is the player being mated, not the one doing the mating"""

    color = (target_player if turn == MIN else opposite_color(target_player))
    logging.debug("Finding best move for player %s" % color)

    if is_in_checkmate(board, target_player):
        logging.debug("Reached terminal condition: found checkmate")
        return (CHECKMATE, [last_move])
    elif depth == limit:
        # once we reach the max depth, just return 0 for the score
        return (0, [last_move])
    elif turn == MAX:
        best_move = (-1 * CHECKMATE - 1, None)

        # score each potential move
        for (piece, src, dest) in gen_all_moves(board, color):
            logging.debug("Looking at move %s%s-%s" %
                    (piece[1], index_to_sq(src), index_to_sq(dest)))
            b_new = board[:]
            move_piece(b_new, src, dest)
            move = dls_minimax(b_new, limit, MIN, target_player, (piece, src, dest), depth + 1)
            if move[0] > best_move[0]:
                best_move = move

        if last_move is not None:
            best_move[1].insert(0, last_move)

        return best_move
    elif turn == MIN:
        best_move = (CHECKMATE + 1, None)
        # score each potential move
        for (piece, src, dest) in gen_all_moves(board, color):
            b_new = board[:]
            move_piece(b_new, src, dest)
            move = dls_minimax(b_new, limit, MAX, target_player, (piece, src, dest), depth + 1)
            if move[0] < best_move[0]:
                best_move = move

        if last_move is not None:
            best_move[1].insert(0, last_move)

        return best_move


def gen_all_moves(board, color):
    """Generate all valid moves by given color. This is a list."""
    moves = []

    for location, piece in get_piece_list(board, color):
        for dest in _get_piece_valid_squares(board, location):
            # the destination here is chess notation, rather than index
            moves.append( (piece, location, sq_to_index(dest)) )

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
