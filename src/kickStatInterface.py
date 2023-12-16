import kuzu
import shutil

import import_ipynb
from create_schema_and_populate_kb import *

SUBJECT_NONE = 0
SUBJECT_TEAM = 1
SUBJECT_PLAYER = 2
SUBJECT_MANAGER = 3
SUBJECT_EVENT = 4
SUBJECT_COUNTRY = 5
SUBJECT_COMPETITION = 6
SUBJECT_STADIUM = 7
SUBJECT_SEASON = 8

questions = ["Given a competition name, season name and a player name, where does he rank with respect to how many matches he is involved in?",
             "Given a competition name, season name and a team name, where does the team rank with respect to how many goals the team conceded?",
             "Given a competition name, season name, a team name and a stadium name, where does the team rank with respect to win-loss ratio?",
             "Given a competition name, season name and a player name, find out how many referees referred in the mathces he is involved in.",
             "Given a competition name, season name and a country name, how many teams in the season have managers from the same country?",
             "Given a player name, find out how many managers he worked with in the all available mathes.",
             "Given a competition name, season name and a player name, where does he rank with respect to how many events he is involved in?",
             "Given a competition name, season name and a player name, where does he rank with respect to how many goals he scored",
             "Given a competition name and season name, find the player with most cards received? (for a given player: count",
             "Given a competition name and season name, find if any players involved in a self goal"]


class QueryBuilder:
    def __init__(self, conn):
        self.conn = conn

    def setCompetition(self, val):
        if(self.validateInput(val, SUBJECT_COMPETITION)):
            self.competition = val
            return True
        return False

    def setSeason(self, val):
        self.season = val
        return True

    def setSubject(self, subject, subjectType):
        if(self.validateInput(subject, subjectType)):
            self.subject = subject
            self.subjectType = subjectType
            return True
        return False
    
    def validateInput(self, val, st):
        if typeString(st) == "UNEXPECTED TYPE":
            print("Subject type unexpected, cannot set\n")
            return False
        
        try:
            out = 0 != len(execute_and_return_result('MATCH (a:' + typeString(st).capitalize() + ') WHERE a.' + typeString(st) + '_name =~ "' + val + '" RETURN a'))
        except:
            out = 0 != len(execute_and_return_result('MATCH (a:' + typeString(st).capitalize() + ') WHERE a.name =~ "' + val + '" RETURN a')) 

        if not out:
            print('Value "' + val + '" was not found in "' + typeString(st).capitalize() +"'\n")
        
        return out

    def setColumns(self, columns=[]):
        if type(columns) == type([]):
            self.columns = columns

    def setHomeGames(self, val):
        self.homeGames = val

    def setAwayGames(self, val):
        self.awayGames = val

    def setStadium(self, val):
        if(self.validateInput(val, SUBJECT_STADIUM)):
            self.stadium = val
            return True
        return False
    
    def setCountry(self, val):
        if(self.validateInput(val, SUBJECT_COUNTRY)):
            self.country = val
            return True
        return False
    
    def getCompetition(self):
        return self.competition
    
    def getSubject(self):
        return self.subject
    
    def getSeason(self):
        return self.season
    
    def getStadium(self):
        return self.stadium
    
    def getCountry(self):
        return self.country


    def __str__(self):
        s = "Competition: " + self.competition
        s += "\nSeason(s): " + str(self.startSeason)

        if self.endSeason > 0:
            s += "-"+str(self.endSeason)
        s+="\n"+typeString(self.subjectType).capitalize()+": "+self.subject

        if hasattr(self, 'stadium'):
            s+="\nStadium: "+self.stadium
        
        if hasattr(self, 'country'):
            s+="\nCountry: "+self.country

        return s


def typeString(i):
    if i==0: return "none"
    elif i==1: return "team"
    elif i==2: return "player"
    elif i==3: return "manager"
    elif i==4: return "event"
    elif i==5: return "country"
    elif i==6: return "competition"
    elif i==7: return "stadium"
    else: return "UNEXPECTED TYPE"

def displayList(st):
    try:
        execute_and_print_result('MATCH (a:' + typeString(st).capitalize() + ') RETURN DISTINCT a.' + typeString(st) + '_name')
    except:
        execute_and_print_result('MATCH (a:' + typeString(st).capitalize() + ') RETURN DISTINCT a.' + 'name')
    print("\n")

def validateInput(userIn, st):
    try:
        vals = execute_and_return_result('MATCH (a:' + typeString(st).capitalize() + ') WHERE a.' + typeString(st) + '_name =~ "' + userIn + '" RETURN a')
    except:
        vals = execute_and_return_result('MATCH (a:' + typeString(st).capitalize() + ') WHERE a.' + typeString(st) + ' =~ "' + userIn + '" RETURN a')

    print(len(vals) != 0)

