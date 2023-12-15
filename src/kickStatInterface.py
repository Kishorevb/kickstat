import kuzu
import shutil

printInput = True

SUBJECT_NONE = 0
SUBJECT_TEAM = 1
SUBJECT_PLAYER = 2
SUBJECT_MANAGER = 3
SUBJECT_EVENT = 4
SUBJECT_COUNTRY = 5
SUBJECT_COMPETITION = 6

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

    def setCompetition(self, comp):
        self.competition = comp

    def setSeasons(self, start, end=0):
        self.startSeason = start
        self.endSeason = end

    def setSubject(self, subject, subjectType):
        if typeString(subjectType) == "UNEXPECTED TYPE":
            print("Subject type unexpected, cannot set")
            return
        self.subject = subject
        self.subjectType = subjectType

    def setColumns(self, columns=[]):
        if type(columns) == type([]):
            self.columns = columns

    def setHomeGames(self, val):
        self.homeGames = val

    def setAwayGames(self, val):
        self.awayGames = val

    def setStadium(self, val):
        self.stadium = val
    
    def setCountry(self, val):
        self.country = val

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
    else: return "UNEXPECTED TYPE"

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

    print("Which predetermined query are you interested in?")
    for i in range(len(questions)):
        print(""+str(i+1)+". "+questions[i])

    inQuestion = int(input())

    if inQuestion != 6:
        print("Which competition are you interested in?")
        qb.setCompetition(input())

        print("Start season?")
        start = int(input())

        print("End season? (or 0 for one season)")
        qb.setSeasons(start, int(input()))

    if inQuestion in [1, 4, 6, 7, 8]:
        print("Which player are you interested in?")
        qb.setSubject(input(), SUBJECT_PLAYER)

    else:
        print("Which team are you interested in?")
        qb.setSubject(input(), SUBJECT_TEAM)
    
    if inQuestion == 3:
        print("Which stadium are you interested in?")
        qb.setStadium(input())

    if inQuestion == 5:
        print("Which country are you interested in?")
        qb.setCountry(input())

   
    return qb


# qb = userInput()
qb = userInputSetQueries()
print(qb)
