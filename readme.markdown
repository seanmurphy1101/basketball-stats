# BasketBall Statskeeper

## The goal of this project was to create an application which would allow users to record detailed game statistics in an easy and fast manner. Using an interactive court, users can record shot location as well as many other stats. Afterwards, the user can export the data as a Pandas Dataframe. The GUI was mainly built using the Tkinter library but also makes use of a few other libraries such as matplotlib for the court. A lot of effort was put towards making this application intuitive and efficient while recording more than just a few statistics.


<br />

# How to Use


## Once the software is downloaded and running with required dependencies, you will be prompted to enter basic team informatin including the team names and players. Note that by default there are 5 players required for each team in order to create the game instance. When this section is finished, click START and you will be ready to begin recording stats!

## To record a stat begin by selecting a player. If your desired stats doesn't require any extra information then you can click the corresponding button. You can verify the stat was recorded by looking at the last added stat section in the bottom middle or checking if the buttons are set back to their defualt values. If your stat is a shot then it you can click a location on the court where the shot took place. The toggle buttons labeled Contested and Made allow you to toggle these values before you click the final stat. Once all this is done, you can select 2pt or 3pt and the shot intance will be created. In the case that an incorrect stat is added, select remove last and the stat will be deleted. You can do this until you are reset. Removed stats are permanently deleted so be careful with this function. If you would like to make a substitution, select the sub button for the corresponding team so it reveals a column with all team players. If a player is in the game currently then their box will be larger than those on the bench. Click a player to toggle them in/out of the game. You cannot add a player unless there are less than 5 selected so you must remove them before you add. You can check the boxscore at anytime by selecting the box score button. Make sure to save the most recent state before exiting the application or else data will be lost.


# Anyone is welcome to use this project for non-commercial purposes, thanks for the support!
