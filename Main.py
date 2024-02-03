#! GUI Libraries
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

# ! Database Library
import mysql.connector as mc

# ! Shared class : that holds all the global variables
from SharedDomain import Shared

# ! Chess Game
import chessMain

# ! Time Library
from time import time as currenttime_stamp


# ! GUI Classes
class MainGUI(QDialog):
    """Main Game window GUI"""
    def __init__(self):
        super(MainGUI, self).__init__();
        loadUi("GUI/Main.ui", self)

        # Buttons
        self.btnPlay.clicked.connect(self.GameStarterCaller)
        self.btnScoreboard.clicked.connect(self.ScoreBoardWindowCaller)
        self.btnTheme.clicked.connect(self.ThemeWindowCaller)
        self.btnExit.clicked.connect(self.ExitWindowCaller)

        # set the default theme
        try:
            mycursor = Shared.conn.cursor()
            query = "SELECT theme_pieces_path, colorA_bg, colorB_bg FROM themes WHERE status = 1"
            mycursor.execute(query)
            Shared.Theme["path"], Shared.Theme["colorA"], Shared.Theme["colorB"] = mycursor.fetchone()
            # * Setting the theme in global Theme dictionary
            mycursor.close()
        except:
            print("connection failed, Starting game without Database")

    def GameStarterCaller(self):
        gamestarterwindow = GameStarterGUI() # intializing a widget
        widget.addWidget(gamestarterwindow) # adding it to the stack
        Shared.all_widgits.append(gamestarterwindow)# adding widget to list to hold it
        widget.setCurrentIndex(widget.currentIndex() + 1)# shanging the index to desplay the called widget

    def ThemeWindowCaller(self):
        themewindow = ThemeGUI()
        widget.addWidget(themewindow)
        Shared.all_widgits.append(themewindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ScoreBoardWindowCaller(self):
        scoreboardwindow = ScoreBoardGUI()
        widget.addWidget(scoreboardwindow)
        Shared.all_widgits.append(scoreboardwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ExitWindowCaller(self):
        exitwindow = ExitGUI()
        widget.addWidget(exitwindow)
        Shared.all_widgits.append(exitwindow)
        # Resizing the window
        widget.setFixedWidth(390)
        widget.setFixedHeight(200)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class GameStarterGUI(QDialog):
    """Game Starter Main window"""
    def __init__(self):
        super(GameStarterGUI, self).__init__();
        loadUi("GUI/GameStarter.ui", self)

        #Buttons
        self.btnBack.clicked.connect(self.MainWindowCaller)
        self.btnPlay.clicked.connect(self.IntiateGame)

    def MainWindowCaller(self):
        """Recalling the main window"""
        widget.setCurrentIndex(widget.currentIndex() - 1) # going back to the previous window
        widget.removeWidget(Shared.all_widgits[-1]) # removing widget from stack
        Shared.all_widgits.pop() # removing widget from reference holder

    def IntiateGame(self):
        """Intializing the game and starting it"""

        Shared.playerName = "unKnown GM" if self.txtPlayerName.text() == "" else self.txtPlayerName.text() # Setting player name
        Shared.playas = 1 if self.radioWhite.isChecked() == True else 2; # setting side to play as (white = 1 or black = 2)
        # ! if true set playas to 1 else 2

        # Setting level
        if self.comLevel.currentIndex() + 1 == 1:
            Shared.level = 1;
        elif self.comLevel.currentIndex() + 1 == 2:
            Shared.level = 2;
        else:
            Shared.level = 3;

        # ! intiate pygame here⬇ (chess)
        widget.hide() # hide window
        Shared.starttime = currenttime_stamp() # take start time
        chessMain.main() #* call the chess game
        Shared.timetaken = (currenttime_stamp() - Shared.starttime) // 60 # calculate match time

        # ! if player wins add them to scores - ( save to DB )
        if Shared.playerWon: # check for winner
            query = ("INSERT INTO scores(player_name, tiime_minutes, steps_taken, level) VALUES ('" +
                     Shared.playerName + "', " +
                     str(Shared.timetaken) + ", " +
                     str(Shared.movesmade) + ", " +
                     str(Shared.level) + ")")
            mycursor = Shared.conn.cursor()
            mycursor.execute(query)
            Shared.conn.commit()  # save changes in database (used with update and insert)
            mycursor.close()

        # reset global varibles
        Shared.timetaken = Shared.starttime = Shared.movesmade = 0
        Shared.playerWon = False
        widget.show() # show window


class ScoreBoardGUI(QDialog):
    """Scoreboard Window Class"""
    def __init__(self):
        super(ScoreBoardGUI, self).__init__();
        loadUi("GUI/ScoreBoard.ui", self)

        # initialize Style and FirstTime Data
        self.tableScoreBoard.setColumnWidth(0, 179) # Player Name Column
        self.tableScoreBoard.setColumnWidth(1, 60) # Moves Column
        self.tableScoreBoard.setColumnWidth(2, 75) # Time Column
        self.tableScoreBoard.setHorizontalHeaderLabels(["Name", "Moves", "Time"])
        # ! load data for  the frist time  and the  default  level is easy==1
        self.LoadData()

        self.comLevel.currentIndexChanged.connect(self.LoadData)  # if score level is changed load data  for the choisen level
        self.btnBack.clicked.connect(self.MainWindowCaller)

        # styling
        # ! coloring header
        self.sh = "::section{Background-color:rgb(170,0,0)}"
        self.tableScoreBoard.horizontalHeader().setStyleSheet(self.sh)
        self.tableScoreBoard.verticalHeader().setStyleSheet(self.sh)
        self.tableScoreBoard.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # ! Changing size and font
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Impact')
        self.tableScoreBoard.setFont(font)

        # ! changing content foreground color
        self.tableScoreBoard.setStyleSheet("color: black;")

    def MainWindowCaller(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(Shared.all_widgits[-1])
        Shared.all_widgits.pop()

    def LoadData(self):
        try:
            mycursor = Shared.conn.cursor()
            query = ("select player_name,steps_taken,tiime_minutes from scores where level="
                     + str(
                        self.comLevel.currentIndex() + 1) + " order by steps_taken desc ,tiime_minutes,game_timestamp   limit 10")
            # we use +1 because indexing in combo box start from 0
            mycursor.execute(query)
            returnedrows = mycursor.fetchall()  # get all data
            mycursor.close()  # ! NOTE: all connections should be closed after the query


            count = len(returnedrows) # ! NOTE: because the rows returned as a list of tuples we can get its length

            # set rowcount to 0 this is because when we choose another score level we need to remove the previuse data on table so set rows to zero
            self.tableScoreBoard.setRowCount(0)

            self.tableScoreBoard.setRowCount(10)
            """if count > 10:
                self.tableScoreBoard.setRowCount(10)
            else:
                self.tableScoreBoard.setRowCount(count)"""
                #  if returned rows less than 10 so only make rows on table as many as returned rows

            tablerow = 0  # just to start filling from row 0

            for row in returnedrows:
                # first 0 means column 0 in the table widget second 0 means first  column in table retrieved
                self.tableScoreBoard.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0])) #! row | column | value of type Item
                self.tableScoreBoard.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.tableScoreBoard.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                tablerow += 1
        except:
            print("Connection Failed: There is No Database and no high scores")

