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
        self._num_mines = mines

    def to_dict(self):
        ret = {
            "game_id": self.id,
            "num_cols": self._num_cols,
            "num_rows": self._num_rows,
            "num_mines": self._num_mines
        }

        return ret
