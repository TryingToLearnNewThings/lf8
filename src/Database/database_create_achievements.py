import sqlite3

con = sqlite3.connect("Database/database.db")
# Cursor-Objekt zum Ausführen von SQL-Befehlen
cursor = con.cursor()


# Achievements in die Tabelle einpflegen
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 hard questions correct", "correctHardQuestions", 10) """
)
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 medium questions correct", "correctMediumQuestions", 10) """
)
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 easy questions correct", "correctEasyQuestions", 10) """
)
# Änderungen speichern und Verbindung schließen
con.commit()
con.close()
