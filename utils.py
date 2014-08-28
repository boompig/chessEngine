def sq_to_index(sq):
	"""Expects sq to be a 2-character string.
	First character is lower case [a-h], second character is number [1-8]"""
	col = ord(sq[0]) - 97
	row = 8 - int(sq[1])
	return (row, col)


def index_to_sq(row, col):
	pt1 = chr(col + 97)
	pt2 = 8 - row
	return "%s%d" % (pt1, pt2)


def is_valid_square(row, col):
	return 0 <= row and row < 8 and 0 <= col and col < 8


def opposite_color(col):
	return ("W" if col == "B" else "B")