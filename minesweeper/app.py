#!/usr/bin/env python
from json import dumps

from flask import Flask, request
from flask_restful import Api, Resource

from models import Game


app = Flask(__name__)
api = Api(app)

# We will have a dict until I implement persistence
_games = {}


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
            ret = game.to_dict()
        return ret

    def put(self, game_id):
        """Creates a game.

        Arguments:
            game_id -- unique id for a game.
        """
        # FIXME: the client setting the id of the new game is not the best idea
        # TODO: should validate something
        form = request.form
        game = Game(game_id, int(form['rows']), int(form['cols']),
                    int(form['mines']))
        game.init_cells()
        _games[game_id] = game
        return game.to_dict()


api.add_resource(GameResource, '/games/<game_id>')



if __name__ == '__main__':
    app.run(debug=True)
