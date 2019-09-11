"""
This file makes sure that full chess games can be played
"""

import chess.pgn
from chess_engine import Board
from chess_engine.board import WHITE, BLACK


def read_pgn_moves(fname):
    with open(fname) as fp:
        first_game = chess.pgn.read_game(fp)
        return first_game.headers.get("Result"), first_game.mainline_moves()


def test_anand_carlsen_2013():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1737896
    """
    fname = "data/anand_carlsen_2013.pgn"
    result, moves = read_pgn_moves(fname)
    board = Board()

    for i, move in enumerate(moves):
        uci = move.uci()
        color = ("white" if i % 2 == 0 else "black")
        readable_move = board.get_normal_person_move(uci[:2], uci[2:4])
        print("{}. {} ({})".format(i // 2 + 1, readable_move, color))

        board.move_piece(uci[:2], uci[2:4], promotion=(uci[4] if move.promotion else None))
        board.print()

    # and that's it
    # note that white resigned at the end here without check or checkmate

    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)
