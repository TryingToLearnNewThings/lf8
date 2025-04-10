import sqlite3
from repositories.database_helper import DatabaseHelper


class DifficultyRepository(DatabaseHelper):
    def __init__(self, connection=None):
        super().__init__(connection=connection)  # Initialisiert die Verbindung über die Basisklasse
        self.question_id = None
    
    def get_difficulty_infos(self, get_field,search_field, search_field_value):
        return self.Get_value_from_table(
            "Difficulty", get_field, search_field, search_field_value)

    
    def Get_all_difficulties(self):
        self.cursor.execute("SELECT * FROM Difficulty")
        difficulties = self.cursor.fetchall()

        # Mapping von Schwierigkeit zu Farben
        color_map = {
            "easy": "green",
            "medium": "yellow",
            "hard": "red"
        }

        # Mapping zusammenbauen
        difficulty_mapping = {
            diff[0]: (diff[1], color_map.get(diff[1], "gray")) for diff in difficulties}

        return difficulty_mapping
    
    
    def Update_points(self, new_points, difficulty_id):
        self.cursor.execute(
            """ 
        UPDATE Difficulty SET difficultyPoints = ? WHERE difficultyID = ?
        """,
            (
                new_points,
                difficulty_id,
            ),
        )
        self.con.commit()
