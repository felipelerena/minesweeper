#!/usr/bin/env python
from json import dumps

from flask import Flask
from flask_restful import Api, Resource

from models import Game


app = Flask(__name__)
api = Api(app)

# We will have a dict until I implement persistence
_games = {}
_games["1"] = Game(1, 10, 10, 5)


class GameResource(Resource):
    """Manages a single game."""
    def get(self, game_id):
        """Get the game public data.

        Arguments:
            game_id -- the id for the game
        """
        ret = None
        game = _games.get(game_id)
        if game is not None:
            ret = {
                "game_id": game_id,
                "num_cols": game._num_cols,
                "num_rows": game._num_rows,
                "num_mines": game._num_mines
            }
        return ret


api.add_resource(GameResource, '/games/<game_id>')



if __name__ == '__main__':
    app.run(debug=True)
