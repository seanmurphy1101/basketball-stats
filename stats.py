class Player():
    def __init__(self, name, number, team):
        self.name = name
        self.number = number
        self.team = team
        self.shots = {"made": 0, "missed": 0, "twos": 0, "threes": 0, "contested": 0, "uncontested": 0}
        self.assists = 0
        self.rebounds = {"offensive": 0, "defensive": 0}
        self.turnovers = 0
        self.freethrows = {"made": 0, "missed": 0}
        
class Team():
    def __init__(self, name):
        self.name = name
        self.shots = {"made": 0, "missed": 0, "twos": 0, "threes": 0, "contested": 0, "uncontested": 0}
        self.assists = 0
        self.rebounds = {"offensive": 0, "defensive": 0}
        self.turnovers = 0
        self.freethrows = {"made": 0, "missed": 0}
    
        

class Shot():
    def __init__(self, player1, made, contested, player2):
            self.player1 = player1
            self.made = made
            self.contested = contested
            self.player2 = player2


