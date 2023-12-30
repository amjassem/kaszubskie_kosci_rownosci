from flask import Flask, render_template, request, make_response, url_for
import secrets

from _state import GameState

from urllib import parse


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

game_state = GameState()

@app.route('/', methods=['GET'])
def index():
    player_name = parse.unquote(request.cookies.get('player_name') or "")
    if player_name:
        game_state.activate_player(player_name)

    return render_template(
        '_index.html',
        player_name=player_name,
        **game_state.__dict__)

@app.route('/forfeit/', methods=['POST'])
def forfeit():
    player_name = request.cookies.get("player_name")
    is_forfeit = game_state.submit_forfeit(player_name)
    if is_forfeit:
        txt = "Z Twoim głosem przepadła ostatnia nadzieja na rozwiązanie..."
    else:
        txt = "Może i Ty już się poddałeś, ale inni dalej walczą!"
    return txt

@app.route('/solution/', methods=['POST'])
def solution():
    player_name = request.cookies.get("player_name")
    game_state.submit_solution(player_name)
    return game_state.get_valid_response()


@app.route('/invalid/', methods=['POST'])
def invalid():
    return game_state.get_invalid_response()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

