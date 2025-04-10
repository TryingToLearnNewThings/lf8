import random
from repositories.database_helper import DatabaseHelper


class QuestionRepository(DatabaseHelper):
    
    def __init__(self, connection=None):
        # Initialises the connection via the base class
        super().__init__(connection=connection)  
        self.question_id = None
        self.connection = connection

    def Get_questionids_with_categorys(self, category_id):
        
        self.cursor.execute(
            """
            SELECT questionID
            FROM Question
            WHERE categoryID = ?
            """,
            (category_id,),
        )
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def Get_random_questionID(self, question_ids):
        self.question_id = random.choice(question_ids)
        return self.question_id
        

    def Get_question(self):
        """
        Retrieves the question and the corresponding answers from the database.
        """
        self.cursor.execute(
            """ 
        SELECT question, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3, difficultyID
        FROM Question
        WHERE questionID = ?
        """,
            (self.question_id,),
        )
        row = (
            self.cursor.fetchone()
        )  # fetchone(), as only one question is expected

        if row:
            return {
                "questionText": row[0],
                "correctAnswer": row[1],
                "incorrectAnswer1": row[2],
                "incorrectAnswer2": row[3],
                "incorrectAnswer3": row[4],
                "difficultyID": row[5]
            }
        return None  # Returns None if no question was found

    def Get_correct_answer(self):
        self.cursor.execute(
            """ 
        SELECT correctAnswer FROM Question WHERE questionID = ?
        """,
            (self.question_id,),
        )
        row = self.cursor.fetchone()

        return row[0] if row else None

    def Create_question(self, question, category_id, difficulty_id, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3):
        """Fügt eine neue Frage in die Datenbank ein."""
        self.cursor.execute(
            """
            INSERT INTO Question (question, categoryID, difficultyID, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (question, category_id, difficulty_id, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3),
        )
        self.connection.commit()

        return "Question created! :)"

    def Get_question_by_id(self, question_id):
        
        # Query for the question and the answers
        self.cursor.execute("""
            SELECT question, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3
            FROM Question
            WHERE questionID = ?""", (question_id,))
        question_row = self.cursor.fetchone()

        if not question_row:
            return None

        # Extracting the answers
        answers = [
            {"answerText": question_row[1], "isCorrect": 1},  # Correct Answer
            {"answerText": question_row[2], "isCorrect": 0},  # False Answer 1
            {"answerText": question_row[3], "isCorrect": 0},  # False Answer 2
            {"answerText": question_row[4], "isCorrect": 0},  # False Answer 3
        ]

        return {
            "questionText": question_row[0],
            "correctAnswerIndex": 1,  # The correct answer always comes first
            "answers": answers,
        }
    
    def Update_question(self, questionID, question_text=None, answers=None, correct_answer_index=None):
        try:
            if question_text:
                self.cursor.execute(
                    "UPDATE Question SET question = ? WHERE questionID = ?",
                    (question_text, questionID),
                )

            if answers and correct_answer_index is not None:
                # Update the answers
                self.cursor.execute(
                    """
                    UPDATE Question
                    SET correctAnswer = ?, incorrectAnswers1 = ?, incorrectAnswers2 = ?, incorrectAnswers3 = ?
                    WHERE questionID = ?
                    """,
                    (
                        answers[correct_answer_index - 1],  # Korrekte Antwort
                        answers[0] if correct_answer_index != 1 else answers[1],  # First False Answer
                        answers[1] if correct_answer_index != 2 else answers[2],  # Second False Answer
                        answers[2] if correct_answer_index != 3 else answers[3],  # Third False Answer
                        questionID,
                    ),
                )

            self.con.commit()
            return "Question successfully updated!"
        except Exception as e:
            raise Exception(f"Error updating the question: {e}")

    def Delete_question(self, question_id):
        """
        Deletes a question from the question table based on the question ID.
        """
        try:
            self.cursor.execute(
                """
                DELETE FROM Question
                WHERE questionID = ?
                """,
                (question_id,),
            )
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Error deleting the question: {e}")

    def Get_question_points(self, question_id):
        cursor = self.con.cursor()
        cursor.execute(
            "SELECT difficultyPoints FROM Difficulty WHERE difficultyID = (SELECT difficultyID FROM Question WHERE questionID = ?)",
            (question_id,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


