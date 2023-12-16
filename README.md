# KickStat
Uncover Rare events in Soccer from match data  

In the realm of football analytics, there is a critical need for a comprehensive system capable of identifying and analyzing rare, extraordinary events during matches. These rare events, which often hold key insights into player performance and match dynamics, remain hidden within vast datasets. Traditional analytics fall short in uncovering them. To address this challenge, our project aims to develop 'KickStat,' a sophisticated knowledge graph-based analytics system. KickStat will enable sports analysts to timely and effortlessly pinpoint and study rare occurrences in the world of soccer, enhancing our understanding of the game and offering valuable insights for sports analysts.   

Use the following commands to install the necessary libraries:

```pip install kuzu```

```pip install shutil```

```pip install import_ipynb```

Run the program while in the src directory with the command:

```python kickStatInterface.py```

You should see the folloiwng output:  

Which predetermined query are you interested in?  
1. Given a competition name, season name and a player name, where does he rank with respect to how many matches he is involved in?  
2. Given a competition name, season name and a team name, where does the team rank with respect to how many goals the team conceded?  
3. Given a competition name, season name, a team name and a stadium name, where does the team rank with respect to win-loss ratio?  
4. Given a competition name, season name and a player name, find out how many referees referred in the mathces he is involved in.  
5. Given a competition name, season name and a country name, how many teams in the season have managers from the same country?  
6. Given a player name, find out how many managers he worked with in the all available mathes.  
7. Given a competition name, season name and a player name, where does he rank with respect to how many events he is involved in?  
8. Given a competition name, season name and a player name, where does he rank with respect to how many goals he scored  
9. Given a competition name and season name, find the player with most cards received? (for a given player: count  
10. Given a competition name and season name, find if any players involved in a self goal  

When prompted, enter a number corresponding to the predetermined query you wish to execute, or -1 to exit.
From there you will be prompted to provide additional data, and then your chosen query will be executed and printed.
