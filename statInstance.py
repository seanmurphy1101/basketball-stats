class Stat():
    def __init__(self, player, team, type):
        self.player = player
        self.team = team
        self.type = type
        self.missed = False
        self.contested = False
        self.reboundType = "defensive"
    
    def setMissed(self):
        self.missed = True
        return self

    def setContested(self):
        self.contested = True
        return self

    def setRebound(self, rebType):
        self.reboundType = rebType
        return self
