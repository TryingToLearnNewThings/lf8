import sqlite3

con = sqlite3.connect("Database/database.db")
# Cursor-Objekt zum Ausführen von SQL-Befehlen
cursor = con.cursor()


# Standard User erstellen
cursor.execute(
    """INSERT INTO Player (playerPassword, Playername, playerScore,correctHardQuestions, correctMediumQuestions, correctEasyQuestions) 
               VALUES ("12345","Leon", 10,2, 40, 100) """
)
cursor.execute(
    """INSERT INTO Player (playerPassword, Playername, playerScore,correctHardQuestions,correctMediumQuestions , correctEasyQuestions)
               VALUES ("12345","Jana", 100, 10 ,20, 150) """
)
cursor.execute(
    """INSERT INTO Player (playerPassword, Playername, playerScore,correctHardQuestions, correctMediumQuestions, correctEasyQuestions)
               VALUES ("12345","Luka", 1000,10, 10, 10) """
)
# Änderungen speichern und Verbindung schließen
con.commit()
con.close()
