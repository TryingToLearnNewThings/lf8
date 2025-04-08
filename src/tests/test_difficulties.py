import os
import sys
import sqlite3
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.difficulty_repository import DifficultyRepository

class TestDifficultiesRepository(unittest.TestCase):
    def setUp(self):
        """Creates a temporary in-memory SQLite database for testing."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Creates the required tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Difficulty (
                difficultyID INTEGER PRIMARY KEY AUTOINCREMENT,
                difficultyName TEXT UNIQUE NOT NULL,
                difficultyPoints INTEGER NOT NULL
            );
        """)
        self.conn.commit()

        # Initialize repository with test connection
        self.difficulties = DifficultyRepository(connection=self.conn)

        # Add sample difficulty
        self.cursor.execute(
            "INSERT INTO Difficulty (difficultyName, difficultyPoints) VALUES (?, ?)",
            ("Easy", 100)
        )
        self.conn.commit()

    def test_update_points(self):
        # given
        difficultyID = 1
        new_points = 200

        # when
        self.difficulties.update_points(new_points, difficultyID)
        
        # then
        self.cursor.execute("SELECT difficultyPoints FROM Difficulty WHERE difficultyID = ?", (difficultyID,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], new_points)

    def test_get_difficulty_points(self):
        # given
        difficultyID = 1
        expected_points = 100

        # when
        points = self.difficulties.get_difficulty_points(difficultyID)

        # then
        self.assertEqual(points, expected_points)

    def test_get_all_difficulties(self):
        # given
        self.cursor.execute(
            "INSERT INTO Difficulty (difficultyName, difficultyPoints) VALUES (?, ?)",
            ("Medium", 200)
        )
        self.conn.commit()

        # when
        difficulties = self.difficulties.get_all_difficulties()
        self.cursor.execute("SELECT difficultyName FROM Difficulty")
        result = self.cursor.fetchall()
        result = [row[0] for row in result]
        # then
        expected_difficulties = ["Easy", "Medium"]
        self.assertIsNotNone(result)
        self.assertEqual(result, expected_difficulties)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestDifficultiesRepository("test_update_points"))
    suite.addTest(TestDifficultiesRepository("test_get_difficulty_points"))
    suite.addTest(TestDifficultiesRepository("test_get_all_difficulties"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)