# KickStat
Uncover Rare events in Soccer from match data

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
conn.execute("CREATE REL TABLE MatchPartOfCompetition(FROM MatchNode TO Competition)")  
conn.execute("CREATE REL TABLE MatchHeldInSeason(FROM MatchNode TO Season)")  
conn.execute("CREATE REL TABLE StadiumCountry(FROM Stadium TO Country)")   
conn.execute("CREATE REL TABLE RefereeCountry(FROM Referee TO Country)")  
conn.execute("CREATE REL TABLE ManagerCountry(FROM Managers TO Country)")  
conn.execute("CREATE REL TABLE MatchCompetitionStage(FROM MatchNode TO CompetitionStage)") 
conn.execute("CREATE REL TABLE MatchHeldInStadium(FROM MatchNode TO Stadium)")   
conn.execute("CREATE REL TABLE MatchReferee(FROM MatchNode TO Referee)")  

Load data:  
conn.execute('COPY MatchNode FROM "matches.csv"')   
conn.execute('COPY Competition FROM "competition.csv"')  
conn.execute('COPY Season FROM "season.csv"')  
conn.execute('COPY Stadium FROM "stadium.csv"')  
conn.execute('COPY Country FROM "country.csv"') 
conn.execute('COPY Referee FROM "referee.csv"')  
conn.execute('COPY Managers FROM "managers.csv"')  
conn.execute('COPY CompetitionStage FROM "competition_stage.csv"')   
conn.execute('COPY MatchPartOfCompetition FROM "match_part_of_competition.csv"')   
conn.execute('COPY MatchHeldInSeason FROM "match_held_in_season.csv"')   
conn.execute('COPY StadiumCountry FROM "stadium_country.csv"')  
conn.execute('COPY RefereeCountry FROM "referee_country.csv"')  
conn.execute('COPY ManagerCountry FROM "manager_country.csv"')   
conn.execute('COPY MatchCompetitionStage FROM "match_competition_stage.csv"') 
conn.execute('COPY MatchHeldInStadium FROM "match_held_in_stadium.csv"')    
conn.execute('COPY MatchReferee FROM "match_referee.csv"')  

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
      
