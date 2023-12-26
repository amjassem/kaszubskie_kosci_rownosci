import numpy as np
import pandas as pd
import datetime as dt


VALUES = [1, 2, 3, 4, 5, 6]
ACTIVE_LIMIT = dt.timedelta(minutes=1)

INVALIDS = [
    "Yyy... No nie wydaje mi się.",
    "Czy aby na pewno?",
    "Czaisz o co chodzi w tej grze, nie?",
    "Te kości nie są sobie równe",
    "Spróbuj jeszcze raz",
    "Mam wątpliwości co do Twojego rozwiąznia..."
]

VALIDS = [
    "Świetnie układasz kości, jak prawdziwy Kaszub!",
    "No i po kłopocie, walniemy tabaczi?",
    "Co za rozwiązanie. Taki taktyk przyda nam się do walki z Kociewiakami.",
    "Abrahamowi aż się łezka zakręciła w oku.",
    "Jesteś jak zaklinacz kości!",
    "Twój spryt zna każdy od Pucka aż po Chojnice!"
]

class GameState:
    def __init__(self):
        self.draws = tuple(np.random.choice(VALUES, size=6))
        self.draws_id = hash(self.draws)
        self.img_html_0 = self.generate_image_html(0)
        self.img_html_1 = self.generate_image_html(1)
        self.img_html_2 = self.generate_image_html(2)
        self.img_html_3 = self.generate_image_html(3)
        self.img_html_4 = self.generate_image_html(4)

        self.fails = 0
        self.players = pd.DataFrame(columns=["Score", "Last_Active", "Forfeit_Vote"])
        self.scores_html = self.generate_scores_html()

    def new_roll(self):
        self.draws = tuple(np.random.choice(VALUES, size=6))
        self.draws_id = hash(self.draws)
        self.img_html_0 = self.generate_image_html(0)
        self.img_html_1 = self.generate_image_html(1)
        self.img_html_2 = self.generate_image_html(2)
        self.img_html_3 = self.generate_image_html(3)
        self.img_html_4 = self.generate_image_html(4)

    def generate_image_html(self, i: int) -> str:
        draw = self.draws[i]
        html = f'<div class="start-container" id=start{i} ondrop="drop(event)" ondragover="allowDrop(event)">\n'
        html += rf'    <img class="dice-img" id="image{i}" src="static\img\D{draw}.png" num-value="{draw}" image-id={i}'
        html += ' draggable="true" ondragstart="dragStart(event)">\n'
        html += '</div>\n'
        return html

    def activate_player(self, player_name: str):
        self.players.loc[player_name, "Last_Active"] = dt.datetime.now()
        self.scores_html = self.generate_scores_html()

    def submit_solution(self, player_name: str):
        score = self.players.loc[player_name, "Score"]
        if np.isnan(score):
            score = 0
        self.players.loc[player_name, "Score"] = score + 1

        self.new_roll()
        self.scores_html = self.generate_scores_html()

    def generate_scores_html(self):
        scores = self.players["Score"].sort_values()
        series = pd.concat([pd.Series(self.fails, index=["Porażki"]), scores.fillna(0)])
        html = series.to_frame().to_html(header=False)
        return html

    def submit_forfeit(self, player_name: str) -> bool:
        self.players.loc[player_name, "Forfeit_Vote"] = True
        sel_active = dt.datetime.now() - self.players["Last_Active"] < ACTIVE_LIMIT
        frac = self.players.loc[sel_active, "Forfeit_Vote"].sum() / sel_active.sum()

        if frac > 0.5:
            self.new_roll()

            self.fails += 1
            self.scores_html = self.generate_scores_html()
            return True
        else:
            return False

    def get_valid_response(self):
        return np.random.choice(VALIDS)

    def get_invalid_response(self):
        return np.random.choice(INVALIDS)
