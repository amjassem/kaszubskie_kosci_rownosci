from flask import Flask
import pandas as pd


app = Flask(__name__)
scores = pd.DataFrame(index=[0, 1], columns=["A", "B"])


@app.route("/")
def index():
    return "<h1>Test App</h1>"


if __name__ == "__main__":
    app.run()
