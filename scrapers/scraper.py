from multiprocessing.pool import ThreadPool

from scrapers.altomfotball.season import Season


class Scraper:

    @staticmethod
    def update_season(d):
        season_year = d[0]
        season = d[1]
        print("Starting %s" % season.title)

        season.get_teams()

        for idx, team in season.teams.items():
            team.get_players()

        season.get_matches()
        print("Ending %s" % season.title)

    @staticmethod
    def scrape():
        seasons = Season.get_seasons()
        pool = ThreadPool(8)
        results = pool.map(Scraper.update_season, list(seasons.items()))

        return seasons

