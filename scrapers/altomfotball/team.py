import requests
from bs4 import BeautifulSoup

from scrapers.altomfotball.player import Player
from scrapers.altomfotball.settings import settings
from urllib.parse import parse_qs

class TeamStats:

    def __init__(self,
                 team_position,
                 team_home_total,
                 team_home_wins,
                 team_home_draw,
                 team_home_loss,
                 team_home_goals_for,
                 team_home_goals_against,
                 team_away_total,
                 team_away_wins,
                 team_away_draw,
                 team_away_loss,
                 team_away_goals_for,
                 team_away_goals_against,
                 team_total_total,
                 team_total_wins,
                 team_total_draw,
                 team_total_loss,
                 team_total_goals_for,
                 team_total_goals_against,
                 team_total_score
                 ):
        self.team_position = team_position
        self.team_home_total = team_home_total
        self.team_home_wins = team_home_wins
        self.team_home_draw = team_home_draw
        self.team_home_loss = team_home_loss
        self.team_home_goals_for = team_home_goals_for
        self.team_home_goals_against = team_home_goals_against
        self.team_away_total = team_away_total
        self.team_away_wins = team_away_wins
        self.team_away_draw = team_away_draw
        self.team_away_loss = team_away_loss
        self.team_away_goals_for = team_away_goals_for
        self.team_away_goals_against = team_away_goals_against
        self.team_total_total = team_total_total
        self.team_total_wins = team_total_wins
        self.team_total_draw = team_total_draw
        self.team_total_loss = team_total_loss
        self.team_total_goals_for = team_total_goals_for
        self.team_total_goals_against = team_total_goals_against
        self.team_total_score = team_total_score

class Team:

    def __init__(self, season, team_id, team_name):
        self.season = season
        self.id = team_id
        self.name = team_name

        self.players = []
        self.team_stats = []
        self.matches = []

    def get_most_recent_stat(self):
        return self.team_stats[0]

    def get_players(self):
        html = requests.get(settings["api"]["player"]["list"] % (self.id, self.season.id)).content
        soup = BeautifulSoup(html, 'html.parser')

        for player_tr in soup.find(id="sd_players_table").find("tbody").find_all("tr"):
            columns = player_tr.find_all("td")


            player = Player()
            player.name = columns[1].text.strip()
            try:
                player.id = int(parse_qs(columns[1].find("a")["href"])["personId"][0])
            except Exception as e:
                player.id = -1
            player.position = columns[2].text.strip()
            score = columns[8].text.strip().replace(",", ".")
            goals = columns[5].text.strip()
            red_cards = columns[6].text.strip()
            yellow_cards = columns[7].text.strip()
            matches = columns[4].text.strip()
            player.matches = 0 if matches == "-" else int(matches)
            player.score = 0 if score == "-" else float(score)
            player.goals = 0 if goals == "-" else int(goals)
            player.red_cards = 0 if red_cards == "-" else int(red_cards)
            player.yellow_cards = 0 if yellow_cards == "-" else int(yellow_cards)

            self.players.append(player)




