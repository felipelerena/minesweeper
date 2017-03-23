from random import shuffle

from constants import (ACTION_CLICK, ACTION_FLAG, ACTION_QUESTION, EMPTY_CELL,
                       MINE)


class Game:

    """Represents a single game."""

    def __init__(self, uid, rows, cols, mines):
        """Constructor for the game class.

        Arguments:
            uid -- unique id for a game.
            rows -- the number of rows the grid will have.
            cols -- the number of columns the grid will have.
            mines -- how many mines we will like in the game.
        """
        self.id = uid
        self._num_rows = rows
        self._num_cols = cols
        # TODO: should validate the number of mines
        self._num_mines = mines

        self.is_over = False
        self._cells = None

    def to_dict(self):
        """Dict representation of the game."""
        cells = []
        for row in self._cells:
            cols = []
            for cell in row:
                cols.append(cell.to_dict(self.is_over))
            cells.append(cols)

        ret = {
            "game_id": self.id,
            "num_cols": self._num_cols,
            "num_rows": self._num_rows,
            "num_mines": self._num_mines,
            "cells": cells,
        }
        return ret

    def init_cells(self):
        """Create the cells for the board, add the mines, assign proximity."""
        # of course there must be a better, faster, nicer way to do this.
        rows = []
        # first we create the Cell objects for each cell of the board.
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                row.append(Cell(i, j))
            rows.append(row)
        self._cells = rows
        # I create the mines
        self._create_mines()
        # and asign the proximity number to the neighbor cells.
        self._fill_proximity()

    def _create_mines(self):
        """Place the mines on the board."""
        # there should be a better way to do this. I create a "key" list and
        # shuffle it, and use the first elements and put the mines
        places = []
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                places.append((i, j))

        shuffle(places)
        mines = places[:self._num_mines]
        for mine in mines:
            mine_cell = self._cells[mine[0]][mine[1]]
            mine_cell._proximity = MINE

    def _fill_proximity(self):
        """Assigns proximity number to the cells."""
        for row in self._cells:
            for cell in row:
                if not cell.is_mine:
                    self._fill_cell_proximity(cell)

    def _fill_cell_proximity(self, cell):
        """Assigns proximity number to a certain cell.

        Arguments:
            cell - a Cell instance.
        """
        neighbors = self.get_neighbor_cells(cell)
        proximity = 0

        # now we add the proximity and have the magic number
        for neighbor in neighbors:
            if neighbor.is_mine:
                proximity += 1

        cell._proximity = proximity

    def get_neighbor_cells(self, cell):
        """Get the neighbors for the clicked cell.

        Arguments:
            cell -- a Cell instance
        """
        neighbors = []
        # we get the index for the first and last columns of the neighbors
        first_col = cell.col - 1 if cell.col > 0 else cell.col
        last_col = cell.col + 2 if cell.col < self._num_rows else cell.col
        # if this is not the first line of the grid
        if cell.row > 0:
            neighbors += self._cells[cell.row-1][first_col:last_col]

        # if this is not the last line of the grid
        if cell.row < self._num_rows - 1:
            neighbors += self._cells[cell.row+1][first_col:last_col]

        # prev and next for this row
        if cell.col > 0:
            neighbors.append(self._cells[cell.row][cell.col-1])

        if cell.col < self._num_rows - 1:
            neighbors.append(self._cells[cell.row][cell.col+1])

        return neighbors

    def click_cell(self, row, col, action):
        """Performs the click action over the cell.

        Arguments:
            row -- the row number.
            col -- the column number.
            action -- the action performed by the click action.
        """
        cell = self._cells[row][col]
        # TODO: should show an error when already clicked?
        if not cell.clicked:
            if action == ACTION_FLAG:
                cell.flagged = True
            elif action == ACTION_QUESTION:
                cell.question = True
            elif action == ACTION_CLICK:
                cell.flagged = False
                cell.clicked = True
                if cell.is_mine:
                    self.end_game()
                elif cell.is_empty:
                    self.empty_cell_clicked(cell)
            else:
                cell.flagged = False
                cell.question = False

    def empty_cell_clicked(self, cell):
        """Propagates the viral click of the empty cells."""
        neighbors = self.get_neighbor_cells(cell)
        for neighbor in neighbors:
            self.click_cell(neighbor.row, neighbor.col, ACTION_CLICK)

    def end_game(self):
        self.is_over = True
        for row in self._cells:
            for cell in row:
                cell.flagged = False



class Cell:
    def __init__(self, row, col):
        """Constructor for the game class.

        Arguments:
            row -- the row where this cell is located.
            col -- the colum where this cell is located.
        """
        self.row = row
        self.col = col
        # proximity 0-9. the number of sorrounding mines. 9 is the mine. 0 means
        # "empty cell"
        self._proximity = EMPTY_CELL
        self.flagged = False
        self.question = False
        self.clicked = False

    @property
    def is_mine(self):
        return self._proximity == MINE

    @property
    def is_empty(self):
        return self._proximity == EMPTY_CELL

    def to_dict(self, force=False):
        """Dict representation of the cell.

        Arguments:
            force -- a boolean to always show the cell value.
        """
        ret = {
            "row": self.row,
            "col": self.col,
            "proximity": self._proximity if self.clicked or force else None,
            "flagged": self.flagged,
            "question": self.question,
            "is_mine": force and self.is_mine,
            "clicked": self.clicked,
        }
        return ret

    def __repr__(self):
        return "Cell R:{} C:{} - {}".format(self.row, self.col, self._proximity)

