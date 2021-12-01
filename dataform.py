from tkinter import *
from tkinter import Frame, Label, ttk, font
from tkinter.constants import CENTER
from ttkthemes import THEMES, ThemedTk
from statsWindow import newWindow
from Game import createGame


dateStr = ""
infoStr = ""
homeTeam = []
awayTeam = []
numbersHome = []
numbersAway = []
playersHome=[]
playersAway=[]
game = []

# createEntry(frame: Frame{}, placeholder: String, w: int): Entry{}
def createEntry(frame, placeholder, w, p, t):
    
    text = StringVar()
    text.set(placeholder)
    entry = ttk.Entry(frame, justify=CENTER, width=w)
    entry.insert(0, placeholder)
    entry.configure(font=_font_)
    
    def on_click(event):
        entry.configure(state=NORMAL)
        entry.delete(0, END)
        # make the callback only work once
        entry.unbind('<Button-1>', on_click_id)

    on_click_id = entry.bind('<Button-1>', on_click)
    
    if (placeholder == "Date" or placeholder == "Additional Notes" or placeholder== "-home-" or placeholder == "-away-"):
        return entry 
    if p:
        if t:
            playersHome.append(entry)
        else:
            playersAway.append(entry)
    else:
        if t:
            numbersHome.append(entry)
        else:
            numbersAway.append(entry)

    return entry

# createNotebook(name: String, tab: Frame{}, label: String): Void
def createNotebook(name, tab, label, h):
    label = ttk.Label(tab, text=label)
    label.configure(font=_font_)
    label.pack(pady=10)
    
    title = createEntry(tab, name, 71, False, False)
    title.pack(padx=10, pady=10)
    if h:
        homeTeam.append(title)
    else: 
        awayTeam.append(title)

    frame = ttk.Frame(tab)
    frame.pack(pady=40)
    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    for i in range(15):
        frame.grid_rowconfigure(i, weight=1)
        if h:
            createEntry(frame, str(i+1), 60, True, True).grid(row=i, column=0,padx=0, pady=1)
            createEntry(frame, "--", 10, False, True).grid(row=i, column=1, padx=0, pady=1)
        else:
            createEntry(frame, str(i+1), 60, True, False).grid(row=i, column=0,padx=0, pady=1)
            createEntry(frame, "--", 10, False, False).grid(row=i, column=1, padx=0, pady=1)

# startGame(): Void
def startGame():
    playersH = []
    playersA = []
    numbersH = []
    numbersA = []
    dateStr = info.get()
    infoStr = notes.get()
    for i in range(len(playersHome)):
        if not ord(numbersHome[i].get()[0])==45:
            playersH.append(playersHome[i].get())
            numbersH.append(numbersHome[i].get())
            #for testing purposes players are not required
        #playersH.append(playersHome[i].get())
        #numbersH.append(numbersHome[i].get())
    for i in range(len(playersAway)):
        if not ord(numbersAway[i].get()[0])==45:
            playersA.append(playersAway[i].get())
            numbersA.append(numbersAway[i].get())
            #for testing purposes players are not required
        #playersA.append(playersAway[i].get())
        #numbersA.append(numbersAway[i].get())
    if len(numbersH)<5 or len(numbersA)<5:
        message.configure(text="5 Players Numbers Requiered for Each Team")
        return
    game.append(createGame(playersH, numbersH, homeTeam[0].get(), playersA, numbersA, awayTeam[0].get()))
    root.destroy()
    

