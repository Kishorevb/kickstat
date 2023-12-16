# KickStat
Uncover Rare events in Soccer from match data

Use the following commands to install the necessary libraries:

```pip install kuzu```

```pip install shutil```

```pip install import_ipynb```

Follow the steps to define and populate KickStat Knowledge Base:

Import libraries:  

import kuzu  
import shutil 

Create an empty database and connect to it with Python API:  

shutil.rmtree("./knowledgebase", ignore_errors=True)  
db = kuzu.Database('./knowledgebase', buffer_pool_size=1024**3)  
conn = kuzu.Connection(db) 

Define the schema:  
conn.execute("CREATE NODE TABLE MatchNode(match_id INT64, match_date DATE, kick_off TIMESTAMP, home_score INT64, away_score INT64, match_status STRING, match_status_360 STRING, match_week INT64, PRIMARY KEY (match_id))")   
conn.execute("CREATE NODE TABLE Competition(competition_id INT64, country_name STRING, competition_name STRING, PRIMARY KEY (competition_id))")  
conn.execute("CREATE NODE TABLE Season(season_id INT64,season_name STRING, PRIMARY KEY (season_id))")  
conn.execute("CREATE NODE TABLE Stadium(id INT64, name STRING, PRIMARY KEY (id))")  
conn.execute("CREATE NODE TABLE Country(id INT64, name STRING, PRIMARY KEY (id))") 
conn.execute("CREATE NODE TABLE Referee(id INT64, name STRING, PRIMARY KEY (id))")  
conn.execute("CREATE NODE TABLE Managers(id INT64, name STRING, nickname STRING, dob DATE, PRIMARY KEY (id))")  
conn.execute("CREATE NODE TABLE CompetitionStage(id INT64, name STRING, PRIMARY KEY (id))")  
conn.execute("CREATE NODE TABLE Team(team_id INT64, team_name STRING, team_gender STRING, PRIMARY KEY (team_id))") 
conn.execute("CREATE REL TABLE MatchHomeTeam(FROM MatchNode TO Team, HomeTeamGroup STRING)")  
conn.execute("CREATE REL TABLE MatchAwayTeam(FROM MatchNode TO Team, AwayTeamGroup STRING)")  
conn.execute("CREATE REL TABLE TeamCountry(FROM Team TO Country)")  
conn.execute("CREATE REL TABLE TeamManagers(FROM Team TO Managers)")  
conn.execute("CREATE REL TABLE MatchPartOfCompetition(FROM MatchNode TO Competition)")  
conn.execute("CREATE REL TABLE MatchHeldInSeason(FROM MatchNode TO Season)")  
conn.execute("CREATE REL TABLE MatchHeldInStadium(FROM MatchNode TO Stadium)")  
conn.execute("CREATE REL TABLE StadiumCountry(FROM Stadium TO Country)")   
conn.execute("CREATE REL TABLE RefereeCountry(FROM Referee TO Country)")  
conn.execute("CREATE REL TABLE ManagerCountry(FROM Managers TO Country)")  
conn.execute("CREATE REL TABLE MatchCompetitionStage(FROM MatchNode TO CompetitionStage)")  
conn.execute("CREATE REL TABLE MatchReferee(FROM MatchNode TO Referee)")  
  
 

conn.execute("CREATE NODE TABLE Player(player_id INT64, player_name STRING, player_nickname STRING, PRIMARY KEY (player_id))")  
conn.execute("CREATE REL TABLE MatchPlayerPositions(FROM MatchNode TO Player, position_id INT64, position STRING, from_time STRING, to_time STRING, from_period INT64, to_period INT64, start_reason STRING, end_reason STRING)")  
conn.execute("CREATE REL TABLE MatchPlayers(FROM MatchNode TO Player, jersey_number INT64)")  
conn.execute("CREATE REL TABLE MatchPlayerCards(FROM MatchNode TO Player, time STRING, card_type STRING, reason STRING, period INT64)")  
conn.execute("CREATE REL TABLE PlayerCountry(FROM Player TO Country)")  
conn.execute("CREATE REL TABLE PlayerTeam(FROM Player TO Team)")  

