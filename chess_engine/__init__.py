from typing import Optional

from .board import (get_raw_piece, is_empty_square, move_piece, print_board,
                    sq_to_index, starter_board)
from .piece_movement_rules import (is_castle_move, is_in_check, is_in_checkmate,
                                   is_in_stalemate, is_legal_move)


class MoveError(Exception):
    pass


class Board:

    def __init__(self, board=None):
        """
        Create a new board. By default, create board from starter
        """
        if board:
            self._board = board
        else:
            self._board = starter_board[:]

    def get_normal_person_move(self, from_square: str, to_square: str, promotion: Optional[str]) -> str:
        from_index = sq_to_index(from_square)
        to_index = sq_to_index(to_square)

        if is_castle_move(self._board, from_index, to_index):
            if to_index - from_index == 2:
                return "O-O"
            else:
                return "O-O-O"
        else:
            piece = get_raw_piece(self._board[from_index])
            s = ("-" if is_empty_square(self._board, to_index) else "x")
            if promotion:
                return "{piece}{from_square}{capture_or_move}{to_square}={promotion}".format(
                    piece=piece,
                    from_square=from_square,
                    to_square=to_square,
                    capture_or_move=s,
                    promotion=promotion
                )
            else:
                return "{piece}{from_square}{capture_or_move}{to_square}".format(
                    piece=piece,
                    from_square=from_square,
                    to_square=to_square,
                    capture_or_move=s
                )

    def move_piece(self, from_square: str, to_square: str, promotion: Optional[str]):
        if promotion:
            assert isinstance(promotion, str) and len(promotion) == 1
        from_index = sq_to_index(from_square)
        to_index = sq_to_index(to_square)

        if not is_legal_move(self._board, from_index, to_index):
            print_board(self._board)
            raise MoveError("cannot move piece from {} to {}".format(
                from_square, to_square
            ))

        is_castle = is_castle_move(self._board, from_index, to_index)
        move_piece(self._board, from_square, to_square, promotion_piece=promotion, is_castle=is_castle)
        return True

    def is_in_checkmate(self, color: str) -> bool:
        assert isinstance(color, str) and len(color) == 1
        return is_in_checkmate(self._board, color)

    def is_in_check(self, color: str) -> bool:
        assert isinstance(color, str) and len(color) == 1
        return is_in_check(self._board, color)

    def is_in_stalemate(self, color: str) -> bool:
        assert isinstance(color, str) and len(color) == 1
        return is_in_stalemate(self._board, color)

    def print(self):
        print_board(self._board)