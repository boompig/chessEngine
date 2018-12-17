# Chess Engine

## About

A basic command-line chess simulator and engine.
The goal of this project is to simply encapsulate the rules of chess, and to write a basic engine for it.
The quality of the engine, and representations of the data, are constantly evolving to accomodate new efficiency requirements.

## What Does That Mean?

This is super unstable and actively being worked on.

## How Good Is The Engine?

I have no idea. Let's benchmark it against a human!

## TODO

* Reduced reliance on strings, more power-of-two integers please!
* Smarter cloning of the board state
* More consistent use of notation vs. index. Use of index consistently in engine code and related representations
* UI?
* faster language than Python
* actual analytics/metrics, to figure out what is the slow part

## Design Choices (So Far)

### Board Representation

I currently represent the board as a flat array of pieces, empty spaces, and guard regions. This array contains 120 elements, and is meant to be viewed as a flattened matrix which is 12x10. The first and last 2 rows of this matrix contain only guard elements. The first and last element of each row are also guard elements. The 8x8 submatrix is the game board, where index (1, 1) of the submatrix is a8 on a chessboard. It is meant to be viewed as a board from the perspective of white.

Possible inefficiencies with this approach:
* ???

### Piece Representation

Pieces are represented as strings. Empty spaces are the empty string, guard regions are the string "G". Each piece is a single character - capital for white and lower-case for black. This is consistent with [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).

Possible inefficiencies:
* strings are large-ish in memory, compared to numbers. A lot of space can be saved with 6-bit numbers. 1 bit for the color, 1 bit for whether it is actually a guard element, 1 bit for whether it is actually an empty square, and 3 bits for the piece type (since there are only 6). Note that by being clever, we could also include guard and empty stuff into these first 3 bits, to get a 4-bit int.

Benefits:
* easy to think about

### Search Strategy

Currently doing depth-limited minimax with alpha-beta pruning. I will be switching over to [killer heuristic](https://en.wikipedia.org/wiki/Killer_heuristic) + [negamax](https://en.wikipedia.org/wiki/Negamax) as soon as I can find the bugs with existing code...
