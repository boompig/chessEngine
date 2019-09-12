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


def run_pgn(fname):
    _, moves = read_pgn_moves(fname)
    board = Board()

    for i, move in enumerate(moves):
        uci = move.uci()
        color = ("white" if i % 2 == 0 else "black")
        readable_move = board.get_normal_person_move(uci[:2], uci[2:4],
                                                     promotion=(uci[4].upper() if move.promotion else None)
        )
        print("{}. {} ({})".format(i // 2 + 1, readable_move, color))

        board.move_piece(uci[:2], uci[2:4], promotion=(uci[4].upper() if move.promotion else None))
        board.print()
    # and that's it
    return board


def test_weird_promotions():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1075750
    lots of weird promotions here
    """
    fname = "data/macdonnell_bird_1874.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_weird_promotions_2():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1075778
    lots of weird promotions here
    """
    fname = "data/wiede_goetz_1880.pgn"
    board = run_pgn(fname)
    assert board.is_in_checkmate(WHITE)


def test_stalemate():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1255706
    """
    fname = "data/stalemate.pgn"
    board = run_pgn(fname)
    assert board.is_in_stalemate(WHITE)


def test_kasparov_topalov():
    """Taken from here: http://www.chessgames.com/perl/chessgame?gid=1011478"""
    fname = "data/kasparov_topalov_1999.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_aronian_anand():
    """Taken from here: http://www.chessgames.com/perl/chessgame?gid=1451858"""
    fname = "data/aronian_anand_2007.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_anand_carlsen_2013_game_5():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1737319
    """
    fname = "data/carlsen_anand_2013_game_5.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_anand_carlsen_2013_game_6():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1737460
    """
    fname = "data/anand_carlsen_2013_game_6.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_anand_carlsen_2013_game_9():
    """
    Taken from here: http://www.chessgames.com/perl/chessgame?gid=1737896
    """
    fname = "data/anand_carlsen_2013_game_9.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_carlsen_bu_2017():
    """Taken from here: http://www.chessgames.com/perl/chessgame?gid=1884908"""
    fname = "data/carlsen_bu_xiangzhi_2017.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_carlsen_karjakin_2016_game_16():
    """Taken from: http://www.chessgames.com/perl/chessgame?gid=1848607
    This game is interesting because both players castle and it has en-passant"""
    fname = "data/carlsen_karjakin_2016_game_16.pgn"
    board = run_pgn(fname)
    assert (not board.is_in_checkmate(WHITE) and
            not board.is_in_checkmate(BLACK) and
            board.is_in_check(BLACK))


def test_carlsen_caruana_2018_game_13():
    """Taken from http://www.chessgames.com/perl/chessgame?gid=1937925
    """
    fname = "data/carlsen_caruana_2018.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)


def test_aronian():
    """from http://www.chessgames.com/perl/chessgame?gid=1399152"""
    fname = "data/aronian_anand_2007.pgn"
    board = run_pgn(fname)
    assert not board.is_in_checkmate(WHITE) and not board.is_in_checkmate(BLACK)
