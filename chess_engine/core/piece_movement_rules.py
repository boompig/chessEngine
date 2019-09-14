import itertools
from typing import Iterator, List, Any

from .board import (BISHOP, BLACK, KING, KNIGHT, PAWN, QUEEN, ROOK, WHITE,
                    Board, Color, E, PieceName, find_king_index, get_color,
                    get_piece_color, get_piece_list, get_raw_piece,
                    index_to_col, index_to_row, is_capture, is_empty_square,
                    is_valid_square, slide_index, sq_to_index)
from .move import gen_successor
from .utils import get_opposite_color


def is_valid_and_empty(board: Board, index: int) -> bool:
    return is_valid_square(index) and is_empty_square(board, index)


def is_empty_or_capture(board: Board, index: int, piece: PieceName) -> bool:
    return is_valid_square(index) and (
        is_empty_square(board, index) or is_capture(board, index, piece))


def is_valid_en_passant(board: Board, from_index: int, to_index: int) -> bool:
    """
    This method only checks if the given pawn-capture move is a valid en-passant move

    NOTE: with current board representation it is impossible to check for en-passant completely accurately
    So this is a bit of a hack

    Assume:
    1. piece is pawn
    2. from_index and to_index are valid squares

    Avoiding these checks saves significant time in the engine
    """
    # assert is_valid_square(to_index)
    # assert get_raw_piece(board[from_index]) == PAWN

    if index_to_col(from_index) == index_to_col(to_index):
        # not a capture move
        return False

    # destination square must be empty, otherwise could not have moved pawn 2 squares on previous turn
    if not is_empty_square(board, to_index):
        return False

    piece = board[from_index]
    color = get_piece_color(piece)
    if color == WHITE:
        en_passant_dest_row = 6
        expected_target_pawn_index = slide_index(to_index, 0, -1)
    else:
        en_passant_dest_row = 3
        expected_target_pawn_index = slide_index(to_index, 0, 1)
    if index_to_row(to_index) != en_passant_dest_row:
        return False

    # this would be much easier if board had a list of previous moves
    # however this requires us to check that the expected square contains an opposite-colored pawn
    return (not is_empty_square(board, expected_target_pawn_index) and
            get_opposite_color(color) == get_piece_color(board[expected_target_pawn_index]) and
            get_raw_piece(board[expected_target_pawn_index]) == PAWN)


def is_valid_capture(board: Board, to_index: int, piece: PieceName) -> bool:
    """
    This method does not handle en-passant
    That is handled by its own method
    """
    return is_valid_square(to_index) and is_capture(board, to_index, piece)


def slide_and_check(board: Board, index: int, piece_color: Color, dy: int, dx: int) -> Iterator[int]:
    """Slide the given piece in the direction (dx, dy) from index.
    Return a generator over all the squares that the piece could visit, including captures, in that direction
    Extend squares array with valid squares.
    TODO, in the future, write this to be easily parallelisable"""
    while True:
        index = slide_index(index, dx, dy)

        if not is_valid_square(index):
            return
        if is_empty_square(board, index):
            yield index
        else:
            # logging.debug("square occupied by %s" % board[index])
            # logging.debug("attacking piece is %s" % piece)
            if piece_color != get_color(board, index):
                # this is a capture
                yield index
            return


def get_rook_valid_squares(board: Board, index: int) -> Iterator[int]:
    piece = board[index]
    color: Any = get_piece_color(piece)
    return itertools.chain(
        slide_and_check(board, index, color, 0, 1),
        slide_and_check(board, index, color, 0, -1),
        slide_and_check(board, index, color, 1, 0),
        slide_and_check(board, index, color, -1, 0)
    )


def get_bishop_valid_squares(board: Board, index: int) -> Iterator[int]:
    piece = board[index]
    color: Any = get_piece_color(piece)
    return itertools.chain(
        slide_and_check(board, index, color, 1, 1),
        slide_and_check(board, index, color, 1, -1),
        slide_and_check(board, index, color, -1, 1),
        slide_and_check(board, index, color, -1, -1)
    )


def get_queen_valid_squares(board: Board, index: int) -> Iterator[int]:
    return itertools.chain(
        get_rook_valid_squares(board, index),
        get_bishop_valid_squares(board, index)
    )


def get_king_valid_squares(board: Board, index: int) -> Iterator[int]:
    """This is easily parallelisable. """
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
    return (
        index for index in squares
        if is_empty_or_capture(board, index, piece)
    )


