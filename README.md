# KickStat
Uncover Rare events in Soccer from match data  

In the realm of football analytics, there is a critical need for a comprehensive system capable of identifying and analyzing rare, extraordinary events during matches. These rare events, which often hold key insights into player performance and match dynamics, remain hidden within vast datasets. Traditional analytics fall short in uncovering them. To address this challenge, our project aims to develop 'KickStat,' a sophisticated knowledge graph-based analytics system. KickStat will enable sports analysts to timely and effortlessly pinpoint and study rare occurrences in the world of soccer, enhancing our understanding of the game and offering valuable insights for sports analysts.   

Use the following commands to install the necessary libraries:

```pip install kuzu```

```pip install shutil```

```pip install import_ipynb```

Run the program while in the correct directory with the command:
```python kickStatInterface.py```

When prompted, enter a number corresponding to the predetermined query you wish to execute, or -1 to exit.
From there you will be prompted to provide additional data, and then your chosen query will be executed and printed.

Execute a sample query:  
results = conn.execute('MATCH (u:Competition) RETURN u.competition_id, u.country_name, u.competition_name;')  
while results.has_next():  
    print(results.get_next())  

Sample output:  
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
      