conn.execute("CREATE NODE TABLE Event(event_id STRING, index INT64, period INT64, timestamp STRING, minute INT64, second INT64,\
type_id INT64, type_name STRING, possession INT64, play_pattern_id INT64, play_pattern_name STRING, position_id INT64, \
position_name STRING, location STRING, duration FLOAT, under_pressure BOOLEAN, off_camera BOOLEAN, out BOOLEAN, \
related_events STRING, bad_behaviour_card_id INT64, bad_behaviour_card_name STRING, PRIMARY KEY (event_id))")  
conn.execute("CREATE REL TABLE EventRelatedToPlayer(FROM Event TO Player)")  
conn.execute("CREATE REL TABLE EventRelatedToTeam(FROM Event TO Team)")  
conn.execute("CREATE REL TABLE EventPossessionTeam(FROM Event TO Team)")  

Load data:  
conn.execute('COPY MatchNode FROM "matches.csv"')   
conn.execute('COPY Competition FROM "competition.csv"')  
conn.execute('COPY Season FROM "season.csv"')  
conn.execute('COPY Stadium FROM "stadium.csv"')  
conn.execute('COPY Country FROM "country.csv"') 
conn.execute('COPY Referee FROM "referee.csv"')  
conn.execute('COPY Managers FROM "managers.csv"')  
conn.execute('COPY CompetitionStage FROM "competition_stage.csv"')   
conn.execute('COPY Team FROM "teams.csv"')  
conn.execute('COPY TeamCountry FROM "teams_country.csv"') 
conn.execute('COPY TeamManagers FROM "teams_managers.csv"') 
conn.execute('COPY MatchHomeTeam FROM "match_home_team.csv"') 
conn.execute('COPY MatchAwayTeam FROM "match_away_team.csv"')  
conn.execute('COPY MatchPartOfCompetition FROM "match_part_of_competition.csv"')   
conn.execute('COPY MatchHeldInSeason FROM "match_held_in_season.csv"')   
conn.execute('COPY MatchHeldInStadium FROM "match_held_in_stadium.csv"')  
conn.execute('COPY StadiumCountry FROM "stadium_country.csv"')  
conn.execute('COPY RefereeCountry FROM "referee_country.csv"')  
conn.execute('COPY ManagerCountry FROM "manager_country.csv"')   
conn.execute('COPY MatchCompetitionStage FROM "match_competition_stage.csv"') 
conn.execute('COPY MatchHeldInStadium FROM "match_held_in_stadium.csv"')    
conn.execute('COPY MatchReferee FROM "match_referee.csv"')  

conn.execute('COPY Player FROM "player.csv"')  
conn.execute('COPY MatchPlayerPositions FROM "match_player_positions.csv"')  
conn.execute('COPY MatchPlayers FROM "match_player.csv"')   
conn.execute('COPY MatchPlayerCards FROM "match_player_cards.csv"')   
conn.execute('COPY PlayerCountry FROM "player_country.csv"')   
conn.execute('COPY PlayerTeam FROM "player_team.csv"')    

conn.execute('COPY Event FROM "event.csv"')  
conn.execute('COPY EventRelatedToPlayer FROM "event_related_to_player.csv"')  
conn.execute('COPY EventRelatedToTeam FROM "event_relates_to_team.csv"')  
conn.execute('COPY EventPossessionTeam FROM "possession_team.csv"') 

Execute a simple query:  
results = conn.execute('MATCH (u:Competition) RETURN u.competition_id, u.country_name, u.competition_name;')  
while results.has_next():  
    print(results.get_next())  

Output:  
[11,Spain,La Liga]  
[116,North and Central America,North American League]  
[12,Italy,Serie A]  
[1238,India,Indian Super league]  
[1470,International,FIFA U20 World Cup]  
[16,Europe,Champions League]  
[2,England,Premier League]  
[35,Europe,UEFA Europa League]  
[37,England,FA Women's Super League]  
[43,International,FIFA World Cup]  
[49,United States of America,NWSL]  
[53,Europe,UEFA Women's Euro]  
[55,Europe,UEFA Euro]  
[7,France,Ligue 1]  
[72,International,Women's World Cup]  
[81,Argentina,Liga Profesional]  
[87,Spain,Copa del Rey]  
[9,Germany,1. Bundesliga]  
      
