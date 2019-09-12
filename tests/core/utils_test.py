from chess_engine.core.utils import opposite_color
from chess_engine.core.board import WHITE, BLACK


def test_opposite_color_W():
    assert opposite_color(WHITE) == BLACK


def test_opposite_color():
    assert opposite_color(BLACK) == WHITE
