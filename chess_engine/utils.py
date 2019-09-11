import logging
from .board import WHITE, BLACK


def opposite_color(col):
    return (WHITE if col == BLACK else BLACK)


def full_color_name(col):
    return ("white" if col == WHITE else "black")


def setup_logging(verbose: bool):
    level = (logging.DEBUG if verbose else logging.INFO)
    logging.basicConfig(level=level)
