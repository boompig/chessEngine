import logging
import sys

from utils import opposite_color
from utils import full_color_name

#logging.basicConfig(level=logging.DEBUG)

E = "E"
G = "G"

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

def get_piece_list(board, color):
    """Return the mapping."""

    return [(index, piece) for index, piece in enumerate(board)
            if get_piece_color(piece) == color]


def index_to_sq(index):
    row, col = index_to_row_col(index)
    return "%s%d" % (chr(col + 97), 8 - row)


def index_to_row(index):
    return index / 10 - 2


def index_to_row_col(index):
    row = index_to_row(index)
    col = index % 10 - 1
    return (row, col)


def sq_to_row_col(sq):
    row = 8 - int(sq[1])
    col = ord(sq[0]) - 97
    return (row, col)


def sq_to_index(sq):
    row, col = sq_to_row_col(sq)
    return (row + 2) * 10 + col + 1


def is_valid_square(index):
    return starter_board[index] != G


def is_empty_square(board, index):
    return board[index] == E


def get_color(board, index):
    return get_piece_color(board[index])


def slide_index(index, dx, dy):
    return index + (10 * dy) + dx


def move_piece(board, src, dest):
    """No check on this."""
    piece = board[src]
    board[src] = E
    board[dest] = piece


def load_board_from_file(board, fname="game.txt"):
    raise ValueError("Not implemented")


def get_piece_color(piece):
    if piece in set([E, G]):
        return None
    else:
        return ("W" if piece.isupper() else "B")


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
    board.extend( [G] * 20 )
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
        rows.append( simple_arr[i: i + 8] )
    return rows


def print_board(board):
    print ("*" * 18),
    for i, piece in enumerate(board):
        if not is_valid_square(i):
            continue
        if i % 10 == 1:
            print ""
            sq = index_to_sq(i)
            sys.stdout.write("%s " % sq[1])
        if piece == E:
            sys.stdout.write("  ")
        else:
            sys.stdout.write("%s " % piece)

    print ""
    sys.stdout.write("  ")
    for i in range(8):
        sys.stdout.write("%s " % (chr(i + 97)))
    print ""
    print ("*" * 18)


def save_board(board, fname="game.txt"):
    with open(fname, "w") as fp:
        for i, sq in enumerate(board):
            if i % 10 == 0:
                fp.write("\n")
            fp.write(sq)


def gen_successor(board_init, move_src, move_dest):
    board = board_init[:]
    move_piece(board, move_src, move_dest)
    return board
