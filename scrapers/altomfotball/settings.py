
settings = {
    "tournament": 1,
    "year_limit": 1999
}
settings["api"] = {
    "season": {
        "list": "http://www.altomfotball.no/element.do?cmd=tournamentFixtures&tournamentId=%s&seasonId=241&month=all&useFullUrl=false" % settings["tournament"]

    },
    "teams": {
        "list": "http://www.altomfotball.no/elementsCommonAjax.do?cmd=table&tournamentId=" + str(settings["tournament"]) + "&seasonId=%s&subCmd=both&live=true&useFullUrl=false"
    },
    "player": {
        "list": "http://www.altomfotball.no/element.do?cmd=team&teamId=%s&tournamentId=" + str(settings["tournament"]) + "&seasonId=%s&useFullUrl=false"

    },
    "matches": {
        "list": "http://www.altomfotball.no/elementsCommonAjax.do?cmd=fixturesContent&tournamentId=" + str(settings["tournament"]) +"&seasonId=%s&month=all&useFullUrl=false"

    }
}
