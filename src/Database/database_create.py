import sqlite3
import sys
import os

# Add the main folder to the Python search path
# Connection to the SQLite database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
con = sqlite3.connect("Database/database.db")
cursor = con.cursor()


# Create required tables
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Category (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT UNIQUE NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Difficulty (
    difficultyID INTEGER PRIMARY KEY AUTOINCREMENT,
    difficultyName TEXT UNIQUE NOT NULL,
    difficultyPoints INTEGER NOT NULL
);
"""
)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Question (
    questionID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryID INTEGER,
    difficultyID INTEGER,
    question TEXT UNIQUE NOT NULL,
    correctAnswer TEXT NOT NULL,
    incorrectAnswers1 TEXT NOT NULL,
    incorrectAnswers2 TEXT NOT NULL,
    incorrectAnswers3 TEXT NOT NULL,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID),
    FOREIGN KEY (difficultyID) REFERENCES Difficulty(difficultyID)
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Player (
    playerID INTEGER PRIMARY KEY AUTOINCREMENT,
    playerPassword TEXT,
    playerName TEXT UNIQUE,
    playerScore INTEGER,
    correctHardQuestions INTEGER,
    correctMediumQuestions INTEGER,
    correctEasyQuestions INTEGER
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Achievement (
    achievementID INTEGER PRIMARY KEY AUTOINCREMENT,
    achievementName TEXT UNIQUE,
    conditionType TEXT,
    value INTEGER
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS PlayerToAchievement (
    playerID INTEGER,
    achievementID INTEGER,
    FOREIGN KEY (playerID) REFERENCES Player(playerID),
    FOREIGN KEY (achievementID) REFERENCES Achievement(achievementID)
);
"""
)

# Save changes and close connection
con.commit()
con.close()
