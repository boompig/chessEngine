from utils import opposite_color

from board import is_valid_square
from board import is_empty_square
from board import slide_index
from board import get_color
from board import sq_to_index
from board import index_to_sq
from board import index_to_row_col
from board import get_piece_list
from board import move_piece


def valid_and_empty(board, index):
    return is_valid_square(index) and is_empty_square(board, index)


def empty_or_capture(board, index, piece):
    return is_valid_square(index) and (
        is_empty_square(board, index) or is_capture(board, index, piece))


def is_capture(board, index, piece):
    return get_color(board, index) is not None and get_color(board, index) != piece[0]


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
            if piece[0] != get_color(board, index):
                squares.append(index)
            break

    return


def get_rook_valid_squares(board, index, piece):
    squares = []
    slide_and_check(board, index, piece, 0, 1, squares)
    slide_and_check(board, index, piece, 0, -1, squares)
    slide_and_check(board, index, piece, 1, 0, squares)
    slide_and_check(board, index, piece, -1, 0, squares)
    return [index_to_sq(index) for index in squares]


def get_bishop_valid_squares(board, index, piece):
    squares = []
    slide_and_check(board, index, piece, 1, 1, squares)
    slide_and_check(board, index, piece, 1, -1, squares)
    slide_and_check(board, index, piece, -1, 1, squares)
    slide_and_check(board, index, piece, -1, -1, squares)
    return [index_to_sq(index) for index in squares]


def get_queen_valid_squares(board, index, piece):
    squares = []
    squares.extend(get_rook_valid_squares(board, index, piece))
    squares.extend(get_bishop_valid_squares(board, index, piece))
    return squares


def get_king_valid_squares(board, index, piece):
    """This is easily parallelisable."""

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
        index_to_sq(index) for index in squares
        if empty_or_capture(board, index, piece)
    ]


def get_pawn_valid_squares(board, index, piece):
    d_row = (-1 if piece[0] == "W" else 1)
    row, col = index_to_row_col(index)

    l1 = [slide_index(index, 0, d_row)]
    if (row == 1 and piece[0] == "B") or (row == 6 and piece[0] == "W"):
        l1.append(slide_index(index, 0, 2 * d_row))

    # should be empty
    squares = [index for index in l1 if valid_and_empty(board, index)]
    l2 = [slide_index(index, 1, d_row), slide_index(index, -1, d_row)]
    # should be capture
    squares.extend(
        [index for index in l2 if valid_capture(board, index, piece)]
    )
    return [index_to_sq(index) for index in squares]


def get_knight_valid_squares(board, index, piece):
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
    
    return [index_to_sq(index) for index in squares
        if empty_or_capture(board, index, piece)
    ]


def _get_piece_valid_squares(board, index):
    piece = board[index]

    return {
        "N": get_knight_valid_squares,
        "R": get_rook_valid_squares,
        "Q": get_queen_valid_squares,
        "K": get_king_valid_squares,
        "P": get_pawn_valid_squares,
        "B": get_bishop_valid_squares
    }[piece[1]](board, index, piece)


def get_piece_valid_squares(board, sq):
    return _get_piece_valid_squares(board, sq_to_index(sq))


def is_legal_move(board, src, dest):
    """src and dest are squares, not indices.
    No turn checking."""
    src_idx = sq_to_index(src)
    dest_idx = sq_to_index(dest)

    if is_empty_square(board, src_idx):
        raise ValueError("There is no piece at square %s" % src)

    piece = board[src_idx]
    color = get_color(board, src_idx)

    if dest not in _get_piece_valid_squares(board, src_idx):
        return False

    # apply the move
    move_piece(board, src_idx, dest_idx)
    has_check = is_in_check(board, color)
    # undo the move
    move_piece(board, dest_idx, src_idx)
    return not has_check


def is_in_check(board, color):
    attacked_squares = set([])
    opp_color = opposite_color(color)
    # get everything for that color
    for index, piece in get_piece_list(board, opp_color):
        attacked_squares.update(
            _get_piece_valid_squares(board, index)
        )

    # find the king
    king_index = [
        index for index, piece in get_piece_list(board, color)
        if piece[1] == "K" 
    ][0]

    return index_to_sq(king_index) in attacked_squares
