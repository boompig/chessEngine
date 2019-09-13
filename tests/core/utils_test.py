from chess_engine.core.utils import get_opposite_color
from chess_engine.core.board import WHITE, BLACK


def test_opposite_color_W():
    assert get_opposite_color(WHITE) == BLACK


def test_opposite_color():
    assert get_opposite_color(BLACK) == WHITE
