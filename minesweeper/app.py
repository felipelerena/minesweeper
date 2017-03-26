#!/usr/bin/env python
from uuid import uuid1
from flask import Flask, request
from flask_restful import Api, Resource

from models import Game


app = Flask(__name__, static_folder="../client")
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

    def post(self):
        """Creates a game."""
        # TODO: should validate something
        form = request.json
        game_id = str(uuid1())
        game = Game(game_id, int(form['rows']), int(form['cols']),
                    int(form['mines']))
        game.init_cells()
        _games[game_id] = game
        return game.to_dict()


class CellResource(Resource):

    """Manages the game cell interaction."""

    def put(self, game_id, row, col):
        """Manages the user interaction with a cell.

        Arguments:
            game_id -- the game_id.
            row -- the cell row.
            col -- the cell col.
        """
        # TODO: should validate request
        form = request.json
        game = _games[game_id]
        game.click_cell(int(row), int(col), form["action"])
        return game.to_dict()

# adding the resources
api.add_resource(GameResource, '/games', endpoint="game")
api.add_resource(GameResource, '/games/<game_id>')
api.add_resource(CellResource, '/cells/<game_id>/<row>/<col>')


# static files, I would love to have the time to serve this somewhere else
app.add_url_rule('/static/<path:filename>', endpoint='static',
                 view_func=app.send_static_file)
@app.route('/')
def index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
