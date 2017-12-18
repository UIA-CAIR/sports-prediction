from scrapers.altomfotball.season import Season
from multiprocessing.pool import ThreadPool

if __name__ == "__main__":
    print("Starting altomfotball.no scraper!")

    seasons = Season.get_seasons()

    def update_season(season):
        print("Starting %s" % season.title)

        season.get_teams()

        for idx, team in season.teams.items():
            team.get_players()

        season.get_matches()
        print("Ending %s" % season.title)

    pool = ThreadPool(8)
    results = pool.map(update_season, seasons)


