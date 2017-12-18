from algorithms.Model1 import Model1
from scrapers.scraper import Scraper
import pickle
import os
import numpy as np

from settings import settings

if __name__ == "__main__":
    print("Starting altomfotball.no scraper!")

    data = None
    if not settings["use_pickle_model"]:
        scraper = Scraper.scrape()
        pickle.dump(scraper, open(os.path.join(os.getcwd(), "model.p"), "wb"))
        data = scraper
    else:
        data = pickle.load(open(os.path.join(os.getcwd(), "model.p"), "rb"))


    model = Model1()

    X_train = []
    Y_train = []
    X_test = []
    Y_test = []

    train_years = [x for x in range(2016, 2017)]
    test_years = [x for x in range(2017, 2018)]

    for year, season in data.items():
        if year not in train_years and year not in test_years:
            print("SKipping " + str(year))
            continue

        for match in season.matches:
            if match.is_played == False:
                continue

            is_training_data = True if match.date.year in train_years else False



            try:
                x = [
                    match.team_home.id,
                    match.team_away.id,
                    #data[year - 1]._get_team_by_id(match.team_home.id).team_stats[0].team_position, #match.team_home.team_stats[0].team_position,
                    #data[year - 1]._get_team_by_id(match.team_away.id).team_stats[0].team_position #match.team_away.team_stats[0].team_position
                ]
            except:
                continue

            if match.score_home > match.score_away:
                y = [1, 0, 0]
            elif match.score_home == match.score_away:
                y = [0, 1, 0]
            else:
                y = [0, 0, 1]


            #y = [match.score_home, match.score_away]

            if is_training_data:
                X_train.append(x)
                Y_train.append(y)
            else:
                X_test.append(x)
                Y_test.append(y)

    model.model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=8, epochs=5000, verbose=2)

    test_season = data[2017]
    for match in test_season.matches:
        team_home = season._get_team_by_id(match[0][0])
        team_away = season._get_team_by_id(match[0][1])
        predicted = model.model.predict(np.array([match[0]]))
        predicted = predicted[0]

        type = np.argmax(predicted)
        print(type)

        print(predicted, type)

        #print("%s | %s. runde | %s           %s-%s (%s-%s)            %s" % (match[2].date.date(), match[2].round, team_home.name, predicted[0], predicted[1], match[1][0], match[1][1], team_away.name))

