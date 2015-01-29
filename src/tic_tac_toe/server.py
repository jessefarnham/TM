from flask import Flask, request, jsonify
from .engine import TicTacToe, Team


class DebugMode(object):
    DEBUG_MODE = False


def get_char(x):
    if x == 0:
        return '_'
    else:
        return Team(x).name


def encode_status(game):
    char_board = []
    for row in game.board:
        char_board.append([get_char(x) for x in row])
    return {'board': char_board,
            'turn': game.turn.name,
            'winning_team': game.winning_team,
            'game_over': game.game_over()}


class Game(object):
    game = TicTacToe()


app = Flask('tic_tac_toe')


def status():
    return jsonify(encode_status(Game.game))


@app.route('/ttt/new', methods=['POST'])
@app.route('/new', methods=['POST'])
def make_new_game():
    Game.game = TicTacToe()
    return status()


@app.route('/ttt/move', methods=['POST'])
@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    if Game.game.turn == Team.O:
        Game.game.mark_o(int(data['row']), int(data['col']))
    else:
        Game.game.mark_x(int(data['row']), int(data['col']))
    return status()


@app.route('/ttt/status')
@app.route('/status')
def get_status():
    return status()


@app.route('/')
def index():
    return app.send_static_file("html/index.html")


def main():
    DebugMode.DEBUG_MODE = True
    app.run(debug=True)


if __name__ == '__main__':
    main()
