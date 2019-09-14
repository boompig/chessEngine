import logging
from typing import Iterator, List, Optional, Tuple

from .core.board import (BISHOP, BLACK, KING, KNIGHT, PAWN, QUEEN, ROOK, WHITE,
                         Board, Color, PieceName, dump_board, get_color,
                         get_piece_list, get_raw_piece, is_capture)
from .core.move import Move, gen_successor, gen_successor_from_move
from .core.piece_movement_rules import (_get_promotions, _has_no_legal_moves,
                                        get_piece_valid_squares, is_in_check)
from .core.utils import get_opposite_color

piece_scores = {
    KNIGHT: 3,
    BISHOP: 3,
    ROOK: 5,
    PAWN: 1,
    QUEEN: 9,
    KING: 1000
}
CHECKMATE = 10000
CHECK = 5
MAX = True
MIN = False

logging.basicConfig(level=logging.INFO, format="%(message)s")


def gen_all_moves(board: Board, color: Color) -> Iterator[Move]:
    """Generate all valid moves by given color. This is a list."""
    for location, piece in get_piece_list(board, color):
        for dest in get_piece_valid_squares(board, location):
            next_board = gen_successor(board, location, dest)
            if not is_in_check(next_board, color):
                prs = _get_promotions(piece, location, dest)
                is_capture_move = is_capture(board, dest, piece)
                if prs != []:
                    for p in prs:
                        yield Move(piece, location, dest, promotion=p, is_capture=is_capture_move)
                else:
                    # the destination here is chess notation, rather than index
                    yield Move(piece, location, dest, is_capture=is_capture_move)


def find_mate_in_n(board: Board, color: Color, n: int, stats_dict: Optional[dict] = None):
    """Find a mate in at most n moves. If no such mate exist, will return a
    non-CHECKMATE value in the first slot."""
    if stats_dict is None:
        stats_dict = {}
    stats_dict.setdefault("nodes_explored", 0)
    results = dls_minimax(board, (n - 1) * 2 + 1, MAX, stats_dict=stats_dict)
    print("nodes explored=%d" % stats_dict['nodes_explored'])
    return results


def dls_minimax(board: Board, depth_remaining: int, turn: bool, last_move: Optional[Move] = None,
                alpha: int =(-1 * CHECKMATE - 1), beta=(CHECKMATE + 1),
                stats_dict: Optional[dict] = None) -> Tuple[int, list]:
    """Return whether or not there exists a winning combination of moves.
    Return this combination.
    TODO: alpha-beta this"""

    # color is the color of the player being mated
    color = (BLACK if turn == MIN else WHITE)
    if stats_dict:
        stats_dict['nodes_explored'] += 1

    if _has_no_legal_moves(board, color):
        if is_in_check(board, color):
            logging.info("[%d depth remaining] Reached terminal condition: %s is in checkmate", depth_remaining, color)
            logging.debug("Previous move is %s", str(last_move))

            for row in dump_board(board):
                logging.info(row)
            if turn == MIN:
                return (CHECKMATE, [last_move])
            else:
                return (-1 * CHECKMATE, [last_move])
        else:
            logging.debug("Reached terminal condition: %s is in stalemate", color)
            return (0, [last_move])
    elif depth_remaining == 0:
        # once we reach the max depth, just return 0 for the score
        logging.debug("Max depth reached, exit 0")
        return (0, [last_move])
    elif turn == MAX:
        logging.debug("[%d] Finding best move for player %s", depth_remaining, color)
        best_move = []  # type: List[Move]
        move_gen_flag = False

        def _score_move(move):
            return score_move(board, move)

        # score each potential move
        # order in order of score
        for g_move in sorted(gen_all_moves(board, color), key=_score_move, reverse=True):
            move_gen_flag = True
            logging.debug("[%d] Looking at move %s",
                          depth_remaining, g_move.show(board))
            b_new = gen_successor_from_move(board, g_move)
            a, move = dls_minimax(b_new, depth_remaining - 1, MIN, g_move, alpha, beta, stats_dict)
            if a > alpha:
                best_move = move
                alpha = a

            # TODO there should be some sort of theory on why this is good
            # but for now, the idea seems solid
            if alpha >= CHECKMATE:
                logging.info("[%d depth remaining] Checkmate found as MAX, not checking any more nodes", depth_remaining)
                break

            if alpha >= beta:
                logging.debug("beta cutoff for %s", color)
                logging.debug("exceeded beta value %d with alpha %d",
                              beta, alpha)
                break

        if not move_gen_flag:
            # this should be caught by first if statement
            raise Exception("No moves generated, returning empty set")

        if last_move is not None:
            best_move.insert(0, last_move)

        logging.debug("returning alpha=%d", alpha)
        return (alpha, best_move)
    elif turn == MIN:
        logging.debug("[%d depth remaining] Finding best move for player %s", depth_remaining, color)
        best_move = []
        move_gen_flag = False

        def _score_move(move):
            return score_move(board, move)

        # score each potential move
        # order in order of score
        for g_move in sorted(gen_all_moves(board, color), key=_score_move, reverse=True):
            move_gen_flag = True
            logging.debug("[%d] Looking at move %s",
                          depth_remaining, g_move.show(board))
            b_new = gen_successor_from_move(board, g_move)
            b, move = dls_minimax(b_new, depth_remaining - 1, MAX, g_move, alpha, beta, stats_dict)
            if b < beta or (b == beta and len(move) > len(best_move)):
                beta = b
                best_move = move

            if beta <= -1 * CHECKMATE:
                logging.info("[%d depth remaining] Checkmate found as MIN, not checking any more nodes", depth_remaining)
                break

            if alpha >= beta:
                logging.debug("alpha cutoff")
                break

        if not move_gen_flag:
            # this should be caught by first if statement
            raise Exception("No moves generated, returning empty set")

        if last_move is not None:
            best_move.insert(0, last_move)

        logging.debug("Returning beta=%d", beta)
        return (beta, best_move)
    raise Exception("should never get here - missing return statement")


def score_move(board: Board, move: Move):
    """Score moves which give a check higher than those which do not."""
    moving_color = get_color(board, move.src)
    new_board = gen_successor_from_move(board, move)
    if is_in_check(new_board, get_opposite_color(moving_color)):
        return CHECK
    else:
        return 0


def score_piece(piece: PieceName, location):
    return piece_scores[get_raw_piece(piece)]


def score_board(board):
    """My heuristic for determining value of a position."""

    white_pts = sum([score_piece(piece, location)
                     for location, piece in get_piece_list(board, WHITE)])

    black_pts = sum([score_piece(piece, location)
                     for location, piece in get_piece_list(board, "B")])

    return white_pts - black_pts
