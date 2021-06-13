from tkinter import *
from tkinter import Frame, Label, ttk, font
from tkinter.constants import CENTER
from ttkthemes import THEMES, ThemedTk
from sub import Sub

activeHome = [0,1,2,3,4]
buttons = []

def newWindow(game, font_):

    def createSub(game):
        screen = Toplevel()
        arr = []

        if len(buttons) == 15:
            for i in buttons:
                i.pack_forget()
                i.pack()
        else:
            button0 = ttk.Button(screen, text=game.playersHome[0].name+" - "+game.playersHome[0].number, width=(20 if activeHome.__contains__(0) else 10), command=lambda: toggleSub(0))
            buttons.append(button0)
            button0.pack()

            button1 = ttk.Button(screen, text=game.playersHome[1].name+" - "+game.playersHome[1].number, width=(20 if activeHome.__contains__(1) else 10), command=lambda: toggleSub(1))
            buttons.append(button1)
            button1.pack()

            button2 = ttk.Button(screen, text=game.playersHome[2].name+" - "+game.playersHome[2].number, width=(20 if activeHome.__contains__(2) else 10), command=lambda: toggleSub(2))
            buttons.append(button2)
            button2.pack()

            button3 = ttk.Button(screen, text=game.playersHome[3].name+" - "+game.playersHome[3].number, width=(20 if activeHome.__contains__(3) else 10), command=lambda: toggleSub(3))
            buttons.append(button3)
            button3.pack()

            button4 = ttk.Button(screen, text=game.playersHome[4].name+" - "+game.playersHome[4].number, width=(20 if activeHome.__contains__(4) else 10), command=lambda: toggleSub(4))
            buttons.append(button4)
            button4.pack()

            button5 = ttk.Button(screen, text=game.playersHome[5].name+" - "+game.playersHome[5].number, width=(20 if activeHome.__contains__(5) else 10), command=lambda: toggleSub(5))
            buttons.append(button5)
            button0.configure(width=(20 if activeHome.__contains__(0) else 10))
            button5.pack()

            button6 = ttk.Button(screen, text=game.playersHome[6].name+" - "+game.playersHome[6].number, width=(20 if activeHome.__contains__(6) else 10), command=lambda: toggleSub(6))
            buttons.append(button6)
            button6.pack()

            button7 = ttk.Button(screen, text=game.playersHome[7].name+" - "+game.playersHome[6].number, width=(20 if activeHome.__contains__(7) else 10), command=lambda: toggleSub(7))
            buttons.append(button7)
            button7.pack()

            button8 = ttk.Button(screen, text=game.playersHome[8].name+" - "+game.playersHome[8].number, width=(20 if activeHome.__contains__(8) else 10), command=lambda: toggleSub(8))
            buttons.append(button8)
            button0.configure(width=(20 if activeHome.__contains__(0) else 10))
            button8.pack()

            button9 = ttk.Button(screen, text=game.playersHome[9].name+" - "+game.playersHome[9].number, width=(20 if activeHome.__contains__(9) else 10), command=lambda: toggleSub(9))
            buttons.append(button9)
            button9.pack()

            button10 = ttk.Button(screen, text=game.playersHome[10].name+" - "+game.playersHome[10].number, width=(20 if activeHome.__contains__(10) else 10), command=lambda: toggleSub(10))
            buttons.append(button10)
            button10.pack()

            button11 = ttk.Button(screen, text=game.playersHome[11].name+" - "+game.playersHome[11].number, width=(20 if activeHome.__contains__(11) else 10), command=lambda: toggleSub(11))
            buttons.append(button11)
            button11.pack()

            button12 = ttk.Button(screen, text=game.playersHome[12].name+" - "+game.playersHome[12].number, width=(20 if activeHome.__contains__(12) else 10), command=lambda: toggleSub(12))
            buttons.append(button12)
            button12.pack()

            button13 = ttk.Button(screen, text=game.playersHome[13].name+" - "+game.playersHome[13].number, width=(20 if activeHome.__contains__(13) else 10), command=lambda: toggleSub(13))
            buttons.append(button13)
            button13.pack()

            button14 = ttk.Button(screen, text=game.playersHome[14].name+" - "+game.playersHome[14].number, width=(20 if activeHome.__contains__(14) else 10), command=lambda: toggleSub(14))
            buttons.append(button14)
            button14.pack()

        def apply():
            for i in range(len(activeHome)):
                if i==0:
                    homeButton1.configure(text=game.playersHome[activeHome[i]].name+" - "+game.playersHome[activeHome[i]].number)
                elif i==1:
                    homeButton2.configure(text=game.playersHome[activeHome[i]].name+" - "+game.playersHome[activeHome[i]].number)
                elif i==2:
                    homeButton3.configure(text=game.playersHome[activeHome[i]].name+" - "+game.playersHome[activeHome[i]].number)
                elif i==3:
                    homeButton4.configure(text=game.playersHome[activeHome[i]].name+" - "+game.playersHome[activeHome[i]].number)
                else:
                    homeButton5.configure(text=game.playersHome[activeHome[i]].name+" - "+game.playersHome[activeHome[i]].number)
                screen.destroy()

        app = ttk.Button(screen, text="APPLY", command=apply)
        app.pack()




    master = ThemedTk()
    master.geometry('700x700')
    master.set_theme("smog")
    s=ttk.Style()
    s.configure('.',font=font_)

    buttonFrame = ttk.Frame(master)
    buttonFrame.pack()

    homeLabel = ttk.Label(buttonFrame, text=game.homeTeam.name)
    homeLabel.grid(row=0, column=0)

    awayLabel = ttk.Label(buttonFrame, text=game.awayTeam.name)
    awayLabel.configure(font=font_)
    awayLabel.grid(row=0, column=2)

    home = ttk.Frame(buttonFrame)
    home.grid(row=1, column=0)

    vs = ttk.Label(buttonFrame, text="   VS   ")
    vs.grid(row=1, column=1)

    away = ttk.Frame(buttonFrame)
    away.grid(row=1, column=2)

    homeSub = ttk.Button(home, text="SUB", command= lambda: createSub(game))
    homeSub.grid(row=0, column=0)

    homeButton1 = ttk.Button(home, text=game.playersHome[0].name+" - "+game.playersHome[0].number)
    homeButton1.grid(row=0, column=1)

    homeButton2 = ttk.Button(home, text=game.playersHome[1].name+" - "+game.playersHome[1].number)
    homeButton2.grid(row=0, column=2)

    homeButton3 = ttk.Button(home, text=game.playersHome[2].name+" - "+game.playersHome[2].number)
    homeButton3.grid(row=0, column=3)

    homeButton4 = ttk.Button(home, text=game.playersHome[3].name+" - "+game.playersHome[3].number)
    homeButton4.grid(row=0, column=4)

    homeButton5 = ttk.Button(home, text=game.playersHome[4].name+" - "+game.playersHome[4].number)
    homeButton5.grid(row=0, column=5)

    awaySub = ttk.Button(away, text="SUB")
    awaySub.grid(row=0, column=0)

    awayButton1 = ttk.Button(away, text=game.playersAway[0].name+" - "+game.playersAway[0].number)
    awayButton1.grid(row=0, column=1)

    awayButton2 = ttk.Button(away, text=game.playersAway[1].name+" - "+game.playersAway[1].number)
    awayButton2.grid(row=0, column=2)

    awayButton3 = ttk.Button(away, text=game.playersAway[2].name+" - "+game.playersAway[2].number)
    awayButton3.grid(row=0, column=3)

    awayButton4 = ttk.Button(away, text=game.playersAway[3].name+" - "+game.playersAway[3].number)
    awayButton4.grid(row=0, column=4)

    awayButton5 = ttk.Button(away, text=game.playersAway[4].name+" - "+game.playersAway[4].number)
    awayButton5.grid(row=0, column=5)


    master.mainloop()

        

def toggleSub(index):
    for e in activeHome:
        if (index == e):
            buttons[index].configure(width=10)
            activeHome.remove(e)
            return                
    if (len(activeHome)<5):
        buttons[index].configure(width=20)
        activeHome.append(index)
        activeHome.sort()
    return






    

            
    