from typing import List

from .board import (get_color, get_piece_color, get_piece_list, get_raw_piece,
                    index_to_row, index_to_sq, is_capture, is_empty_square,
                    is_valid_square, print_board, slide_index, sq_to_index, E)
from .move import gen_successor
from .utils import opposite_color


def valid_and_empty(board, index):
    return is_valid_square(index) and is_empty_square(board, index)


def empty_or_capture(board, index, piece):
    return is_valid_square(index) and (
        is_empty_square(board, index) or is_capture(board, index, piece))


def valid_capture(board, index, piece):
    return is_valid_square(index) and is_capture(board, index, piece)


def slide_and_check(board, index, piece, d_row, d_col, squares):
    """Extend squares array with valid squares.
    TODO, in the future, write this to be easily parallelisable"""
    while True:
        index = slide_index(index, d_col, d_row)

        if not is_valid_square(index):
            break
        if is_empty_square(board, index):
            squares.append(index)
        else:
            # logging.debug("square occupied by %s" % board[index])
            # logging.debug("attacking piece is %s" % piece)
            if get_piece_color(piece) != get_color(board, index):
                squares.append(index)
            return


def get_rook_valid_squares(board, index: int) -> List[int]:
    piece = board[index]
    squares = []  # type: List[int]
    slide_and_check(board, index, piece, 0, 1, squares)
    slide_and_check(board, index, piece, 0, -1, squares)
    slide_and_check(board, index, piece, 1, 0, squares)
    slide_and_check(board, index, piece, -1, 0, squares)
    return squares


def get_bishop_valid_squares(board, index: int) -> List[int]:
    piece = board[index]
    squares = []  # type: List[int]
    slide_and_check(board, index, piece, 1, 1, squares)
    slide_and_check(board, index, piece, 1, -1, squares)
    slide_and_check(board, index, piece, -1, 1, squares)
    slide_and_check(board, index, piece, -1, -1, squares)
    return squares


def get_queen_valid_squares(board, index: int) -> List[int]:
    # piece = board[index]
    squares = []
    squares.extend(get_rook_valid_squares(board, index))
    squares.extend(get_bishop_valid_squares(board, index))
    return squares


def get_king_valid_squares(board, index: int) -> List[int]:
    """This is easily parallelisable. """
    assert isinstance(index, int)
    piece = board[index]
    squares = [
        slide_index(index, 1, -1),
        slide_index(index, 1, 0),
        slide_index(index, 1, 1),
        slide_index(index, 0, -1),
        slide_index(index, 0, 1),
        slide_index(index, -1, -1),
        slide_index(index, -1, 0),
        slide_index(index, -1, 1),
    ]

    # TODO, this does not check whether capture is possible by the king
    # this will be implemented later
    return [
        index for index in squares
        if empty_or_capture(board, index, piece)
    ]


def get_pawn_valid_squares(board, from_index: int, capture_only=False) -> list:
    assert isinstance(from_index, int)
    piece = board[from_index]

    d_row = (-1 if get_piece_color(piece) == "W" else 1)
    row = index_to_row(from_index)

    if capture_only:
        squares = []  # type: List[int]
    else:
        l1 = [slide_index(from_index, 0, d_row)]
        if (row == 1 and get_piece_color(piece) == "B") or (row == 6 and get_piece_color(piece) == "W"):
            l1.append(slide_index(from_index, 0, 2 * d_row))

        # should be empty
        squares = [i for i in l1 if valid_and_empty(board, i)]
    l2 = [slide_index(from_index, 1, d_row), slide_index(from_index, -1, d_row)]
    # should be capture
    squares.extend(
        [index for index in l2 if valid_capture(board, index, piece)]
    )
    return squares


def get_knight_valid_squares(board, index):
    piece = board[index]
    squares = [
        slide_index(index, 1, 2),
        slide_index(index, 1, -2),
        slide_index(index, -1, 2),
        slide_index(index, -1, -2),
        slide_index(index, 2, 1),
        slide_index(index, 2, -1),
        slide_index(index, -2, 1),
        slide_index(index, -2, -1),
    ]

    return [index for index in squares
            if empty_or_capture(board, index, piece)]


def _get_piece_valid_squares(board: list, from_index: int) -> List[int]:
    piece = get_raw_piece(board[from_index])
    if piece == "N":
        return get_knight_valid_squares(board, from_index)
    elif piece == "R":
        return get_rook_valid_squares(board, from_index)
    elif piece == "Q":
        return get_queen_valid_squares(board, from_index)
    elif piece == "K":
        return get_king_valid_squares(board, from_index)
    elif piece == "P":
        return get_pawn_valid_squares(board, from_index)
    elif piece == "B":
        return get_bishop_valid_squares(board, from_index)
    else:
        raise Exception("no such piece: %s" % piece)


