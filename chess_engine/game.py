#!/usr/bin/env python

import logging
from typing import List, Tuple


from .core.board import (get_color, index_to_sq, is_empty_square, move_piece,
                         print_board, sq_to_index, starter_board, WHITE, get_piece_of_color,
                         Color)
from .core.piece_movement_rules import get_piece_valid_squares, is_legal_move
from .core.utils import get_opposite_color


class Game(object):
    turn = WHITE
    moves = []  # type: List[str]

    @staticmethod
    def record_move(move: str):
        Game.moves.append(move)

    @staticmethod
    def flip_turn():
        Game.turn = get_opposite_color(Game.turn)


def get_piece_location(board, piece_name: str, color: Color) -> List[int]:
    piece = get_piece_of_color(piece_name, color)
    indexes = []
    try:
        start_index = 0
        while True:
            i = board.index(piece, start_index)
            indexes.append(i)
            start_index = i + 1
    except ValueError:
        # stop
        pass

    return indexes



def interpret_move(notation: str, board) -> Tuple[str, str]:
    """Return tuple (src, dest). Each is algebraic.
    Raises ValueError on improper notation."""

    if notation.upper() == "O-O" or notation.upper() == "O-O-O":
        raise ValueError("Castling is not yet implemented")
    elif "-" in notation:
        move = notation.split("-")
        assert len(move) == 2
        return (move[0], move[1])
    elif "x" in notation:
        move = notation.split("x")
        assert len(move) == 2
        return (move[0], move[1])
    else:
        if len(notation) == 2:
            # pawn move
            piece = "P"
            dest = notation
        elif len(notation) == 3:
            piece = notation[0].upper()
            dest = notation[1:].lower()
        else:
            raise ValueError("Cannot interpret this move: %s" % notation)

        logging.debug("Inferring move with piece %s to %s", piece, dest)
        dest_index = sq_to_index(dest)

        src_list = get_piece_location(board, piece, Game.turn)
        src_flag = None
        for src_idx in src_list:
            src = index_to_sq(src_idx)
            logging.debug("Trying piece at %s" % str(src))
            valid_sqs = get_piece_valid_squares(board, src_idx)
            if dest_index in valid_sqs:
                src_flag = src
                break

        if src_flag is None:
            raise ValueError("The piece %s cannot go to square %s" % (piece, dest))
        else:
            return (src_flag, dest)


def show_moves():
    for i in range(len(Game.moves)):
        if i % 2 == 0:
            print("%d. %s" % (i / 2 + 1, Game.moves[i]))
        else:
            print(Game.moves[i])
    if len(Game.moves) % 2:
        print("")
    print("")


def can_move_this_turn(board, index, turn):
    return get_color(board, index) == turn


def process_command(board, command: str):
    logging.debug("Received command %s" % command)

    if command == "q":
        logging.debug("Quitting")
        return 1
    elif command == "s":
        board.save()
        print("board saved")
        return
    elif command == "l":
        board.load()
        print("board loaded")
        return
    elif "-" in command or "x" in command:
        try:
            src, dest = interpret_move(command, board)
        except ValueError as e:
            print("E: %s" % str(e))
            return

        if len(src) != 2 or len(dest) != 2:
            print("E: Invalid src or dest")
            return
        else:
            logging.debug("Valid piece")

        src_idx, dest_idx = [sq_to_index(sq) for sq in [src, dest]]

        if is_empty_square(board, src_idx):
            print("E: %s is empty", src)
            return

        if not can_move_this_turn(board, src_idx, Game.turn):
            print("E: It is not your turn")
            return

        try:
            if is_legal_move(board, src_idx, dest_idx):
                move_piece(board, src_idx, dest_idx)
                Game.flip_turn()
                Game.record_move(command)
            else:
                print("%s is an illegal move", command)
        except ValueError as e:
            print("Error! %s" % str(e))
    else:
        i = sq_to_index(command)
        print(board[i])


def game_loop():
    board = starter_board

    while True:
        show_moves()
        print_board(board)
        print("Enter move as [src]-[dest], inspect square at [src], or q to quit")
        command = input(">> ")
        if command == "":
            continue

        exit_status = process_command(board, command.lower())
        if exit_status:
            return exit_status - 1

    return 0
