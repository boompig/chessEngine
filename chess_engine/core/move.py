from typing import Optional

from .board import (PAWN, Board, PieceName, get_raw_piece, index_to_sq,
                    move_piece)


class Move(object):
    def __init__(self, piece: PieceName, src: int, dest: int,
                 promotion: Optional[PieceName] = None,
                 is_capture: bool = False,
                 is_castle: bool = False):
        """
        Move is saved together with metadata (is_capture, is_castle).
        This adds a little bit of overhead that is not entirely necessary
        It's nice for reconstructing what happened"""
        self.piece = piece
        self.src = src
        self.dest = dest
        self.promotion = promotion
        self.is_castle = is_castle
        self.is_capture = is_capture

    def show(self, board: Board) -> str:
        sym = ("x" if self.is_capture else "-")
        if self.promotion:
            return "{src}{move_or_capture}{dest}={promo}".format(
                src=index_to_sq(self.src),
                move_or_capture=sym,
                dest=index_to_sq(self.dest),
                promo=self.promotion
            )
        else:
            return "{piece}{src}{move_or_capture}{dest}".format(
                piece=("" if get_raw_piece(self.piece) == PAWN else self.piece),
                src=index_to_sq(self.src),
                move_or_capture=sym,
                dest=index_to_sq(self.dest),
            )


def gen_successor(board_init: Board, src: int, dest: int) -> Board:
    """Called by core-internal functions
    Don't bother updating other data structures in board_init
    """
    # create a copy of the board quickly
    board = Board(board_init._board)
    move_piece(board, src, dest)
    return board


def gen_successor_from_move(board_init: Board, move: Move) -> Board:
    board = gen_successor(board_init, move.src, move.dest)
    if move.promotion:
        # change the piece at dest into the correct piece
        board[move.dest] = move.promotion
    return board
