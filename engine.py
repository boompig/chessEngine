import logging

from utils import opposite_color

from board import get_piece_list
from board import starter_board
from board import sq_to_index
from board import index_to_sq
from board import gen_successor
from board import dump_board
from board import get_color

from piece_movement_rules import _get_piece_valid_squares
from piece_movement_rules import is_legal_move
from piece_movement_rules import is_in_check
from piece_movement_rules import is_in_checkmate
from piece_movement_rules import _has_no_legal_moves


piece_scores = {
    "N": 3,
    "B": 3,
    "R": 5,
    "P": 1,
    "Q": 9,
    "K": 1000
}
CHECKMATE = 10000
CHECK = 5
MAX = True
MIN = False

#logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logging.basicConfig(level=logging.INFO, format="%(message)s")


def find_mate_in_n(board, color, n):
    """Find a mate in at most n moves. If no such mate exist, will return a
    non-CHECKMATE value in the first slot."""
    d = {"nodes_explored": 0}
    results = dls_minimax(board, (n - 1) * 2 + 1, MAX, opposite_color(color), stats_dict=d)
    print "nodes explored=%d" % d['nodes_explored']
    return results


def dls_minimax(board, depth_remaining, turn, target_player, last_move=None,
        alpha=(-1 * CHECKMATE - 1), beta=(CHECKMATE + 1), stats_dict={}):
    """Return whether or not there exists a winning combination of moves.
    Return this combination.
    target_player is the player being mated, not the one doing the mating
    TODO: alpha-beta this"""

    color = (target_player if turn == MIN else opposite_color(target_player))
    stats_dict['nodes_explored'] += 1

    if _has_no_legal_moves(board, color):
        if is_in_check(board, color):
            logging.info("Reached terminal condition: %s is in checkmate" % color)
            logging.debug("Previous move is %s" % str(last_move))

            for row in dump_board(board):
                logging.info(row)
            if turn == MIN:
                return (CHECKMATE, [last_move])
            else:
                return (-1 * CHECKMATE, [last_move])
        else:
            logging.debug("Reached terminal condition: %s is in stalemate" % color)
            return (0, [last_move])
    elif depth_remaining == 0:
        # once we reach the max depth, just return 0 for the score
        logging.debug("Max depth reached, exit 0")
        return (0, [last_move])
    elif turn == MAX:
        logging.debug("[%d] Finding best move for player %s" % (depth_remaining, color))
        best_move = [None]
        move_gen_flag = False

        def _score_move(move):
            return score_move(board, move[1], move[2])

        # score each potential move
        # order in order of score
        for (piece, src, dest) in sorted(gen_all_moves(board, color), key=_score_move, reverse=True):
            move_gen_flag = True
            logging.debug("[%d] Looking at move %s%s-%s" %
                    (depth_remaining, piece, index_to_sq(src), index_to_sq(dest)))
            b_new = gen_successor(board, src, dest)
            a, move = dls_minimax(b_new, depth_remaining - 1, MIN, target_player, (piece, src, dest), alpha, beta, stats_dict)
            if a > alpha:
                best_move = move
                alpha = a

            #TODO there should be some sort of theory on why this is good
            # but for now, the idea seems solid
            if alpha >= CHECKMATE:
                logging.info("Checkmate found, not checking any more nodes")
                break

            if alpha >= beta:
                logging.debug("beta cutoff for %s" % color)
                logging.debug("exceeded beta value %d with alpha %d" % 
                        (beta, alpha))
                break

        if not move_gen_flag:
            logging.debug("No moves generated, returning empty set")
            best_move = [None]

        if last_move is not None:
            best_move.insert(0, last_move)

        logging.debug("returning alpha=%d" % alpha)
        return (alpha, best_move)
    elif turn == MIN:
        logging.debug("[%d] Finding best move for player %s" % (depth_remaining, color))
        best_move = [None]
        move_gen_flag = False

        def _score_move(move):
            return score_move(board, move[1], move[2])

        # score each potential move
        # order in order of score
        for (piece, src, dest) in sorted(gen_all_moves(board, color), key=_score_move, reverse=True):
            move_gen_flag = True
            logging.debug("[%d] Looking at move %s%s-%s" %
                    (depth_remaining, piece, index_to_sq(src), index_to_sq(dest)))
            b_new = gen_successor(board, src, dest)
            b, move = dls_minimax(b_new, depth_remaining - 1, MAX, target_player, (piece, src, dest), alpha, beta, stats_dict)
            if b < beta:
                beta = b
                best_move = move

            if beta <= -CHECKMATE:
                logging.info("Checkmate found, not checking any more nodes")
                break

            if alpha >= beta:
                logging.debug("alpha cutoff")
                break
        if not move_gen_flag:
            logging.debug("No moves generated, returning empty set")
            best_move = [None]

        if last_move is not None:
            best_move.insert(0, last_move)

        logging.debug("Returning beta=%d" % beta)
        return (beta, best_move)


def gen_all_moves(board, color):
    """Generate all valid moves by given color. This is a list."""
    moves = []

    for location, piece in get_piece_list(board, color):
        for dest in _get_piece_valid_squares(board, location):
            if is_legal_move(board, index_to_sq(location), dest):
                # the destination here is chess notation, rather than index
                moves.append( (piece, location, sq_to_index(dest)) )

    return moves


def score_move(board, src, dest):
    """Score moves which give a check higher than those which do not."""
    moving_color = get_color(board, src)
    new_board = gen_successor(board, src, dest)
    if is_in_check(new_board, opposite_color(moving_color)):
        return CHECK
    else:
        return 0


def score_piece(piece, location):
    return piece_scores[get_raw_piece(piece)]


def score_board(board):
    """My heuristic for determining value of a position."""

    white_pts = sum([score_piece(piece, location)
                     for location, piece in get_piece_list(board, "W")])

    black_pts = sum([score_piece(piece, location) 
                     for location, piece in get_piece_list(board, "B")])

    return white_pts - black_pts
