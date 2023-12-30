from flask import Flask, render_template, request, make_response, url_for
import secrets

from _state import GameState

from urllib import parse


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/', methods=['GET'])
def index():

    return render_template(
        'index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

