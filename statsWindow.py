from os import remove
from stats import Player, Shot, Team
from tkinter import *
from tkinter import Frame, Label, ttk, font
from tkinter.constants import CENTER
from ttkthemes import THEMES, ThemedTk
from sub import SubWindow, Miss, Contested
from functools import partial
from court import drawCourt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle, Arc
from statInstance import Stat
import pandas as pd
import os
from datetime import date

# newWindow(game: Game{}): Void
def newWindow(game):
    master = ThemedTk()
    master.title("statskeeper")
    master.set_theme("aquativo")
    master.geometry('1600x1600')
    Menlo = font.Font(family="Menlo", size=14, weight="bold")
    master.option_add("*Font", Menlo)
    mainFrame = ttk.Frame(master)
    mainFrame.pack()

    activeHome = [0,1,2,3,4]
    activeAway = [0,1,2,3,4]
    buttonsHome = []
    buttonsAway = []
    global curPlayer
    curPlayer = None
    global curTeam
    curTeam = None
    screenButtonsHome = []
    screenButtonsAway = []
    missed = Miss()
    contested = Contested()
    global x
    x = None
    global y
    y = None
    canvasVersions = []
    global first
    first = True
    global circle
    circle = None
    global innerCircle
    innerCircle = None
    shots = []
    previousStats = []
    global statsArr
    statsArr = []
    screenFramesHome = []
    screenFramesAway = []

    # displaySubs(): Void
    def displaySubs():
        if not screen.hidden:
            screen.hidden = True
            screen.window.grid_forget()
        else:
            screen.window.grid(column=0, row=2)
            screen.hidden = False
    
    # displaySubsAway(): Void
    def displaySubsAway():
        if not screenAway.hidden:
            screenAway.hidden = True
            screenAway.window.grid_forget()
        else:
            screenAway.window.grid(column=2, row=2)
            screenAway.hidden = False
    
    # setCurrent(player: Player{}, button: Button{}, home: boolean): Void
    def setCurrent(player, frame, home):
        global curPlayer
        global curTeam
        for i in range(5):
            screenFramesHome[i]['relief'] = 'flat'
            screenFramesAway[i]['relief'] = 'flat'
        if player == curPlayer:
            curPlayer = None
            curTeam = None
            return
        else:
            curTeam = game.homeTeam if home else game.awayTeam
            frame['relief'] = 'raised'
            curPlayer = player
    
    # setPrev(type: String, player: String, team: String, isContested: boolean, isMissed: boolean): Void
    def setPrev(type, player, team, isContested, isMissed):
        global statsArr
        
        previousStats.append({"type": type, "player": player, "contested": isContested, "missed": isMissed })
        if type == "twos" or type == "threes":
            bottomLabel.configure(text="PlAYER: "+player+"     TEAM: "+team+"      SHOT TYPE: "+type[0: len(type)-1].upper()+("       MISSED" if isMissed else "      MADE")+" "+("     CONTESTED" if isContested else "     NOT CONTESTED"))
        elif type=="free throw":
            bottomLabel.configure(text="PlAYER: "+player+"     TEAM: "+team+"      TYPE: FREE THROW"+("       MISSED" if isMissed else "      MADE"))
        elif type=="offensive" or type=="defensive":
            bottomLabel.configure(text="PLAYER: "+player+"     TEAM: "+team+"      CATEGORY: "+type.upper()+" REBOUND")
        elif type=="steals":
            bottomLabel.configure(text="PLAYER: "+player+"     TEAM: "+team+"      CATEGORY: STEAL")
        elif type=="blocks":
            bottomLabel.configure(text="PLAYER: "+player+"     TEAM: "+team+"      CATEGORY: BLOCK")
        elif type=="fouls":
            bottomLabel.configure(text="PLAYER: "+player+"     TEAM: "+team+"      CATEGORY: FOUL")
        else:
            bottomLabel.configure(text="PLAYER: "+player+"     TEAM: "+team+"      CATEGORY: "+type.upper())

    # toggleSub(index: int, home: boolean): Void
    def toggleSub(index, home):
        active = activeHome if home else activeAway
        buttons = buttonsHome if home else buttonsAway
        for e in active:
            if (index == e):
                buttons[index].configure(width=10)
                active.remove(e)
                return                
        if (len(active)<5):
            buttons[index].configure(width=20)
            active.append(index)
            active.sort()
        return
    
    # reset(): Void
    def reset():
        global curPlayer
        global curTeam
        global circle
        global innerCircle
        global x
        global y
        #print(curPlayer.name, curPlayer.shots, curPlayer.turnovers, curPlayer.rebounds, curPlayer.assists, curPlayer.freethrows)
        curPlayer = None
        curTeam = None
        missed.missed = False
        contested.contested = False
        missed.isRed = False
        contested.isRed = False
        isMissFrame['relief'] = 'flat'
        contestedFrame['relief'] = 'flat'
        x = None
        y = None
        if not first and circle!=None and innerCircle!=None:
            try:
                circle.remove()
                innerCircle.remove()
                canvas.draw()
            except:
                print("circles are None")
        for i in range(5):
            screenFramesHome[i]['relief'] = 'flat'
            screenFramesAway[i]['relief'] = 'flat'

    # addShot(type: String): Void
    def addShot(type):
        global x
        global y
        #print(x, y)
        if not x == None and not y == None and (x<0) and curTeam.name == game.homeTeam.name:
            x = -x
            y = -y
        elif not x == None and not y == None and (x>=0) and curTeam.name == game.awayTeam.name:
            x = -x
            y = -y
        shot = Shot(type, curPlayer.name,missed.missed, contested.contested, x, y).asDict()
        #print(shot.player.name, shot.type, shot.missed.missed, shot.contested.contested, shot.x, shot.y)
        shots.append(shot)

    #assist(): Void
    def assist():
        global curPlayer
        global curTeam
        updateStats(Stat(curPlayer, curTeam, "assists"))
        if curPlayer != None and curTeam != None:
            curPlayer.assists += 1
            curTeam.assists +=1
            #print(curPlayer.assists, curTeam.assists)
            setPrev("assist", curPlayer.number, curTeam.name, False, False)
            reset()
    
    # foul(): Void
    def foul():
        curPlayer.fouls += 1
        curTeam.fouls +=1
        setPrev("foul", curPlayer.number, curTeam.name, False, False)
        updateStats(Stat(curPlayer, curTeam, "fouls"))
        reset()

    def block():
        global curPlayer
        global curTeam
        updateStats(Stat(curPlayer, curTeam, "blocks"))
    
    def steal():
        curPlayer.steals += 1
        curTeam.steals += 1
        setPrev("steal", curPlayer.number, curTeam.name, False, False)
        updateStats(Stat(curPlayer, curTeam, "steals"))
        reset()
    
    # onclick(ax: Axes{}, event: Event): Void
    def onclick(ax, event):
        global first
        global circle
        global innerCircle
        global x
        global y
        if event.xdata==None or event.xdata==None or event.ydata==None or event.ydata==None or event.xdata>47 or event.xdata<-47 or event.ydata>25 or event.ydata<-25:
            print("invalid spot")
            return 
        if not first and circle!=None and innerCircle!=None:
            try:
                circle.remove()
                innerCircle.remove()
            except:
                print("circles are None")
        else: 
            first = False
        x = round(event.xdata, 2)
        y = round(event.ydata, 2)
        circle = Circle((x, y), 0.75, color='darkblue')
        innerCircle = Circle((x, y), 0.50, color='white')
        ax.add_patch(circle)
        ax.add_patch(innerCircle)
        canvas.draw()

    # rebound(pos: String): Void
    def rebound(pos):
        if curPlayer != None and curTeam != None:
            updateStats(Stat(curPlayer, curTeam, "rebound").setRebound(pos))
            setPrev(pos, curPlayer.number, curTeam.name, False, False)
            curPlayer.rebounds[pos] += 1
            curTeam.rebounds[pos] =+ 1
            reset()
    
    # addShot2or3(points: String): Void
    def addShot2or3(points):
        if curPlayer != None and curTeam != None:
            addShot(points)
            setPrev(points, curPlayer.number, curTeam.name, contested.contested, missed.missed)
            instance = Stat(curPlayer, curTeam, points)
            curPlayer.shots[points] += 1
            curTeam.shots[points] += 1
            if missed:
                curPlayer.shots["missed"][points] +=1
                curTeam.shots["missed"][points] +=1
                instance.setMissed()
            else:
                curPlayer.shots["made"] += 1
                curTeam.shots["made"] += 1
            if contested.contested:
                curPlayer.shots["contested"] += 1
                curTeam.shots["contested"] += 1
                instance.setContested()
            else:
                curPlayer.shots["uncontested"] += 1
                curTeam.shots["uncontested"] += 1
            
            updateStats(instance)
            reset()

    def showBoxScore():
        box = Toplevel()
        box.title("Box Score")
        boxFrame = ttk.Frame(box)
        boxFrame.pack()
        createBoxScore(boxFrame, True)
        createBoxScore(boxFrame, False)
        
    def saveAsCSV():
        today = date.today()
        today = today.strftime("%b-%d-%Y")
        dfShots = pd.DataFrame(shots)
        home_team_underscore = game.homeTeam.name.replace(" ", "_")
        away_team_underscore = game.awayTeam.name.replace(" ", "_")

        homeTeamData = []
        for i in game.playersHome:
            homeTeamData.append(i.__dict__)
        
        homeTeamData.append(game.homeTeam.__dict__)

        awayTeamData = []
        for i in game.playersAway:
            awayTeamData.append(i.__dict__)
        
        awayTeamData.append(game.awayTeam.__dict__)

        if os.path.exists('output/csv_files') == False:
            os.mkdir('output/csv_files')
        
        dfShots.to_csv(f'output/csv_files/{home_team_underscore}_vs_{away_team_underscore}{today}_shots.csv')

        dfHomeTeam = pd.DataFrame(homeTeamData)
        dfAwayTeam = pd.DataFrame(homeTeamData)

        dfHomeTeam.to_csv(f'output/csv_files/{home_team_underscore}_stats.csv')
        dfAwayTeam.to_csv(f'output/csv_files/{away_team_underscore}_stats.csv')




    def createBoxScore(box, team):
        if team:
            p = game.playersHome
            t = game.homeTeam
            columns = 0
        else:
            p = game.playersAway
            t= game.awayTeam
            space = ttk.Label(box, text="          ")
            space.grid(row=0, column=8)
            columns = 9


        playerLabelTitle = ttk.Label(box, text=t.name)
        playerLabelTitle.grid(column=columns+0, row=0, padx=5)

        pointsLabelTitle = ttk.Label(box, text="POINTS")
        pointsLabelTitle.grid(row=0, column=columns+1, padx=5)

        assistsLabelTitle = ttk.Label(box, text="ASSISTS")
        assistsLabelTitle.grid(row=0, column=columns+2, padx=5)

        reboundsLabelTitle = ttk.Label(box, text="REBOUNDS")
        reboundsLabelTitle.grid(row=0, column=columns+3, padx=5)

        turnoversLabelTitle = ttk.Label(box, text="TURNOVERS")
        turnoversLabelTitle.grid(row=0, column=columns+4, padx=5)

        foulsLabelTitle = ttk.Label(box, text="FOULS")
        foulsLabelTitle.grid(row=0, column=columns+5, padx=5)

        blocksLabelTitle = ttk.Label(box, text="BLOCKS")
        blocksLabelTitle.grid(row=0, column=columns+6, padx=5)

        stealsLabelTitle = ttk.Label(box, text="STEALS")
        stealsLabelTitle.grid(row=0, column=columns+7, padx=5)

        for i in range(len(p)):
            playerLabel = ttk.Label(box, text=p[i].number+"  "+p[i].name, justify=LEFT )
            playerLabel.grid(row=i+1, column=columns+0, padx=5)

            pointsLabel = ttk.Label(box, text=str((p[i].shots["twos"]*2)+(p[i].shots["threes"]*3)+p[i].freethrows["made"]))
            pointsLabel.grid(row=i+1, column=columns+1, padx=5)

            assistsLabel = ttk.Label(box, text=str(p[i].assists))
            assistsLabel.grid(row=i+1, column=columns+2, padx=5)

            reboundsLabel = ttk.Label(box, text=str(p[i].rebounds["offensive"]+p[i].rebounds["defensive"]))
            reboundsLabel.grid(row=i+1, column=columns+3, padx=5)

            turnoversLabel = ttk.Label(box, text=str(p[i].turnovers))
            turnoversLabel.grid(row=i+1, column=columns+4, padx=5)

            foulsLabel = ttk.Label(box, text=str(p[i].fouls))
            foulsLabel.grid(row=i+1, column=columns+5, padx=5)

            blocksLabel = ttk.Label(box, text=str(p[i].blocks))
            blocksLabel.grid(row=i+1, column=columns+6, padx=5)

            stealsLabel = ttk.Label(box, text=str(p[i].steals))
            stealsLabel.grid(row=i+1, column=columns+7, padx=5)

            

        totalLabel = ttk.Label(box, text="TOTAL")
        totalLabel.grid(column=columns+0, row=len(p)+1, padx=5)

        pointsLabelTeam = ttk.Label(box, text=str((t.shots["twos"]*2)+(t.shots["threes"]*3)+t.freethrows["made"]))
        pointsLabelTeam.grid(row=len(p)+1, column=columns+1, padx=5)

        assistsLabelTeam = ttk.Label(box, text=str(t.assists))
        assistsLabelTeam.grid(row=len(p)+1, column=columns+2, padx=5)

        reboundsLabelTeam = ttk.Label(box, text=str(t.rebounds["offensive"]+t.rebounds["defensive"]))
        reboundsLabelTeam.grid(row=len(p)+1, column=columns+3, padx=5)

        turnoversLabelTeam = ttk.Label(box, text=str(t.turnovers))
        turnoversLabelTeam.grid(row=len(p)+1, column=columns+4, padx=5)
        
        foulsLabelTeam = ttk.Label(box, text=str(t.fouls))
        foulsLabelTeam.grid(row=len(p)+1, column=columns+5, padx=5)

        blocksLabelTeam = ttk.Label(box, text=str(t.blocks))
        blocksLabelTeam.grid(row=len(p)+1, column=columns+6, padx=5)

        stealsLabelTeam = ttk.Label(box, text=str(t.steals))
        stealsLabelTeam.grid(row=len(p)+1, column=columns+7, padx=5)

        

    # isContested(): Void
    def isContested():
        toggleContested()
        contested.contested = True
    
    # turnover(): Void
    def turnover():
        if curPlayer != None and curTeam != None:
            updateStats(Stat(curPlayer, curTeam, "turnovers"))
            setPrev("turnovers", curPlayer.name, curTeam.name, False, False)
            curPlayer.turnovers += 1
            curTeam.turnovers +=1
            reset()

    # isMiss(): Void
    def isMiss():
        toggleMiss()
        missed.missed = True

    # toggleMiss(): Void
    def toggleMiss():
        if missed.isRed:
            missed.isRed = False
            isMissFrame['relief'] = 'flat'
        else:
            missed.isRed = True
            isMissFrame['relief'] = 'raised'
    
    # toggleContested(): Void
    def toggleContested():
        if contested.isRed:
            contested.isRed = False
            contestedFrame['relief'] = 'flat'
        else:
            contested.isRed = True
            contestedFrame['relief'] = 'raised'

    # freeThrow(): Void
    def freeThrow():
        addShot("free throw")
        if curPlayer != None and curTeam != None:
            instance = Stat(curPlayer, curTeam, "free throw")
            if missed.missed:
                curPlayer.freethrows["missed"] += 1
                curTeam.freethrows["missed"] += 1
                instance.setMissed()
            else:
                curPlayer.freethrows["made"] += 1
                curTeam.freethrows["made"] += 1
            updateStats(instance)
            setPrev("free throw", curPlayer.name, curTeam.name, False, missed.missed)
            reset()
    
    def updateStats(statInstance):
        global statsArr
        statsArr.append(statInstance)
    

    def removeLastStat():
        global statsArr
        if len(statsArr) == 0:
            return
        instance = statsArr[-1]
        if instance.type == "free throw":
            if instance.missed:
                instance.player.freethrows["missed"] -= 1
                instance.team.freethrows["missed"] -= 1
            else:
                instance.player.freethrows["made"] -= 1
                instance.team.freethrows["made"] -= 1
        elif instance.type == "rebound":
            instance.player.rebounds[instance.reboundType] -= 1
            instance.team.rebounds[instance.reboundType] -= 1
        elif instance.type == "turnovers":
            instance.player.turnovers -= 1
            instance.team.turnovers -= 1
        elif instance.type == "assists":
            instance.player.assists -= 1
            instance.team.assists -= 1
        elif instance.type == "twos" or instance.type == "threes":
            del shots[-1]
            instance.player.shots[instance.type] -= 1
            instance.team.shots[instance.type] -= 1
            if instance.missed:
                instance.player.shots["missed"][instance.type] -= 1
                instance.team.shots["missed"][instance.type] -= 1
            else:
                instance.player.shots["made"] -= 1
                instance.team.shots["made"] -= 1
            if instance.contested:
                instance.player.shots["contested"] -= 1
                instance.team.shots["contested"] -= 1
            else: 
                instance.player.shots["uncontested"] -= 1
                instance.team.shots["uncontested"] -= 1
        elif instance.type == "steals":
            instance.player.steals -= 1
            instance.team.steals -= 1
        elif instance.type == "fouls":
            instance.player.fouls -= 1
            instance.team.fouls -= 1
        elif instance.type == "blocks":
            instance.player.blocks -= 1
            instance.team.blocks -= 1
        del statsArr[-1]
        if len(statsArr) == 0:
            bottomLabel.configure(text="")
        elif statsArr[-1].type == "rebound":
            setPrev(statsArr[-1].reboundType, statsArr[-1].player.name, statsArr[-1].team.name, statsArr[-1].contested, statsArr[-1].missed)
        else:
            setPrev(statsArr[-1].type, statsArr[-1].player.name, statsArr[-1].team.name, statsArr[-1].contested, statsArr[-1].missed)
    
    # createSub(): Void
    def createSub():
        # apply(home: boolean): Void
        def apply(home):
            screenButtons = screenButtonsHome if home else screenButtonsAway
            screenFrames = screenFramesHome if home else screenFramesAway
            active = activeHome if home else activeAway
            players = game.playersHome if home else game.playersAway
            for i in range(len(active)):
                func = partial(setCurrent, players[active[i]], screenFrames[i], home)
                screenButtons[i].configure(text=players[active[i]].number, command=func)


        for i in range(len(game.playersHome)):
            func = partial(toggleSub, i, True)
            button = ttk.Button(screen.window, text=game.playersHome[i].number, width=(20 if activeHome.__contains__(i) else 10), command=func)
            buttonsHome.append(button)
            button.pack()
        
        for i in range (len(game.playersAway)):
            func = partial(toggleSub, i, False)
            button = ttk.Button(screenAway.window, text=game.playersAway[i].number, width=(20 if activeAway.__contains__(i) else 10), command=func)
            buttonsAway.append(button)
            button.pack()

        appHome = ttk.Button(screen.window, text='APPLY', command=lambda: apply(True))
        appHome.pack()

        appAway = ttk.Button(screenAway.window, text='APPLY', command=lambda: apply(False))
        appAway.pack()

    screen = SubWindow(mainFrame)
    screenAway = SubWindow(mainFrame)
    createSub()
    
    # create home and away sub labels
    homeSubLabel = ttk.Label(mainFrame, text="Home Subs", width=10, justify=RIGHT)
    homeSubLabel.grid(row=1, column=0, padx=77, sticky='w')

    awaySubLabel = ttk.Label(mainFrame, text="Away Subs", width=10, justify=LEFT)
    awaySubLabel.grid(row=1, column=2, padx=77)

    # create frame for all onscreen player buttons
    buttonFrame = ttk.Frame(mainFrame)
    buttonFrame.grid(column=1, row=0)

    # create home and away team labels
    homeLabel = ttk.Label(buttonFrame, text=game.homeTeam.name)
    homeLabel.grid(row=0, column=0)

    awayLabel = ttk.Label(buttonFrame, text=game.awayTeam.name)
    awayLabel.grid(row=0, column=2)

    # frame for home onscreen players
    home = ttk.Frame(buttonFrame)
    home.grid(row=1, column=0)

    vs = ttk.Label(buttonFrame, text="   VS   ")
    vs.grid(row=1, column=1)

    # frame for away onscreen players
    away = ttk.Frame(buttonFrame)
    away.grid(row=1, column=2)

    screenButtonsWidth = 7

    # create sub button and five onscreen player buttons
    homeSub = ttk.Button(home, text="SUB", command=displaySubs)
    homeSub.grid(row=0, column=0)

    homeFrame1 = ttk.Frame(home)
    homeFrame1['relief']='flat'
    homeFrame1.grid(row=0, column=1)
    screenFramesHome.append(homeFrame1)
    homeButton1 = ttk.Button(homeFrame1, text=game.playersHome[0].number, command=lambda: setCurrent(game.playersHome[0], homeFrame1, True), width=screenButtonsWidth ) 
    homeButton1.pack(pady=3, padx=3)
    screenButtonsHome.append(homeButton1)

    homeFrame2 = ttk.Frame(home)
    homeFrame2['relief']='flat'
    homeFrame2.grid(row=0, column=2)
    screenFramesHome.append(homeFrame2)
    homeButton2 = ttk.Button(homeFrame2, text=game.playersHome[1].number, command=lambda: setCurrent(game.playersHome[1], homeFrame2, True), width=screenButtonsWidth)
    homeButton2.pack(pady=3, padx=3)
    screenButtonsHome.append(homeButton2)

    homeFrame3 = ttk.Frame(home)
    homeFrame3['relief']='flat'
    homeFrame3.grid(row=0, column=3)
    screenFramesHome.append(homeFrame3)
    homeButton3 = ttk.Button(homeFrame3, text=game.playersHome[2].number, command=lambda: setCurrent(game.playersHome[2], homeFrame3, True), width=screenButtonsWidth)
    homeButton3.pack(pady=3, padx=3)
    screenButtonsHome.append(homeButton3)

    homeFrame4 = ttk.Frame(home)
    homeFrame4['relief']='flat'
    homeFrame4.grid(row=0, column=4)
    screenFramesHome.append(homeFrame4)
    homeButton4 = ttk.Button(homeFrame4, text=game.playersHome[3].number, command=lambda: setCurrent(game.playersHome[3], homeFrame4, True), width=screenButtonsWidth)
    homeButton4.pack(pady=3, padx=3)
    screenButtonsHome.append(homeButton4)

    homeFrame5 = ttk.Frame(home)
    homeFrame5['relief']='flat'
    homeFrame5.grid(row=0, column=5)
    screenFramesHome.append(homeFrame5)
    homeButton5 = ttk.Button(homeFrame5, text=game.playersHome[4].number, command=lambda: setCurrent(game.playersHome[4], homeFrame5, True), width=screenButtonsWidth)
    homeButton5.pack(pady=3, padx=3)
    screenButtonsHome.append(homeButton5)

    # create five onscreen player buttons and then sub button
    awaySub = ttk.Button(away, text="SUB", command=displaySubsAway)
    awaySub.grid(row=0, column=5)


    awayFrame1 = ttk.Frame(away)
    awayFrame1['relief']='flat'
    awayFrame1.grid(row=0, column=0)
    screenFramesAway.append(awayFrame1)
    awayButton1 = ttk.Button(awayFrame1, text=game.playersAway[0].number, command=lambda: setCurrent(game.playersAway[0], awayFrame1, False), width=screenButtonsWidth)
    awayButton1.pack(pady=3,padx=3)
    screenButtonsAway.append(awayButton1)

    awayFrame2 = ttk.Frame(away)
    awayFrame2['relief']='flat'
    awayFrame2.grid(row=0, column=1)
    screenFramesAway.append(awayFrame2)
    awayButton2 = ttk.Button(awayFrame2, text=game.playersAway[1].number, command=lambda: setCurrent(game.playersAway[1], awayFrame2, False), width=screenButtonsWidth)
    awayButton2.pack(pady=3,padx=3)
    screenButtonsAway.append(awayButton2)

    awayFrame3 = ttk.Frame(away)
    awayFrame3['relief']='flat'
    awayFrame3.grid(row=0, column=2)
    screenFramesAway.append(awayFrame3)
    awayButton3 = ttk.Button(awayFrame3, text=game.playersAway[2].number, command=lambda: setCurrent(game.playersAway[2], awayFrame3, False), width=screenButtonsWidth)
    awayButton3.pack(pady=3,padx=3)
    screenButtonsAway.append(awayButton3)

    awayFrame4 = ttk.Frame(away)
    awayFrame4['relief']='flat'
    awayFrame4.grid(row=0, column=3)
    screenFramesAway.append(awayFrame4)
    awayButton4 = ttk.Button(awayFrame4, text=game.playersAway[3].number, command=lambda: setCurrent(game.playersAway[3], awayFrame4, False), width=screenButtonsWidth)
    awayButton4.pack(pady=3,padx=3)
    screenButtonsAway.append(awayButton4)

    awayFrame5 = ttk.Frame(away)
    awayFrame5['relief']='flat'
    awayFrame5.grid(row=0, column=4)
    screenFramesAway.append(awayFrame5)
    awayButton5 = ttk.Button(awayFrame5, text=game.playersAway[4].number, command=lambda: setCurrent(game.playersAway[4], awayFrame5, False), width=screenButtonsWidth)
    awayButton5.pack(pady=3,padx=3)
    screenButtonsAway.append(awayButton5)


    for i in range(5):
        screenFramesHome[i]['borderwidth'] = '2'
        screenFramesAway[i]['borderwidth'] = '2'
        #screenButtonsHome[i].configure(anchor='center')
        #screenButtonsAway[i].configure(anchor='center')

    # all stats related buttons
    px = 3
    py = 3

    stats = ttk.Frame(mainFrame)
    stats.grid(row=1, column=1, padx=px, pady=5)

    assistsButton = ttk.Button(stats, text="ASSIST", command=assist)
    assistsButton.grid(row=0,column=0, padx=px, pady=5)

    offRebound = ttk.Button(stats, text="OFFENSIVE REBOUND", command = lambda: rebound("offensive"))
    offRebound.grid(row=0, column=1, padx=px, pady=5)

    defRebound = ttk.Button(stats, text="DEFENSIVE REBOUND", command = lambda: rebound("defensive"))
    defRebound.grid(row=0, column=2, padx=px, pady=5)

    isMissFrame = ttk.Frame(stats)
    isMissFrame.grid(row=0, column=11, padx=px, pady=5)
    isMissFrame['relief'] = 'flat'
    isMissFrame['borderwidth'] = '5'
    isMissButton = ttk.Button(isMissFrame, text="MISS", command = isMiss)
    isMissButton.pack()

    divider = ttk.Label(stats, text="|")
    divider.configure(font=font.Font(family="Menlo", size=24, weight="bold"))
    divider.grid(row=0, column=10, pady=0)

    addShot2 = ttk.Button(stats, text="2", command=lambda: addShot2or3("twos"))
    addShot2.grid(row=0, column=4, padx=px, pady=5)

    addShot3 = ttk.Button(stats, text="3", command=lambda: addShot2or3("threes"))
    addShot3.grid(row=0, column=5, padx=px, pady=5)

    turnoverButton = ttk.Button(stats, text="TURNOVER", command = turnover)
    turnoverButton.grid(row=0, column=6, padx=px, pady=5)

    freeThrowButton = ttk.Button(stats, text="FREE THROW", command = freeThrow)
    freeThrowButton.grid(row=0, column=3, padx=px, pady=5)

    foulButton = ttk.Button(stats, text="FOUL", command=foul)
    foulButton.grid(row=0, column=7, padx=px, pady=5)

    stealButton = ttk.Button(stats, text="STEAL", command=steal)
    stealButton.grid(row=0, column=8, padx=px, pady=5)

    blockButton = ttk.Button(stats, text="BLOCK", command=block)
    blockButton.grid(row=0, column=9, padx=px, pady=5)
    


    contestedFrame = ttk.Frame(stats)
    contestedFrame.grid(row=0, column=12, padx=7, pady=5)
    contestedFrame['relief'] = 'flat'
    contestedFrame['borderwidth'] = '5'
    contestedButton = ttk.Button(contestedFrame, text="CONTESTED", command = isContested)
    contestedButton.pack()


    # embed interactive court into mainFrame
    court = drawCourt()
    myFunc = partial(onclick, court[1])
    court[0].canvas.mpl_connect('button_press_event', myFunc)
    canvas = FigureCanvasTkAgg(court[0], mainFrame)
    canvasVersions.append(canvas)
    canvas.get_tk_widget().grid(row=2, column=1)


    bottomTitle = ttk.Label(mainFrame, text="LAST ADDED STAT: ")
    bottomTitle.grid(row=3, column=1, pady=6)
    bottomLabel = ttk.Label(mainFrame, text="")
    bottomLabel.grid(row=4, column=1, pady=20)

    style_1 = {'bg': 'RoyalBlue3', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}
    style_2 = {'fg': 'white', 'bg': 'OliveDrab2', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}

    removeLast = ttk.Button(mainFrame, text="REMOVE LAST", command=removeLastStat)
    removeLast.grid(row=4, column=2)



    dataFrame = ttk.Frame(mainFrame)
    dataFrame.grid(row=4, column=0)
    boxScore = ttk.Button(dataFrame, text="BOX SCORE", command=showBoxScore)
    boxScore.pack()
    saveCSV = ttk.Button(dataFrame, text="SAVE CSV", command=saveAsCSV)
    saveCSV.pack()



    # run loop
    master.mainloop()


    







    

            
    