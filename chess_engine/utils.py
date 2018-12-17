import logging


def opposite_color(col):
    return ("W" if col == "B" else "B")


def full_color_name(col):
    return ("white" if col == "W" else "black")


def setup_logging(verbose: bool):
    level = (logging.DEBUG if verbose else logging.INFO)
    logging.basicConfig(level=level)