def userInput():
    inComp = "" 
    inSeason = [0,0]
    inSubject = ""
    inType = SUBJECT_NONE
    homeGames = False
    awayGames = False

    shutil.rmtree("./knowledgebase", ignore_errors=True)
    db = kuzu.Database('./knowledgebase', buffer_pool_size=1024**3)
    conn = kuzu.Connection(db)

    print("What competition are you interested in?")
    inComp = input()

    print("Which season(s) are you interested in?")
    print("Start year:")
    inSeason[0] = int(input())
    print("End year (or 0 for one season)")
    inSeason[1] = int(input())

    print("""Are you interested in a specific: 
          \t1. Team
          \t2. Player
          \t3. Manager
          \t4. Event type
          \t5. Country""")
    inType = int(input())

    print("Which " + typeString(inType) + " are you interested in?")
    inSubject = input()
    if inType == 1 or inType == 2 or inType == 3:
        print("Are you interested in: \n\t1. Home games only\n\t2. Away games only\n\t3. All games")
        inHomeAway = int(input())
        homeGames = inHomeAway == 1 or inHomeAway == 3
        awayGames = inHomeAway == 2 or inHomeAway == 3

    qb = QueryBuilder(conn)
    qb.setCompetition(inComp)
    qb.setSeasons(inSeason[0], inSeason[1])
    qb.setSubject(inSubject, inType)
    qb.setHomeGames(homeGames)
    qb.setAwayGames(awayGames)
    
    if(printInput):
        print("Competition: "+ inComp)
        if inSeason[1] == 0: print("Season: " + inSeason[0])
        else: print("Seasons " + str(inSeason[0]) + "-" + str(inSeason[1]))
        print("Interest: " + inSubject)
        print("Interest Type: " + typeString(inType).capitalize())
        if homeGames or awayGames: print("Home games: " + str(homeGames) + ", Away games: " + str(awayGames))

    return qb

def userInputSetQueries():
    inComp = "" 
    inStartSeason = 0
    inEndSeason = 0
    inStadium = ""
    inCountry = ""
    inSubject = ""
    inType = SUBJECT_NONE
    homeGames = False
    awayGames = False
    inQuestion = -1


    shutil.rmtree("./knowledgebase", ignore_errors=True)
    db = kuzu.Database('./knowledgebase', buffer_pool_size=1024**3)
    conn = kuzu.Connection(db)
    qb = QueryBuilder(conn)
    userIn = 0

    print("Which predetermined query are you interested in?")
    for i in range(len(questions)):
        print(""+str(i+1)+". "+questions[i])

    print("\nEnter -1 to exit program\n")

    userIn = int(input())
    if userIn == -1:
        return qb, -1
    
    inQuestion = userIn

    print("\n(At prompts asking for a name, enter \"-l\" to display list of valid names)\n")

    while True:
        if inQuestion != 6:
            print("Which competition are you interested in?")
            userIn = input()
            if userIn.lower() == "-l":
                displayList(SUBJECT_COMPETITION)
                userIn = input()

            if not qb.setCompetition(userIn): continue

            print("Which season? (start year/year after, ie \"2015/2016\")")
            qb.setSeason(input())

        if inQuestion in [1, 4, 6, 7, 8]:
            print("Which player are you interested in?")

            userIn = input()
            if userIn.lower() == "-l":
                displayList(SUBJECT_PLAYER)
                userIn = input()


            if not qb.setSubject(userIn, SUBJECT_PLAYER): continue

        else:
            print("Which team are you interested in?")

            userIn = input()
            if userIn.lower() == "-l":
                displayList(SUBJECT_TEAM)
                userIn = input()

            if not qb.setSubject(userIn, SUBJECT_TEAM): continue
        
        if inQuestion == 3:
            print("Which stadium are you interested in?")

            userIn = input()
            if userIn.lower() == "-l":
                displayList(SUBJECT_STADIUM)
                userIn = input()

            if not qb.setStadium(userIn): continue

        if inQuestion == 5:
            print("Which country are you interested in?")

            userIn = input()
            if userIn.lower() == "-l":
                displayList(SUBJECT_STADIUM)
                userIn = input()

            if not qb.setCountry(userIn): continue

        break
   
    return qb, inQuestion

def executeQuery(qb, inQuestion):

    # Why doesn't this version of python have switch statements :(
    if inQuestion == 1:
        results = rank_player_in_matches(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 2:
        results = rank_team_in_goal_concession(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 3:
        results = calculate_win_loss_ratio(qb.getSubject(), qb.getStadium(), qb.getCompetition())
    elif inQuestion == 4:
        results = count_referees_for_player(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 5:
        results = teams_with_managers_from_country_wrapper(qb.getCompetition(), qb.getSeason(), qb.getCountry())
    elif inQuestion == 6:
        results = managers_for_player(qb.getSubject())
    elif inQuestion == 7:
        results = event_count_for_player(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 8:
        results = own_goals_for_player(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 9:
        results = card_count_for_player(qb.getCompetition(), qb.getSeason(), qb.getSubject())
    elif inQuestion == 10:
        results = own_goals_against_for_player(qb.getCompetition(), qb.getSeason())

    return results
        

# qb = userInput()
while True:
    qb, inQuestion = userInputSetQueries()
    if inQuestion == -1:
        break
    print(executeQuery(qb, inQuestion))
    print("\nWould you like to enter another query? (y/n)")
    if str(input()).lower() != 'y':
        break