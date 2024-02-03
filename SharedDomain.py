import mysql.connector as mc

class Shared():
    """This class holds all the variables that are used"""

    # a list the hold a reference to all the widgets so that it can be removed
    all_widgits = []

    # Player Name
    playerName = "unKnown GM"

    # Player color
    playas = 1 # 1 = white , 2 = Black

    # Player Winner Flage ->  So that it can be added to the scores
    playerWon = False # NOTE: it is set to True in "ChessMain" when the player wins

    # game varibles
    level = 1; #  = Easy , 2 = Normal , 3 =  Hard
    timetaken = 0;
    movesmade = 0;
    starttime = 0

    # Theme
    # this is the default Theme
    Theme = {
            "path": "images/3/",
            "colorA": "white",
            "colorB": "gray",
            }
    # connection string
    try:
        conn = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="chess"
        )
    except mc.Error:
        print("connection failed: Could not load the connection string")

