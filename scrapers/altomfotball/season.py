import requests
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
import datetime

from scrapers.altomfotball.matches import Match
from scrapers.altomfotball.settings import settings
from scrapers.altomfotball.team import Team, TeamStats


class Season:

    def __init__(self, _id, title, year):
        self.title = title
        self.id = _id
        self.year = year
        self.teams = {}
        self.matches = []

    def get_teams(self):
        html = requests.get(settings["api"]["teams"]["list"] % self.id).content
        soup = BeautifulSoup(html, 'html.parser')

        for team_tr in soup.find(id="sd_table_wide").find("tbody").find_all("tr"):
            columns = team_tr.find_all("td")

            # Team data

            team_id = int(parse_qs(columns[1].find("a")["href"])["teamId"][0])
            team_name = columns[1].text.strip()


            """team_position = columns[0].text
            # Home
            team_home_total = columns[2].text
            team_home_wins = columns[3].text
            team_home_draw = columns[4].text
            team_home_loss = columns[5].text
            team_home_goals_for = columns[6].text
            team_home_goals_against = columns[7].text

            # Away
            team_away_total = columns[8].text
            team_away_wins = columns[9].text
            team_away_draw = columns[10].text
            team_away_loss = columns[11].text
            team_away_goals_for = columns[12].text
            team_away_goals_against = columns[13].text

            # Total
            team_total_total = columns[14].text
            team_total_wins = columns[15].text
            team_total_draw = columns[16].text
            team_total_loss = columns[17].text
            team_total_goals_for = columns[18].text
            team_total_goals_against = columns[19].text

            team_total_score = columns[20].text"""

            # Create Team
            team = Team(self, team_id, team_name)
            team_stats = TeamStats(
                team_position=columns[0].text,
                team_home_total=columns[2].text,
                team_home_wins=columns[3].text,
                team_home_draw=columns[4].text,
                team_home_loss=columns[5].text,
                team_home_goals_for=columns[6].text,
                team_home_goals_against=columns[7].text,
                team_away_total=columns[8].text,
                team_away_wins=columns[9].text,
                team_away_draw=columns[10].text,
                team_away_loss=columns[11].text,
                team_away_goals_for=columns[12].text,
                team_away_goals_against=columns[13].text,
                team_total_total=columns[14].text,
                team_total_wins=columns[15].text,
                team_total_draw=columns[16].text,
                team_total_loss=columns[17].text,
                team_total_goals_for=columns[18].text,
                team_total_goals_against=columns[19].text,
                team_total_score=columns[20].text,
            )
            team.team_stats.append(team_stats)

            self.teams[team.id] = team

    def _get_team_by_id(self, _id):
        return self.teams[_id]

    def get_matches(self):
        html = requests.get(settings["api"]["matches"]["list"] % self.id).content
        soup = BeautifulSoup(html, 'html.parser')

        most_recent_date = None
        for match_tr in soup.find(id="sd_fixtures_table").find("tbody").find_all("tr"):
            columns = match_tr.find_all("td")

            try:
                most_recent_date = datetime.datetime.strptime(columns[0].text.strip(), "%d.%m.%Y")
            except:
                pass

            round = int(columns[1].text.strip().split(".")[0])
            team_home = int(parse_qs(columns[3].find("a")["href"])["teamId"][0])
            team_away = int(parse_qs(columns[5].find("a")["href"])["teamId"][0])
            is_played = True
            score_home = None
            score_away = None
            match_id = int(parse_qs(columns[4].find("a")["href"])["matchId"][0])
            try:
                scores = columns[4].text.strip().replace(" ", "").split("-")
                score_home = int(scores[0])
                score_away = int(scores[1])
            except:
                is_played = False

            match = Match()
            match.id = match_id
            match.is_played = is_played
            match.team_home = self._get_team_by_id(team_home)
            match.team_away = self._get_team_by_id(team_away)
            match.round = round
            match.date = most_recent_date
            match.score_home = score_home
            match.score_away = score_away

            self.matches.append(match)
            match.team_home.matches.append(match)
            match.team_away.matches.append(match)

    @staticmethod
    def get_seasons():
        html = requests.get(settings["api"]["season"]["list"]).content
        soup = BeautifulSoup(html, 'html.parser')

        seasons = {}
        for season in soup.find(id="sd_drop_3").find_all("a"):
            s_title = season.text.strip()
            s_id = int(parse_qs(season["href"])["seasonId"][0])
            s_year = int(s_title.split(" ")[1])

            if s_year < settings["year_limit"]:
                continue

            # Create Season
            s = Season(s_id, s_title, s_year)
            seasons[s_year] = s

        return seasons


