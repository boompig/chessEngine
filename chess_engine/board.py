import sys
from typing import List, Tuple, Optional

PieceName = str
Color = str

E = "E"
G = "G"

WHITE = "W"
BLACK = "B"

PAWN = "P"
KNIGHT = "N"
BISHOP = "B"
ROOK = "R"
QUEEN = "Q"
KING = "K"

PIECES = frozenset([PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING])


# the default board, with guard regions
starter_board = [
    G, G, G, G, G, G, G, G, G, G,
    G, G, G, G, G, G, G, G, G, G,
    G, "r", "n", "b", "q", "k", "b", "n", "r", G,
    G, "p", "p", "p", "p", "p", "p", "p", "p", G,
    G, E, E, E, E, E, E, E, E, G,
    G, E, E, E, E, E, E, E, E, G,
    G, E, E, E, E, E, E, E, E, G,
    G, E, E, E, E, E, E, E, E, G,
    G, "P", "P", "P", "P", "P", "P", "P", "P", G,
    G, "R", "N", "B", "Q", "K", "B", "N", "R", G,
    G, G, G, G, G, G, G, G, G, G,
    G, G, G, G, G, G, G, G, G, G,
]


def get_piece_list(board: List[str], color: str) -> List[tuple]:
    """Return the mapping."""

    return [(index, piece) for index, piece in enumerate(board)
            if get_piece_color(piece) == color]


def index_to_sq(index: int) -> str:
    row, col = index_to_row_col(index)
    return "%s%d" % (chr(col + 97), 8 - row)


def index_to_row(index: int) -> int:
    return index // 10 - 2


def index_to_row_col(index):
    row = index_to_row(index)
    col = index % 10 - 1
    return (row, col)


def sq_to_row_col(sq: str) -> Tuple[int, int]:
    assert isinstance(sq, str)
    assert len(sq) == 2
    row = 8 - int(sq[1])
    col = ord(sq[0]) - 97
    return (row, col)


def sq_to_index(sq: str) -> int:
    """
    square is the square in UCI chess notation
    index is into into board array
    """
    assert isinstance(sq, str)
    assert len(sq) == 2
    row, col = sq_to_row_col(sq)
    return (row + 2) * 10 + col + 1


def is_valid_square(index):
    return starter_board[index] != G


def is_empty_square(board: list, index: int):
    return board[index] == E


def get_color(board, index):
    return get_piece_color(board[index])


def slide_index(index: int, dx: int, dy: int) -> int:
    assert isinstance(index, int)
    assert isinstance(dx, int)
    assert isinstance(dy, int)
    return index + (10 * dy) + dx


def get_castle_rook_index(board, from_index, to_index) -> Tuple[int, int]:
    """return (from_index, to_index) for the rook"""
    if from_index < to_index:
        # castle right (short)
        return slide_index(from_index, 3, 0), slide_index(from_index, 1, 0)
    else:
        # castle left (long)
        return slide_index(from_index, -4, 0), slide_index(from_index, -1, 0)


def move_piece_castle(board, from_index: int, to_index: int):
    # this should refer to the king only
    piece = board[from_index]
    assert get_raw_piece(piece) == KING
    board[from_index] = E
    board[to_index] = piece
    # find the rook and move it
    rook_from_index, rook_to_index = get_castle_rook_index(board, from_index, to_index)
    piece = board[rook_from_index]
    board[rook_from_index] = E
    board[rook_to_index] = piece


def move_piece(board, src: str, dest: str, promotion_piece: Optional[str] = None, is_castle=False):
    """No check on this.
    :param promotion: name of the promotion piece"""
    assert len(src) == 2
    assert isinstance(src, str)
    assert len(dest) == 2
    assert isinstance(dest, str)

    from_index = sq_to_index(src)
    to_index = sq_to_index(dest)
    if is_castle:
        move_piece_castle(board, from_index, to_index)
    elif promotion_piece:
        promotion_piece = promotion_piece.upper()
        assert promotion_piece in PIECES
        piece = board[from_index]
        color = get_piece_color(piece)
        assert get_raw_piece(piece) == PAWN
        assert index_to_row(to_index) in [0, 7]
        board[from_index] = E
        board[to_index] = get_piece_of_color(promotion_piece, color)
    else:
        piece = board[from_index]
        board[from_index] = E
        board[to_index] = piece


def get_piece_of_color(piece_name: str, color: str) -> str:
    return (piece_name.upper() if color == WHITE else piece_name.lower())


def load_board_from_file(board, fname="game.txt"):
    raise ValueError("Not implemented")


def get_piece_color(piece):
    if piece in set([E, G]):
        return None
    else:
        return (WHITE if piece.isupper() else BLACK)


def get_raw_piece(piece):
    return piece.upper()


def fen_to_board(fen):
    """Convert FEN to a row-array"""
    flat_arr = [G]

    for c in fen:
        if c.isdigit():
            for i in range(int(c)):
                flat_arr.append(E)
        elif c.isalpha():
            flat_arr.append(c)
        elif c == " ":
            # ignore the other info
            break
        elif c == "/":
            flat_arr.extend([G, G])

    flat_arr.append(G)
    assert len(flat_arr) == 80
    return ([G] * 20) + flat_arr + ([G] * 20)


def load_board(arr):
    # this is an array of arrays
    # each sub-array is a row
    # return a proper representation
    # I will mutate arr in place, beware!
    # treat empty strings as empties

    board = [G] * 20
    for row in arr:
        board.extend([G] + [(E if sq.rstrip() == "" else sq) for sq in row] + [G])
    board.extend([G] * 20)
    return board


def dump_board(board):
    """dump the board to a relatively simple array-based format"""
    simple_arr = [
        (" " if sq == E else sq) for sq in board
        if sq != G
    ]
    assert len(simple_arr) == 64
    # now split this up into sub-arrays by row
    rows = []
    for i in range(0, 64, 8):
        rows.append(simple_arr[i: i + 8])
    return rows


def print_board(board):
    print("*" * 18),
    for i, piece in enumerate(board):
        if not is_valid_square(i):
            continue
        if i % 10 == 1:
            print("")
            sq = index_to_sq(i)
            sys.stdout.write("%s " % sq[1])
        if piece == E:
            sys.stdout.write("  ")
        else:
            sys.stdout.write("%s " % piece)

    print("")
    sys.stdout.write("  ")
    for i in range(8):
        sys.stdout.write("%s " % (chr(i + 97)))
    print("")
    print("*" * 18)


def save_board(board, fname="game.txt"):
    with open(fname, "w") as fp:
        for i, sq in enumerate(board):
            if i % 10 == 0:
                fp.write("\n")
            fp.write(sq)


def is_capture(board, index, piece):
    """Return True iff the move is a capture.
    return squares
    index is the index to which piece is going, and piece is the source piece"""
    return get_color(board, index) is not None and get_color(board, index) != get_piece_color(piece)