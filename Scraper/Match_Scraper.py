# Standard libraries
import datetime
import json
import sys
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm




''' -------------------------------------------------- '''
#       Function will return all  season ids and the tournament id #
''' -------------------------------------------------- '''
def retrieve_season_ids(tournament_id):

    # URL Which contains <select> with all seasons
    link = "http://www.altomfotball.no/element.do?cmd=tournamentFixtures&tournamentId={0}&seasonId=241&month=all&useFullUrl=false".format(tournament_id)

    # Retrieve html
    html = requests.get(link).content

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    tournament_id = None
    season_ids = []

    parameter_list = [x["href"].split('?', 1)[-1].split("&") for x in soup.find(id="sd_drop_3").find_all("a")]
    for idx, param in enumerate(parameter_list):
        for idy, item in enumerate(param):
            split = item.split("=")

            if split[0] == "seasonId":
                season_ids.append(split[1])
            elif split[0] == "tournamentId":
                tournament_id = split[1]

    return tournament_id, season_ids




def create_match_urls(tournament_url):
    html = requests.get(tournament_url).content
    soup = BeautifulSoup(html, 'html.parser')

    match_urls = ["http://www.altomfotball.no/" + x["href"] for x in soup.find_all("a", "sd_fixtures_score")]
    return match_urls


def update_match_file(match_url_data):
    # Save match urls to file
    with open("./available-matches.json", "w") as file:
        json.dump(match_url_data, file)

def generate_match_urls():

    try:
        with open("./available-matches.json", "r") as file:
            match_url_data = json.loads(file.read())

            if len(match_url_data["urls"]) > 0 or match_url_data["state"] == "progress":
                print("Scraping is already under progress. Continuing from checkpoint")
                return match_url_data
    except:
        pass

    tournaments = {
        1: retrieve_season_ids(1),
        #2: retrieve_season_ids(2)
    }

    match_url_data = {
        "state": "init",
        "urls": []
    }

    i = 0
    for tournament_id, season_ids in tournaments.items():
        i += 1
        for j, season_id in enumerate(season_ids[1]):



            # Generate Tournament URL
            tournament_url = 'http://www.altomfotball.no/elementsCommonAjax.do?cmd=fixturesContent&tournamentId={0}&seasonId={1}&month=all&useFullUrl=false' \
                .format(tournament_id, season_id)

            match_url_data["urls"].extend(create_match_urls(tournament_url))
            print("Status: {0}/{1} @ {2}/{3} - Match count: {4}".format(j,len(season_ids[1])-1, i, len(tournaments),len(match_url_data["urls"])))

            #print(tournament_url)
            #for match_url in :
            #    print("\t" + match_url)


    # Save match urls to file
    update_match_file(match_url_data)

    print("Starting new scrape session")
    return match_url_data


def scrape_match(soup):

    # Date and time of match
    date = soup.find_all("td", "sd_game_away")[1]
    date_split = date.text.strip().split(",")
    date_time = datetime.datetime.strptime(date_split[1].strip(), "%d.%m.%Y kl. %H.%M") # Date and time of match

    # Home team
    home_team = soup.find_all("td", "sd_game_home")[0].text.strip()

    # Away team
    away_team = soup.find_all("td", "sd_game_away")[0].text.strip()

    # Stadium
    stadium_split = soup.find_all("td", "sd_game_home")[1].text.strip().split("Tilskuere: ")
    stadium = stadium_split[0].split("Kampen", 1)[0]

    # Match is not yet played
    if datetime.datetime.now() < date_time:
        return {
            "game_date": date_time,
            "home_team": home_team,
            "away_team": away_team,
            "home_score": None,
            "away_score": None,
            "home_halftime_score": None,
            "away_halftime_score": None,
            "stadium": stadium,
            "spectators": None,
            "result": None
        }

    # Match is played
    else:
        # Full Time Score
        score = soup.find_all("td", "sd_game_score")[0].text.strip().replace(":", "-").split("-")
        home_score = int(score[0])
        away_score = int(score[1])


        if "Avlyst" in score:
                return None

        half_time_score_soup = soup.find_all("td", "sd_game_score")[0]
        for tag in half_time_score_soup.find_all('small'):
            tag.replaceWith('')
        half_time_score_split= half_time_score_soup.text.strip().split("-")
        half_time_score_home = half_time_score_split[0]
        half_time_score_away = half_time_score_split[1]


        # Determine score type
        if home_score > away_score:
            result = "H"
        elif away_score > home_score:
            result = "B"
        else:
            result = "U"


        return {
            "game_date": date_time,
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "home_halftime_score": half_time_score_home,
            "away_halftime_score": half_time_score_away,
            "stadium": stadium,
            "result": result
        }