#create window, set theme, and initialize font
root = ThemedTk()
root.geometry("1280x650")
root.set_theme("aquativo")
favorite = "keramik"
favorite2 = "breeze"
favorite3 = "winxpblue"
favorite4 = "radiance"
PTSans = font.Font(family="PT Sans", size=17)
PTSansBold = font.Font(family="PT Sans", size=17, weight="bold")
Mishafi = font.Font(family="Mishafi", size=17)
Thonburi = font.Font(family="Thonburi", size=17) #favorite
Adapta = font.Font(family="Adapta", size=17)
Verdana = font.Font(family="Verdana", size=17)
Optima = font.Font(family="Optima", size=20)
Kokonor = font.Font(family="Kokonor", size=17)
Noteworthy = font.Font(family="Noteworthy", size=17)
Lucida_Grande = font.Font(family="Lucida Grande", size=20)
Lao_MN = font.Font(family="Lao MN", size=20)
Menlo = font.Font(family="Menlo", size=20, weight="bold")
MenloSmall = font.Font(family="Menlo", size=15)
Kannada_Sangam_MN = font.Font(family="Kannada Sangam MN", size=20)
Marker_Felt = font.Font(family="Marker Felt", size=20)
Geeza_Pro = font.Font(family="Geeza Pro", size=20)
Arial_Hebrew_Scholar = font.Font(family="Ariel_Hebrew_Scholar", size=20)
Avenir_Next_Condensed = font.Font(family="Avenir Next Condensed", size=20)
Charter = font.Font(family="Charter", size=20)
AppleGothic = font.Font(family="AppleGothic", size=20)
Plantagenet_Cherokee = font.Font(family="Plantagenet Cherokee", size=20)
#print(font.families())
_font_ = Menlo
s=ttk.Style()
s.configure('.',font=_font_)
s.configure('Black.TLabelframe', tabposition='n')


#create title (although this is currently removed)
title = ttk.Label(root, text="Enter team names, player names, and player numbers in the appropriate setions",)
#title.pack(pady=10)
title.configure(font=_font_)

#create notebook for forms and info
main = ttk.Notebook(root, style='Black.TLabelframe',padding=3)
main.pack()

#create each tab
tab0 = ttk.Frame(main)
tab0.configure(border=100)
tab1 = ttk.Frame(main)
tab2 = ttk.Frame(main)
tab3 = ttk.Frame(main)
main.add(tab0, text="Welcome")
main.add(tab1, text="Home")
main.add(tab2, text="Away")
main.add(tab3, text="Info and Start")


#add a label to the info tab for the date
date = ttk.Label(tab3, text="Date")
date.configure(font=_font_)
date.pack()

#create an entry for date
info = createEntry(tab3, "Date", 71, False, False)
info.configure(font=_font_)
info.pack(pady=10)

#create entry for additional information
notes = createEntry(tab3, "Additional Notes", 71, False, False)
notes.configure(font=_font_)
notes.pack(pady=20)
start = ttk.Button(tab3, text="START", command=startGame)
start.configure()
start.pack(pady=20)
message = ttk.Label(tab3, text="")
message.pack()

#create title page layout
welcome = ttk.Label(tab0, text="Welcome to the Basketball Statskeeper\n"+"\nEnter team names, player names, and player numbers in the appropriate sections"+"\n \nThen, add optional date/info and click Start", justify=CENTER)
git = ttk.Label(tab0, text="\n \n \n \n \n \n \n \n \nFor more info and other projects\n \nvisit my GitHub at https://github.com/seanmurphy1101", justify=CENTER)
git.configure(font=MenloSmall)
welcome.pack(pady=30)
git.pack()


#create tabs 1 and 2 for player/team info
createNotebook("-home-", tab1, "Home Team", True)
createNotebook("-away-", tab2, "Away Team", False)


#run the window
root.mainloop()

exampleHomePlayers = ['Russell Westbrook', 'Anthony Davis', 'Lebron James', 'Dwight Howard', 'Carmelo Anthony', 'Jared Dudley', 'Wesley Matthews', 'Malik Monk', 'Marc Gasol', 'Wayne Ellington', 'Trevor Ariza', 'Kent Bazemore', 'Kendrick Nunn', 'Kostas Antetokounpo', 'Devontae Cacok']
exampleHomeNumbers = ['4', '3', '6', '39', '00', '10', '9', '1', '14', '8', '11', '26', '25', '37', '12']

exampleAwayPlayers = ['Jayson Tatum', 'Marcus Smart', 'Jaylen Brown', 'Enes Kanter', 'Jabari Parker', 'Kris Dunn', 'Tacko Fall', 'Luke Kornet', 'Romeo Langford', 'Payton Pritchard', 'Josh Richardson', 'Dennis Schroder', 'Grant Williams', 'Carson Edwards', 'Robert Williams III']
exampleAwayNumbers = ['0', '36', '7', '11', '20', '32', '99', '40', '45', '11', '0', '17', '12', '4', '44']
exampleGame = createGame(exampleHomePlayers, exampleHomeNumbers, 'LA Lakers', exampleAwayPlayers, exampleAwayNumbers, 'Boston Celtics')


# comment out unless example
# game[0] = exampleGame

newWindow(game[0])
