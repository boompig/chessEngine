import unittest as T

from chess_engine.utils import opposite_color


class UtilsTest(T.TestCase):
    def test_opposite_color_W(self):
        assert opposite_color("W") == "B"

    def test_opposite_color(self):
        assert opposite_color("B") == "W"


if __name__ == "__main__":
    T.main()
