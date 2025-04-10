from repositories.database_helper import DatabaseHelper


class AchievmentRepository(DatabaseHelper):
    # no Init, as the AchievementID can change. This eliminates the benefit
    def Get_achievment_name(self, achievement_id):
        return self.Get_value_from_table(
            "Achievement", "achievementName", "achievementID", achievement_id
        )
    
    # Connects the player to his achievements
    def Fill_player_to_achievments(
        self, player_id, achievement_id,
    ):
        for i in achievement_id:
            self.cursor.execute(
                    """INSERT INTO PlayerToAchievement(playerID,achievementID) VALUES (?,?) """,
                    (player_id, i),
                )
            self.con.commit()
            print("You have achieved a new achievements")

    def Create_new_achievments(self, achievement_name, condition_type, value):
        self.cursor.execute(
            """INSERT INTO Achievement (achievementName, conditionType, value) VALUES (?, ?,?) """,
            (achievement_name, condition_type, value),
        )
        self.con.commit()
        
   

    # Gets the requirement to fulfil the Achievements
    def Get_requierments(self, achievement_id):
        requierments = self.Get_value_from_table(
            "Achievement", "conditionType, value", "achievementID", achievement_id
        )
        print(requierments)
        return requierments
    
    
    
    def Get_all_achievements(self):
        self.cursor.execute(""" SELECT * FROM Achievement""")
        rows = self.cursor.fetchall()
        return([row[0] for row in rows]),([row[2] for row in rows]),([row[3] for row in rows])