def get_piece_valid_squares(board: list, sq: str):
    return _get_piece_valid_squares(board, sq_to_index(sq))


def is_castle_move(board, from_index: int, to_index: int) -> bool:
    assert isinstance(from_index, int)
    assert isinstance(to_index, int)
    if (get_raw_piece(board[from_index]) != "K"):
        return False
    potential_castle_squares = [
        slide_index(from_index, -2, 0),
        slide_index(from_index, 2, 0)
    ]
    return to_index in potential_castle_squares


def can_castle(board, from_index: int, to_index: int) -> bool:
    """
    Castling is quite complicated and I have not implemented all the rules
    1. The king must have never moved. Using the current arguments, there is no way to verify this
    2. The rook must have never moved. Using the current arguments, there is no way to verify this

    Note that the rook may pass through attacking squares. That's fine.
    Additionally the rook can move if it is under attack.

    Implement the following rules:
    1. Rook is on one of the two possible castle spots
    2. King is on the correct square
    3. Rook is the correct color
    4. Intermediate squares are empty
    5. Not in check
    6. King does not pass through checked squares and king is not in check at the end
    """

    # make sure the intermediate squares are empty
    check_squares = []  # type: List[int]
    # includes the final position
    king_passes_squares = []  # type: List[int]
    rook_square = -1
    if from_index < to_index:
        # castling right
        check_squares = [
            slide_index(from_index, 1, 0),
            slide_index(from_index, 2, 0),
        ]
        rook_square = slide_index(from_index, 3, 0)
        king_passes_squares = check_squares[:]
    else:
        # castling left
        check_squares = [
            slide_index(from_index, -1, 0),
            slide_index(from_index, -2, 0),
            slide_index(from_index, -3, 0),
        ]
        rook_square = slide_index(from_index, -4, 0)
        king_passes_squares = check_squares[:2]

    for square in check_squares:
        if not is_empty_square(board, square):
            return False
    if get_raw_piece(board[rook_square]) != "R":
        return False
    color = get_color(board, from_index)

    if get_color(board, rook_square) != color:
        return False

    if color == "W":
        if sq_to_index("e1") != from_index:
            return False
    else:
        if sq_to_index("e8") != from_index:
            return False

    if is_in_check(board, color):
        return False

    for idx in king_passes_squares:
        b2 = board[:]
        piece = b2[from_index]
        b2[from_index] = E
        b2[idx] = piece
        if is_in_check(b2, color):
            return False
    return True


def is_legal_move(board, from_index: int, to_index: int) -> bool:
    """No turn checking."""
    assert isinstance(from_index, int)
    assert isinstance(to_index, int)

    if is_empty_square(board, from_index):
        raise ValueError("There is no piece at square %s" % index_to_sq(from_index))

    # piece = board[src]
    color = get_color(board, from_index)

    if is_castle_move(board, from_index, to_index):
        return can_castle(board, from_index, to_index)
    else:
        if to_index not in _get_piece_valid_squares(board, from_index):
            return False

    has_check = is_in_check(gen_successor(board, from_index, to_index), color)
    return not has_check


def is_in_check(board, color):
    # find the king
    king_index = [
        index for index, piece in get_piece_list(board, color)
        if get_raw_piece(piece) == "K"
    ]
    if king_index == []:
        print_board(board)
        raise ValueError("King for color %s not present on board" % color)

    king_pos = king_index[0]

    opp_color = opposite_color(color)
    # get everything for that color
    for index, _ in get_piece_list(board, opp_color):
        vs = _get_piece_valid_squares(board, index)
        if king_pos in vs:
            return True

    return False


def _has_no_legal_moves(board, color):
    # get all possible moves
    for pos, _ in get_piece_list(board, color):
        # if the king cannot move regularly then it also cannot castle
        for dest in _get_piece_valid_squares(board, pos):
            b_new = gen_successor(board, pos, dest)
            if not is_in_check(b_new, color):
                return False

    return True


def is_in_checkmate(board, color):
    """Criteria for checkmate:
    1. is in check
    2. no move will bring the player out of check
    """
    return is_in_check(board, color) and _has_no_legal_moves(board, color)


def is_in_stalemate(board, color):
    return not is_in_check(board, color) and _has_no_legal_moves(board, color)


def get_promotions(board, src, dest):
    if not is_legal_move(board, src, dest):
        return []
    else:
        return _get_promotions(board[src], src, dest)


def _get_promotions(piece, src, dest):
    """Does not check if the move is valid."""
    if get_raw_piece(piece) != "P":
        return []

    if get_piece_color(piece) == "W" and index_to_row(dest) == 0:
        return ["Q", "B", "R", "N"]
    elif get_piece_color(piece) == "B" and index_to_row(dest) == 7:
        return ["q", "b", "r", "n"]
    else:
        return []
