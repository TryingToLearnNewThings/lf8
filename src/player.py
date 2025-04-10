import sqlite3
import sys
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Database/database.db"))
con = sqlite3.connect(db_path)
cursor = con.cursor()


class Player:

    def __init__(
        self,
        player_id: int,
        score,
        correctHardQuestions,
        correctMediumQuestions,
        correctEasyQuestions,
    ):
        self.player_id = player_id
        self.score = score
        self.correctHardQuestions = correctHardQuestions
        self.correctMediumQuestions = correctMediumQuestions
        self.correctEasyQuestions = correctEasyQuestions


    def Receive_achievement(
    self, achievementIDs, requirements_fields, required_values, player_achievements
):
       # Ensure that player_achievements is a list of tuples
        achievement_avieved =[]
        if player_achievements is None:
            player_achievements = []
        elif isinstance(player_achievements, int):
            player_achievements = [(player_achievements,)]
        elif isinstance(player_achievements, (list, tuple)):
            # Make each entry a tuple, if necessary
            player_achievements = [
                (ach,) if isinstance(ach, int) else ach
                for ach in player_achievements
            ]

        # Set with IDs of the Achievements already received
        already_recieved_ids = {
            entry[0] for entry in player_achievements
            if isinstance(entry, (tuple, list)) and len(entry) > 0
        }

        # Go through all requirements and associated IDs
        for achievement_id, attribute_name, required_value in zip(achievementIDs, requirements_fields, required_values):

            # Check whether this Achievement already exists
            if achievement_id in already_recieved_ids:
                continue

            # Get the player's current value for the required attribute
            current_value = getattr(self, attribute_name, None)

            # If attribute exists and value is sufficient → Achievement awarded
            if current_value is not None and current_value >= required_value:
               
                achievement_avieved.append(achievement_id)
                print(f"Achievement {achievement_id} wird vergeben (für {attribute_name} ≥ {required_value})")
                
                # Here you could, for example, add the achievement to the player
                # For example: self.add_achievement(achievement_id)
        return achievement_avieved
    
    