def get_pawn_valid_squares(board: Board, from_index: int) -> Iterator[int]:
    piece = board[from_index]
    dy = (1 if get_piece_color(piece) == WHITE else -1)
    row = index_to_row(from_index)

    # regular moves
    one_up_move = slide_index(from_index, 0, dy)
    if not is_valid_square(one_up_move):
        # if moving one up takes you off the board, then there's really no point checking the other squares
        return

    if is_empty_square(board, one_up_move):
        yield one_up_move

        color = get_piece_color(piece)
        if (row == 7 and color == BLACK) or (row == 2 and color == WHITE):
            two_up_move = slide_index(from_index, 0, 2 * dy)
            # always on the board, based on this check
            if is_empty_square(board, two_up_move):
                yield two_up_move

    # capture moves
    l2 = [slide_index(from_index, 1, dy), slide_index(from_index, -1, dy)]
    for to_index in l2:
        if is_valid_and_empty(board, to_index) and is_valid_en_passant(board, from_index, to_index):
            yield to_index
        elif is_valid_capture(board, to_index, piece):
            yield to_index


def get_knight_valid_squares(board: Board, index: int) -> Iterator[int]:
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
    return (index for index in squares
            if is_empty_or_capture(board, index, piece))


def get_piece_valid_squares(board: Board, from_index: int) -> Iterator[int]:
    piece = get_raw_piece(board[from_index])
    if piece == KNIGHT:
        return get_knight_valid_squares(board, from_index)
    elif piece == ROOK:
        return get_rook_valid_squares(board, from_index)
    elif piece == QUEEN:
        return get_queen_valid_squares(board, from_index)
    elif piece == KING:
        return get_king_valid_squares(board, from_index)
    elif piece == PAWN:
        return get_pawn_valid_squares(board, from_index)
    elif piece == BISHOP:
        return get_bishop_valid_squares(board, from_index)
    else:
        raise Exception("bad piece at index %d: %s" % (from_index, piece))


def is_castle_move(board: Board, from_index: int, to_index: int) -> bool:
    if (get_raw_piece(board[from_index]) != KING):
        return False
    potential_castle_squares = [
        slide_index(from_index, -2, 0),
        slide_index(from_index, 2, 0)
    ]
    return to_index in potential_castle_squares


def can_castle(board: Board, from_index: int, to_index: int) -> bool:
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
    if get_raw_piece(board[rook_square]) != ROOK:
        return False
    color = get_color(board, from_index)
    assert color is not None

    if get_color(board, rook_square) != color:
        return False

    if color == WHITE:
        if sq_to_index("e1") != from_index:
            return False
    else:
        if sq_to_index("e8") != from_index:
            return False

    if is_in_check(board, color):
        return False

    for idx in king_passes_squares:
        b2 = Board(board._board)
        piece = b2[from_index]
        b2[from_index] = E
        b2[idx] = piece
        if is_in_check(b2, color):
            return False
    return True


def is_legal_move(board: Board, from_index: int, to_index: int) -> bool:
    """
    This method checks whether the move is legal
    This includes checking whether the mover will be in check after making the move
    This function does not check whose turn it is"""
    assert not is_empty_square(board, from_index), \
        f"There is no piece at square {from_index}"
    assert is_valid_square(from_index), \
        f"Invalid source index: {from_index}"

    # piece = board[src]
    color = get_color(board, from_index)
    assert color is not None

    if is_castle_move(board, from_index, to_index):
        return can_castle(board, from_index, to_index)
    else:
        if to_index not in get_piece_valid_squares(board, from_index):
            return False

    return not is_in_check(gen_successor(board, from_index, to_index), color)


def is_in_check(board: Board, color: Color) -> bool:
    """
    Note that this function is expensive to compute
    Avoid calling it too many times
    """
    # find the king
    king_pos = find_king_index(board, color)

    opp_color = get_opposite_color(color)
    # get everything for that color
    for index, _ in get_piece_list(board, opp_color):
        for sq in get_piece_valid_squares(board, index):
            if sq == king_pos:
                return True
    return False


def _has_no_legal_moves(board: Board, color: Color) -> bool:
    """
    NOTE: this method is slow
    """
    for src_index, _ in get_piece_list(board, color):
        for dest_index in get_piece_valid_squares(board, src_index):
            next_board = gen_successor(board, src_index, dest_index)
            if not is_in_check(next_board, color):
                return False
    return True


def is_in_checkmate(board: Board, color: Color):
    """Criteria for checkmate:
    1. is in check
    2. no move will bring the player out of check
    """
    return is_in_check(board, color) and _has_no_legal_moves(board, color)


def is_in_stalemate(board: Board, color: Color):
    return not is_in_check(board, color) and _has_no_legal_moves(board, color)


def get_promotions(board: Board, src: int, dest: int) -> List[PieceName]:
    """Checks that the move is valid"""
    if not is_legal_move(board, src, dest):
        return []
    else:
        return _get_promotions(board[src], src, dest)


def _get_promotions(piece: PieceName, src: int, dest: int) -> List[PieceName]:
    """Does not check if the move is valid."""
    if get_raw_piece(piece) != PAWN:
        return []

    if get_piece_color(piece) == WHITE and index_to_row(dest) == 8:
        return ["Q", "B", "R", "N"]
    elif get_piece_color(piece) == BLACK and index_to_row(dest) == 1:
        return ["q", "b", "r", "n"]
    else:
        return []
