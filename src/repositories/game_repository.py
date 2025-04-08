import datetime
import uuid
from repositories.database_helper import DatabaseHelper


class GameRepository(DatabaseHelper):
    def create_game(self, creatorID):
        con = self.get_connection()
        cursor = con.cursor()
        date = datetime.datetime.now()
        dateForm = date.strftime("%c")

        game_key = str(uuid.uuid4())[:8]  # Kürzerer Code für das Spiel

        # Verwende den korrekten Spaltennamen "gameDate"
        cursor.execute(
            "INSERT INTO Game (gameDate, gameKey) VALUES (?, ?, ?)",
            (dateForm, game_key, creatorID),
        )
        con.commit()
        con.close()
        return game_key

    def get_gameID(self, gameCode):
        return self.get_value_from_table("Game", "gameID", "gameKey", gameCode)

    def fill_player_of_game(self, playerID, gameID):
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO PlayerOfGame (playerID, gameID) VALUES (?, ?)",
            (playerID, gameID),
        )
        con.commit()
        con.close()

    def get_player_score_ingame(self):
        return
