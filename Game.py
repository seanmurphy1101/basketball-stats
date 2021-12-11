from stats  import Player
from stats import Team


def createPlayers(players, numbers, team):
    res = []
    for i in range(len(players)):
        res.append(Player(players[i], numbers[i], team))
    return res


def createGame(playersHome, numbersHome, homeTeam, playersAway, numbersAway, awayTeam):
    return (Game(Team(homeTeam), Team(awayTeam), createPlayers(playersHome, numbersHome, homeTeam), createPlayers(playersAway, numbersAway, awayTeam)))


class Game():
    def __init__(self, homeTeam, awayTeam, playersHome, playersAway):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.playersHome = playersHome
        self.playersAway = playersAway
        self.shots = []

