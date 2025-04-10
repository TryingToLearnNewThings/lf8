import os
import sys
import sqlite3
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.question_repository import QuestionRepository

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestQuestionsRepository(unittest.TestCase):
    def setUp(self):
        """Erstellt eine temporäre In-Memory SQLite-Datenbank für den Test."""
        self.conn = sqlite3.connect(":memory:")  # In-Memory-DB
        self.cursor = self.conn.cursor()

        # Create table manually
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Question (
                questionID INTEGER PRIMARY KEY AUTOINCREMENT,
                categoryID INTEGER,
                difficultyID INTEGER,
                question TEXT UNIQUE NOT NULL,
                correctAnswer TEXT NOT NULL,
                incorrectAnswers1 TEXT NOT NULL,
                incorrectAnswers2 TEXT NOT NULL,
                incorrectAnswers3 TEXT NOT NULL
            );
        """
        )
        self.conn.commit()

         # Repository now uses the in-memory DB via the connection
        self.questions = QuestionRepository(connection=self.conn)

        # Add a sample question that will be used in the tests
        self.cursor.execute(
            """
            INSERT INTO Question (question, categoryID, difficultyID, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("Was ist die Hauptstadt von Frankreich?", 1, 1, "Paris", "Berlin", "Madrid", "Rom"),
        )
        self.conn.commit()
        
    def test_create_question(self):
        #given
        """Testet, ob eine Frage erfolgreich hinzugefügt werden kann."""
        new_question = "Was ist die Hauptstadt von Deutschland?"

        #when
        # Here you simply call the method that contains the SQL command
        self.questions.Create_question(new_question, 1, 1, "Berlin", "Hamburg", "München", "Bielefeld")
        
        # Überprüfe, ob die Frage in der Datenbank ist
        self.cursor.execute("SELECT question FROM Question WHERE question = ?", (new_question,))
        result = self.cursor.fetchone()
        
        #then
        self.assertIsNotNone(result)  # Prüfen, ob die Frage existiert
        self.assertEqual(result[0], new_question)        
        
        

    def test_update_question(self):
        #given
        field = "question"
        new_data = "Was ist die Stadt mit den meisten Einwohnern in Deutschland"
        question_id = 1
        
        #when
        self.questions.Update_question(question_id, new_data)
        self.cursor.execute("SELECT question FROM Question WHERE questionID = ?", (question_id,))
        result = self.cursor.fetchone()
        
        #then
        self.assertIsNotNone(result)
        self.assertEqual(result[0], new_data)  

    def test_remove_question(self):
        question_id = 1
        self.questions.Delete_question(question_id)
        self.assertIsNone(self.questions.Get_question())

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestQuestionsRepository("test_create_question"))
    suite.addTest(TestQuestionsRepository("test_update_question"))
    suite.addTest(TestQuestionsRepository("test_remove_question"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
