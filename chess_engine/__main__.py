from argparse import ArgumentParser

from chess_engine.game import game_loop
from chess_engine.utils import setup_logging


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    setup_logging(verbose=args.verbose)
    exit(game_loop())