''' ----------------------------------------------------------------- '''
#       Saves the scores for each player in a table called match_setup. #
#       The table contains the matchid, and the ranking for each player #
#       Participating in the match                                      #
''' ----------------------------------------------------------------- '''

def get_match_information(soup, db_match):

        soup_html = soup

        try:
            rows = soup_html.find("table", {"class": "sd_table"}).find("tbody").find_all("tr")
        except:
            return

        del rows[len(rows) - 1]
        del rows[len(rows) - 1]
        dict_home = {}
        dict_away = {}

        for row in rows:
            cells = row.find_all("td")

            try:
                # Get home player in double list
                pid, vals = ex_match_info(1, cells)
                dict_home[pid] = vals

                # Get away player in double list
                pid, vals = ex_match_info(4, cells)
                dict_away[pid] = vals

            except IndexError:
                pass


        db_match["away_team_players"] = json.dumps(dict_away)
        db_match["home_team_players"] = json.dumps(dict_home)

        return






def ex_match_info(id, cells):
    pid = ''
    # Find matchid
    for url in cells[id].findAll('a', href=True):
        pid = (url['href'])

    # Parse matchid
    pid = pid.split('=')
    pid = pid[2].split('&')
    pid = pid[0]

    # Find value
    val = cells[id + 1].find('span')

    return pid, val.string








def run():
    tournament_blacklist = ["2"]

    total_time = 0.1

    # Generate all match urls
    match_url_data = generate_match_urls()
    num_items = len(match_url_data["urls"])
    for i in range(num_items):
        start_time = time.time()

        if i % 25 == 0:
            match_url_data["state"] = "progress"
            update_match_file(match_url_data)

        # Retrieve match item
        match_url = match_url_data["urls"].pop(0)
        parameter_list = {y.split("=")[0]: y.split("=")[1] for y in [x for x in match_url.split('?', 1)[-1].split("&")]}


        # Skip tournaments in blacklist
        if parameter_list["tournamentId"] in tournament_blacklist:
            continue


        # Check if match is already downloaded, IF yes. Use local else download
        import os.path
        cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Cache")
        match_dir = os.path.join(cache_dir, parameter_list["matchId"])
        has_cache = os.path.exists(match_dir)



        if not has_cache:
            os.makedirs(match_dir)

        if has_cache:
            try:
                match_html = open(match_dir + "/match" + ".html", "r").read()
                match_player_html = open(match_dir + "/player" + ".html", "r").read()
            except:
                print("Please restart the scraper. Files were missing from last crash!")
                os.rmdir(match_dir)
                sys.exit(0)
        else:
            # Retrieve html
            match_html = requests.get(match_url).content
            match_player_html = requests.get(
                    "http://www.altomfotball.no/"
                    "elementsCommonAjax.do?"
                    "cmd=match&"
                    "matchId={0}&"
                    "tournamentId={1}&"
                    "seasonId={2}&"
                    "subCmd=score&"
                    "useFullUrl=false"
                        .format(
                            parameter_list["matchId"],
                            parameter_list["tournamentId"],
                            parameter_list["seasonId"]
                    )).content

            with open(match_dir + "/match" + ".html", "wb+") as file:
                file.write(match_html)

            with open(match_dir + "/player" + ".html", "wb+") as file:
                file.write(match_player_html)

        # Parse HTML
        match_player_soup = BeautifulSoup(match_player_html, 'html.parser')
        match_soup = BeautifulSoup(match_html, 'html.parser')


        # Scrape match data
        match_data = scrape_match(match_soup)
        get_match_information(match_player_soup, match_data)

        print(match_data)






    # Update the match file to complete state
    match_url_data["state"] = "completed"
    update_match_file(match_url_data)











run()





