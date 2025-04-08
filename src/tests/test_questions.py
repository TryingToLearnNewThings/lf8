import os
import sys
import sqlite3
import unittest
#from ..repositories.database_helper import DatabaseHelper
#from repositories.question_repository import QuestionRepository
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.question_repository import QuestionRepository

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestQuestionsRepository(unittest.TestCase):
    def setUp(self):
        """Erstellt eine temporäre In-Memory SQLite-Datenbank für den Test."""
        self.conn = sqlite3.connect(":memory:")  # In-Memory-DB
        self.cursor = self.conn.cursor()

        # Tabelle manuell erstellen
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

         # Repository nutzt jetzt die in-memory DB über die Verbindung
        self.questions = QuestionRepository(connection=self.conn)

        # Füge eine Beispiel-Frage hinzu, die in den Tests verwendet wird
        self.cursor.execute(
            "INSERT INTO Question (categoryID, difficultyID, question, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, 1, "Was ist die Hauptstadt von Frankreich?", "Paris", "Berlin", "Madrid", "Rom")
        )
        self.conn.commit()
        
    def test_create_question(self):
        #givene
        """Testet, ob eine Frage erfolgreich hinzugefügt werden kann."""
        new_question = "Was ist die Hauptstadt von Deutschland?"

        #when
        # Hier rufst du einfach die Methode auf, die den SQL-Befehl enthält
        self.questions.create_question(new_question, 1, 1, "Berlin", "Hamburg", "München", "Bielefeld")
        
        # Überprüfe, ob die Frage in der Datenbank ist
        self.cursor.execute("SELECT question FROM Question WHERE question = ?", (new_question,))
        result = self.cursor.fetchone()
        
        #then
        self.assertIsNotNone(result)  # Prüfen, ob die Frage existiert
        self.assertEqual(result[0], new_question)        
        
        

    def test_update_question(self):
        #given
        field = "question"
        newData = "Was ist die Stadt mit den meisten Einwohnern in Deutschland"
        questionID = 1
        #when
        self.questions.update_question(questionID, field, newData)
        self.cursor.execute("SELECT question FROM Question WHERE questionID = ?", (questionID,))
        result = self.cursor.fetchone()
        #then
        self.assertIsNotNone(result)  # Prüfen, ob die Frage existiert
        self.assertEqual(result[0], newData)  

    def test_remove_question(self):
        # Testet, ob eine Frage erfolgreich entfernt wird
        questionID = 1
        self.questions.delete_question(questionID)
        self.assertIsNone(self.questions.get_question())

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestQuestionsRepository("test_create_question"))
    suite.addTest(TestQuestionsRepository("test_update_question"))
    suite.addTest(TestQuestionsRepository("test_remove_question"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
