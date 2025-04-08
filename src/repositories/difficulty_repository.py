import sqlite3
from repositories.database_helper import DatabaseHelper


class DifficultyRepository(DatabaseHelper):
    def __init__(self, connection=None):
        super().__init__(connection=connection)  # Initialisiert die Verbindung über die Basisklasse
        self.question_id = None
    
    def get_difficultyId_from_questionId(self, questionID):
        return self.get_value_from_table(
            "Question", "difficultyID", "questionID", questionID
        )

    def get_difficulty_points(self, difficultyID):
        return self.get_value_from_table(
            "Difficulty", "difficultyPoints", "difficultyID", difficultyID
        )

    def get_difficultyid_by_difficultyname(self, difficultyName):
        return self.get_value_from_table(
            "Difficulty", "difficultyID", "difficultyName", difficultyName
        )

    def get_all_difficulties(self):
        self.cursor.execute(
            """ 
        SELECT * FROM Difficulty
        """
        )
        difficulties = self.cursor.fetchall()
        print(difficulties)
        return [difficulties[0] for difficulties in difficulties]
    
    
    def update_points(self, newPoints, difficultyID):
        self.cursor.execute(
            """ 
        UPDATE Difficulty SET difficultyPoints = ? WHERE difficultyID = ?
        """,
            (
                newPoints,
                difficultyID,
            ),
        )
        self.con.commit()
