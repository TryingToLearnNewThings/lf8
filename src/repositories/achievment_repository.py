from repositories.database_helper import DatabaseHelper


class AchievmentRepository(DatabaseHelper):
    # kein Init, da die AchievementsID wechseln kann. Dadurch entfällt der nutzen
    def get_achievment_name(self, achievementID):
        return self.get_value_from_table(
            "Achievement", "achievementName", "achievementID", achievementID
        )
    
    # Verbindet den Player zu seinen Achievements
    def fill_player_to_achievments(
        self, playerID, achievementID,
    ):
        for i in achievementID:
            self.cursor.execute(
                    """INSERT INTO PlayerToAchievement(playerID,achievementID) VALUES (?,?) """,
                    (playerID, i),
                )
            self.con.commit()
            print("You have achieved a new achievements")

    def create_new_achievments(self, achievementName, conditionType, value):
        self.cursor.execute(
            """INSERT INTO Achievement (achievementName, conditionType, value) VALUES (?, ?,?) """,
            (achievementName, conditionType, value),
        )
        self.con.commit()
        
    # holt die Anforderung zur erfüllung der Achievements
    def get_requierments(self, achievementID):
        requierments = self.get_value_from_table(
            "Achievement", "conditionType, value", "achievementID", achievementID
        )

        print(requierments)
        return requierments
    
    def get_all_achievements(self):
        self.cursor.execute(""" SELECT * FROM Achievement""")
        rows = self.cursor.fetchall()
        return([row[0] for row in rows]),([row[2] for row in rows]),([row[3] for row in rows])
