import sqlite3

con = sqlite3.connect("Database/database.db")
# Cursor object for executing SQL commands
cursor = con.cursor()


# Add Achievements to the table
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 hard questions correct", "correctHardQuestions", 10) """
)
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 medium questions correct", "correctMediumQuestions", 10) """
)
cursor.execute(
    """INSERT INTO Achievement (achievementName, conditionType, value) VALUES ("Get 10 easy questions correct", "correctEasyQuestions", 10) """
)
# Save changes and close connection
con.commit()
con.close()
