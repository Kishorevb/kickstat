# KickStat
Uncover Rare events in Soccer from match data

Follow the steps to define and populate KickStat Knowledge Base:

Import library:  
import kuzu  

Create an empty database and connect to it with Python API:  
db = kuzu.Database('./knowledgebase')  
conn = kuzu.Connection(db)  

Define the schema:  
conn.execute("CREATE NODE TABLE Match(match_id INT64, match_date DATE, kick_off TIMESTAMP, home_score INT64, away_score INT64, match_status STRING, match_status_360 STRING, last_updated TIMESTAMP, last_updated_360 TIMESTAMP, match_week INT64, PRIMARY KEY (match_id))")  
conn.execute("CREATE NODE TABLE Competition(competition_id INT64, country_name STRING, competition_name STRING, PRIMARY KEY (competition_id))")  
conn.execute("CREATE NODE TABLE Season(season_id INT64,season_name STRING, PRIMARY KEY (season_id))")  
conn.execute("CREATE REL TABLE MatchPartOfCompetition(FROM Match TO Competition)")  
conn.execute("CREATE REL TABLE MatchHeldInSeason(FROM Match TO Season)")  

Load data:
conn.execute('COPY Match FROM "matches.csv"')  
conn.execute('COPY Competition FROM "competition.csv"')  
conn.execute('COPY Season FROM "season.csv"')  
conn.execute('COPY MatchPartOfCompetition FROM "match_part_of_competition.csv"')  
conn.execute('COPY MatchHeldInSeason FROM "match_held_in_season.csv"')  

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
      
