import unittest
import os
import sys
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.player_repository import PlayerRepository


class TestPlayerRepository(unittest.TestCase):
    def setUp(self):
        """Erstellt eine temporäre In-Memory SQLite-Datenbank für den Test."""
        self.conn = sqlite3.connect(":memory:")  # In-Memory-DB
        self.cursor = self.conn.cursor()

        # Create table manually
        self.cursor.execute(
            """
                       CREATE TABLE IF NOT EXISTS Player (
                       playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                       playerPassword TEXT,
                       playerName TEXT UNIQUE,
                       playerScore INTEGER,
                       playerWins TEXT,
                       playedGames INTEGER,
                       correctHardQuestions INTEGER,
                       correctMediumQuestions INTEGER,
                       correctEasyQuestions INTEGER
                       );       
                    """
        )
        self.conn.commit()

        # Repository now uses the in-memory DB via the connection
        self.player = PlayerRepository(connection=self.conn)
        
        self.cursor.execute(
            "INSERT INTO Player(playerPassword, playerName, playerScore, playerWins, playedGames, correctHardQuestions, correctMediumQuestions, correctEasyQuestions) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
            (12345, "Marsl", 1000, 10, 10, 100, 20, 30)
        )
        self.conn.commit()

    def test_create_Player(self):
        # given
        player_name = "Marsle"
        player_pass = "123456"

        # when
        # Add the player to the database and see if it was successful
        self.player.create_user(player_name, player_pass)
        self.cursor.execute(
            "SELECT playerName FROM Player WHERE playerName = ? AND playerPassword = ?",
            (player_name, player_pass),
        )
        result = self.cursor.fetchone()
        # then
        self.assertIsNotNone(result)  # Check whether the player exists
        self.assertEqual(result[0], player_name, player_pass)

    def test_update_playerField(self):
        # given
        player_id = 1
        # player_name = "Marsl"
        new_value = "Leon"

        # when
        self.player.Update_field_value(
            "Player", "playerName", new_value,player_id , "playerID"
        )

        self.cursor.execute(
            """SELECT playerName FROM Player WHERE playerID = ?""", (player_id,)
        )
        result = self.cursor.fetchone()

        # then
        self.assertIsNotNone(result)
        self.assertEqual(result[0], new_value)

    def tearDown(self):
        """Schließt die Verbindung nach jedem Test."""
        self.conn.close()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestPlayerRepository("test_create_Player"))
    suite.addTest(TestPlayerRepository("test_update_playerField"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