class ThemeGUI(QDialog):
    """Theme Window Class"""
    def __init__(self):
        super(ThemeGUI, self).__init__();
        loadUi("GUI/Settings.ui", self)
        # Default checked
        if "3" in Shared.Theme["path"]:
            self.radioTheme3.setChecked(True);
        elif "2" in Shared.Theme["path"]:
            self.radioTheme2.setChecked(True);
        else:
            self.radioTheme1.setChecked(True);
        # Buttons
        self.btnCancel.clicked.connect(self.MainWindowCaller)
        self.btnSave.clicked.connect(self.ThemeChanger)

    def MainWindowCaller(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(Shared.all_widgits[-1])
        Shared.all_widgits.pop()

    def ThemeChanger(self):
        """Theme Changer Functipn"""
        try:
            choosenTheme = None
            if self.radioTheme1.isChecked() == True:
                choosenTheme = "theme1"
            elif self.radioTheme2.isChecked() == True:
                choosenTheme = "theme2"
            else:
                choosenTheme = "theme3"

            mycursor = Shared.conn.cursor()
            query = "SELECT theme_pieces_path, colorA_bg, colorB_bg FROM themes WHERE theme_name = '" + choosenTheme + "'"
            mycursor.execute(query)
            Shared.Theme["path"], Shared.Theme["colorA"], Shared.Theme["colorB"] = mycursor.fetchone()
            mycursor.close()
            query = "UPDATE themes SET status =  CASE WHEN theme_name = '" + choosenTheme + "'Then 1 ELSE 0 END"
            mycursor = Shared.conn.cursor()
            mycursor.execute(query)
            Shared.conn.commit()  # savechanges in database
            mycursor.close()

            print(choosenTheme)
        except:
            print("You do not have a database so you can not change the theme")

        self.MainWindowCaller()

class ExitGUI(QDialog):
    """Exit Dialog Window"""
    def __init__(self):
        super(ExitGUI, self).__init__()
        loadUi("GUI/ExitDialog.ui", self)
        self.btnCancel.clicked.connect(self.MainWindowCaller)
        self.btnOK.clicked.connect(self.ExitApplication)
        widget.move(x, y+200) # moving Exit Dialog

    def MainWindowCaller(self):
        widget.setFixedWidth(400)
        widget.setFixedHeight(580)
        widget.move(x, y) # moving returning window position
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(Shared.all_widgits[-1])
        Shared.all_widgits.pop()

    def ExitApplication(self):
        """Shut down application"""
        app.closeAllWindows()

# ! starting the application
app = QApplication(sys.argv)

# ! creating main window and adding it to stack
mainwindow = MainGUI()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
# ! setting main window size
widget.setFixedWidth(400)
widget.setFixedHeight(580)

# ! setting main window title and Icon
widget.setWindowTitle("Chess Geeks")
widget.setWindowIcon(QtGui.QIcon("images/logo.png"))

# ! displaying main window
widget.show()

# ! getting previous windows current position
x = widget.pos().x()
y = widget.pos().y()

# ! execute app
app.exec()
