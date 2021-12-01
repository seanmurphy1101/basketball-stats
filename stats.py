class Player():
    def __init__(self, name, number, team):
        self.name = name
        self.number = number
        self.team = team
        self.shots = {"made": 0, "missed": {"twos": 0, "threes": 0}, "twos": 0, "threes": 0, "contested": 0, "uncontested": 0}
        self.assists = 0
        self.rebounds = {"offensive": 0, "defensive": 0}
        self.turnovers = 0
        self.freethrows = {"made": 0, "missed": 0}
        self.fouls = 0
        self.steals = 0
        self.blocks = 0
        
class Team():
    def __init__(self, name):
        self.name = name
        self.shots = {"made": 0, "missed": {"twos": 0, "threes": 0}, "twos": 0, "threes": 0, "contested": 0, "uncontested": 0}
        self.assists = 0
        self.rebounds = {"offensive": 0, "defensive": 0}
        self.turnovers = 0
        self.freethrows = {"made": 0, "missed": 0}
        self.fouls = 0
        self.steals = 0
        self.blocks = 0
        

class Shot():
    def __init__(self, type, player, team, missed, contested, x ,y):
        self.player = player
        self.team = team
        self.missed = missed
        self.contested = contested
        self.type = type
        self.x = x
        self.y = y
    
    def asDict(self):
        return {"player": self.player, "team": self.team, "missed": self.missed, "contested": self.contested, "type": self.type, "x": self.x, "y": self.y}
        


