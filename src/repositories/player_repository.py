from repositories.database_helper import DatabaseHelper
import sqlite3


class PlayerRepository(DatabaseHelper):
    def __init__(self, connection=None):
        super().__init__(connection=connection)
        self.player_id = None 


    def Get_playerfield_info(self,field):
        return self.Get_value_from_table("Player",field, "playerID", self.player_id)

    def Player_login_check(self, player_name, player_password):
        self.cursor.execute(
            """
            SELECT playerID FROM Player WHERE playerName =? AND playerPassword = ?
            """,
            (player_name, player_password),
        )
        result = self.cursor.fetchone()

        if result:
            self.player_id = result[0]
            return self.player_id
        else:
            return None
    
    def Get_player_achievments(self):
        self.cursor.execute(
            """
                            SELECT pta.achievementID, a.achievementID  
                            FROM PlayerToAchievement pta
                            JOIN Achievement a
                            ON a.achievementID = pta.achievementID
                            WHERE pta.playerID = ?
                            """,
            (self.player_id,),
        )
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    
    
    def Get_all_player_infos_by_name(self, player_name): 
        self.Get_value_from_table("Player", "*", "playerName", player_name)
        
    def Update_player_field(self,update_field, new_value):
       self.Update_field_value("Player", update_field, new_value, self.player_id, "playerID")
    
    def create_user(self, player_name, player_password):
        self.cursor.execute(
            """ INSERT INTO Player(playerName, playerPassword) VALUES (?,?)""",
            (
                player_name,
                player_password,
            ),
        )
        self.con.commit()
        return

    def Get_all_player_achievements(self):
        return self.Get_value_from_table(
            "PlayerToAchievement", "achievementID", "playerID", self.player_id
        )

    def Update_high_score(self,player_id, new_score):
        current_score = self.Get_value_from_table("Player", "playerScore", "playerID", self.player_id)
        if current_score == None or new_score > current_score:
            self.Update_field_value("Player", "playerScore", new_score, self.player_id, "playerID")
            print(f"Player {player_id} score updated to {new_score}.")
            
    def Get_player_id(self):
        return self.player_id
            

    def Get_all_players_sorted_by_score(self):
        self.cursor.execute(
            """SELECT playerName, playerScore FROM Player ORDER BY playerScore DESC"""
        )
        rows = self.cursor.fetchall()
        return [{"playerName": row[0], "playerScore": row[1]} for row in rows]
    
    def Achievment_player_info(self):
        self.cursor.execute(""" 
                            SELECT 
                                a.achievementName, 
                                CASE 
                                    WHEN ap.achievementID IS NOT NULL THEN 'Achieved' 
                                    ELSE 'Not Achieved' 
                                END AS achievementStatus
                            FROM 
                                Achievement a
                            LEFT JOIN 
                                PlayerToAchievement ap ON a.achievementID = ap.achievementID
                            LEFT JOIN 
                                Player p ON ap.playerID = p.playerID
                            WHERE 
                                p.playerID = ?
                            """, (self.player_id,)  # Add the comma here so that it is interpreted as a tuple.
                        )

        self.con.commit()
        results = self.cursor.fetchall()

        # Conversion of the results into a dictionary
        achievements = []
        for achievement in results:
            achievements.append({
                "name": achievement[0],  # Name of the Achievement
                "achieved": achievement[1] == 'Achieved',  # Status als boolean
            })
        
        return achievements 
    
    
