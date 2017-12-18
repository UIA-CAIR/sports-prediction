# README #

A $$$$$$ maker machine

### Main repository for a get rich NN / Naive Bayes Machine. ###

* Nobody knows how it works
* It divides something by something and gets a number or some other fancy math stuff. Something about probability and neurons or something.
* It is advised to use this number to bet on a tippeliga match, to make money.

### DATABASE ###

**MATCH_SETUP**

Key | Val
------------- | -------------
matcid        | A unique key matching a specific match present in *db.match*
home_team     | A json-string (dictionary) containing the home players and their respective individual rank (integer) at the present time (matchday)
away_team     | Same as above, for the away team.

*Each player-id is queriable to the *db.players* table, with additional player information.*

**season_breakdown**

Key | Val
------------- | -------------
year          | The current season year
sum_matches   | Number of matches played this season
home_victory  | How many in percentage was won by the home-team decimal-percentage.
tied_victory  | How many of the matches was a tie, decimal percentage.
away_victory  | Hoe many of the matches was won by the away-team decimal percentage.
total_goals   | How many goals was scored this season
total_self_goals | How many of these goals was self-goals decimal percentage.
home_goal_percentage | How many of the goals belongs to the home-team.
away_goal_percentage | How many of the goals belongs to away team.
goals_average  | How many goals is average each match.
home_team_goal_breakdown | How many goals did the home-team score (avg) in decimal percentage py-list serialized json.
away_team_goal_breakdown| How many goals did the away team score (avg) in decimal percentage py-list serialized json.



### Who do I talk to? ###

* Ser helst du lar vær og snakke med noen.