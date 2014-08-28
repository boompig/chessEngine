#!/usr/bin/env python

import logging

from utils import index_to_sq
from board import Board
from piece_movement_rules import is_legal_move
from piece_movement_rules import get_piece_valid_squares

moves = []

def interpret_move(notation, board):
	"""Return tuple (src, dest). Each is algebraic.
	Raises ValueError on improper notation."""

	if notation.upper() == "O-O" or notation.upper() == "O-O-O":
		raise ValueError("Castling is not yet implemented")
	elif "-" in notation:
		return notation.split("-")
	elif "x" in notation:
		return notation.split("x")
	else:
		if len(notation) == 2:
			# pawn move
			piece = "P"
			dest = notation
		elif len(notation) == 3:
			piece = notation[0].upper()
			dest = notation[1:].lower()
		else:
			raise ValueError("Cannot interpret this move: %s" % notation)

		logging.debug("Inferring move with piece %s to %s" % (piece, dest))

		src_list = board.get_piece_location(board.turn, board.turn + piece)
		src_flag = None
		for src in src_list:
			logging.debug("Trying piece at %s" % str(src))
			valid_sqs = get_piece_valid_squares(board, index_to_sq(*src))
			if dest in valid_sqs:
				src_flag = index_to_sq(*src)
				break

		if src_flag is None:
			raise ValueError("The piece %s cannot go to square %s" % (piece, dest))
		else:
			return (src_flag, dest)

def show_moves():
	for i in range(len(moves)):
		if i % 2 == 0:
			print "%d. %s" % (i / 2 + 1, moves[i]),
		else:
			print moves[i]

	if len(moves) % 2:
		print ""

	print ""

def process_command(board, command):
	logging.debug("Received command %s" % command)

	if command == "q":
		logging.debug("Quitting")
		return 1
	elif command == "s":
		board.save()
		return

	try:
		src, dest = interpret_move(command, board)
	except ValueError as e:
		print "E: %s" % e.message
		return

	if len(src) != 2 or len(dest) != 2:
		print "E: Invalid src or dest"
		return
	else:
		logging.debug("Valid piece")

	if board.get_piece(src) == Board.EMPTY:
		print "E: %s is empty" % src
		return

	if not board.can_move_this_turn(src):
		print "E: It is not your turn"
		return

	try:
		if is_legal_move(board, src, dest):
			board.move_piece(src, dest)
			board.flip_turn()
			moves.append(command)
		else:
			print "%s is an illegal move" % command
	except ValueError as e:
		print "Error! %s" % e.message

def game_loop():
	board = Board()

	while True:
		show_moves()
		board.show()
		print("Enter move as [src]-[dest], inspect square at [src], or q to quit")
		command = raw_input(">> ")

		exit_status = process_command(board, command.lower())
		if exit_status:
			return exit_status - 1

	return 0

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	exit(game_loop())