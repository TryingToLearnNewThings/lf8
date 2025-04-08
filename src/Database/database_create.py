import sqlite3
import sys
import os

# Füge den Hauptordner zum Python-Suchpfad hinzu
# Verbindung zur SQLite-Datenbank
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
con = sqlite3.connect("Database/database.db")
cursor = con.cursor()


# Benötigte Tabellen erstellen
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
    playedGames INTEGER,
    correctHardQuestions INTEGER,
    correctMediumQuestions INTEGER,
    correctEasyQuestions INTEGER
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Game (
    gameID INTEGER PRIMARY KEY AUTOINCREMENT,
    gameDate DATE,
    gameKey TEXT
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS PlayerOfGame (
    gameID INTEGER,
    playerID INTEGER,
    FOREIGN KEY (playerID) REFERENCES Player(playerID),
    FOREIGN KEY (gameID) REFERENCES Game(gameID)
);
"""
)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS GameQuestion (
    gameID INTEGER,
    questionID INTEGER,
    played INTEGER,
    FOREIGN KEY (questionID) REFERENCES Question(questionID),
    FOREIGN KEY (gameID) REFERENCES Game(gameID)
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

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS RightOrWrong (
    playerID INTEGER,
    questionID INTEGER,
    gameID INTEGER,
    answerCorrectly INTEGER,
    FOREIGN KEY (playerID) REFERENCES Player(playerID),
    FOREIGN KEY (questionID) REFERENCES Question(questionID),
    FOREIGN KEY (gameID) REFERENCES Game(gameID)
);
"""
)

# Änderungen speichern und Verbindung schließen
con.commit()
con.close()
