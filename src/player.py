import sqlite3

con = sqlite3.connect("Database/database.db")
cursor = con.cursor()


class Player:

    def __init__(
        self,
        name: str,
        player_id: int,
        player_password,
        score,
        correctHardQuestions,
        correctMediumQuestions,
        correctEasyQuestions,
    ):
        self.name = name
        self.player_id = player_id
        self.password = player_password
        self.score = score
        self.correctHardQuestions = correctHardQuestions
        self.correctMediumQuestions = correctMediumQuestions
        self.correctEasyQuestions = correctEasyQuestions


    def receive_achievement(
    self, achievementIDs, requirements_fields, required_values, player_achievements
):
       # Sicherstellen, dass player_achievements eine Liste von Tupeln ist
        achievement_avieved =[]
        if player_achievements is None:
            player_achievements = []
        elif isinstance(player_achievements, int):
            player_achievements = [(player_achievements,)]
        elif isinstance(player_achievements, (list, tuple)):
            # Jeden Eintrag zu einem Tuple machen, falls nötig
            player_achievements = [
                (ach,) if isinstance(ach, int) else ach
                for ach in player_achievements
            ]

        # Set mit IDs der bereits erhaltenen Achievements
        already_recieved_ids = {
            entry[0] for entry in player_achievements
            if isinstance(entry, (tuple, list)) and len(entry) > 0
        }

        # Durch alle Anforderungen und zugehörigen IDs gehen
        for achievement_id, attribute_name, required_value in zip(achievementIDs, requirements_fields, required_values):

            # Prüfen, ob dieses Achievement bereits vorhanden ist
            if achievement_id in already_recieved_ids:
                continue

            # Den aktuellen Wert des Spielers für das geforderte Attribut holen
            current_value = getattr(self, attribute_name, None)

            # Wenn Attribut existiert und Wert ausreicht → Achievement vergeben
            if current_value is not None and current_value >= required_value:
               
                achievement_avieved.append(achievement_id)
                print(f"Achievement {achievement_id} wird vergeben (für {attribute_name} ≥ {required_value})")
                
                # Hier könntest du z. B. das Achievement dem Spieler hinzufügen
               # Zum Beispiel: self.add_achievement(achievement_id)
        return achievement_avieved
    
    