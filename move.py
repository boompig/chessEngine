from board import move_piece

class Move(object):
    def __init__(self, piece, src, dest, promotion=None, castle=None):
        self.piece = piece
        self.src = src
        self.dest = dest
        self.promotion = promotion
        self.castle = castle


def gen_successor(board_init, src, dest):
    board = board_init[:]
    move_piece(board, src, dest)
    return board

def gen_successor_from_move(board_init, move):
    return gen_successor(board_init, move.src, move.dest)
