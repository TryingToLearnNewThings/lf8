import os
import sys
import sqlite3
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.achievment_repository import AchievmentRepository
from repositories.player_repository import PlayerRepository
from player import Player


class TestAchievementRepository(unittest.TestCase):
    def setUp(self):
        """Creates a temporary in-memory SQLite database for testing."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Creates the required table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Achievement (
                achievementID INTEGER PRIMARY KEY AUTOINCREMENT,
                achievementName TEXT UNIQUE,
                conditionType TEXT,
                value INTEGER
            );
        """)
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Player (
                    playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                    playerPassword TEXT,
                    playerName TEXT UNIQUE,
                    playerScore INTEGER,
                    playedGames INTEGER,
                    correctHardQuestions INTEGER,
                    correctMediumQuestions INTEGER,
                    correctEasyQuestions INTEGER
                );
            """)
        
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS PlayerToAchievement (
                    playerID INTEGER,
                    achievementID INTEGER,
                    FOREIGN KEY (playerID) REFERENCES Player(playerID),
                    FOREIGN KEY (achievementID) REFERENCES Achievement(achievementID)
                );
            """)
        self.conn.commit()
        

        # Initialises the repository
        self.achievement = AchievmentRepository(connection=self.conn)
        self.player_repo = PlayerRepository(connection=self.conn)

        # Add sample difficulty
        self.cursor.execute(
            "INSERT INTO Achievement (achievementName, conditionType, value) VALUES (?, ?, ?)",
            ('Get 10 hard questions correct', 'correctHardQuestions', 10)
        )
        self.cursor.execute(
            "INSERT INTO Achievement (achievementName, conditionType, value) VALUES (?, ?, ?)", 
            ("Get 10 medium questions correct", "correctMediumQuestions", 10)
            )
        self.conn.commit()
    # For the Player-Table:
        self.cursor.execute(
            "INSERT INTO Player (playerPassword, playerName, playerScore, correctHardQuestions, correctMediumQuestions, correctEasyQuestions) VALUES (?, ?, ?, ?, ?, ?)",
            (12345, "Marsl", 1000,100, 10, 30)
            )
        self.cursor.execute(
                "INSERT INTO PlayerToAchievement(playerID,achievementID) VALUES (?,?) ",
                    (1, 1),
                )
        self.conn.commit()
        
    def test_get_player_data(self):
        #given
        player_id = 1
        password =12345
        name = "Marsl"
        score = 1000
        correct_hard = 100
        correct_medium = 10
        correct_easy = 30
        player_id_new = self.player_repo.Player_login_check(name,password)
        
        #when
        playerID_for_ach = self.player_repo.Get_player_id()
        player_data = self.player_repo.Get_value_from_table("Player","playerID, playerScore, correctHardQuestions,correctMediumQuestions,correctEasyQuestions","playerID",playerID_for_ach)
        
        #then
        self.assertIsNotNone(player_id)
        self.assertEqual(player_id, player_id_new)
        self.assertEqual(player_id_new, playerID_for_ach)
        
        self.assertEqual(player_id_new, player_data[0])
        self.assertEqual(score, player_data[1])
        self.assertEqual(correct_hard, player_data[2])
        self.assertEqual(correct_medium, player_data[3])
        self.assertEqual(correct_easy, player_data[4])
        
    def test_get_all_references(self): 
        achievment_ids = [1,2]
        condition_types = ["correctHardQuestions","correctMediumQuestions"]
        values= [10,10]
        all_achievements = self.achievement.Get_all_achievements()
    
        self.assertEqual(achievment_ids, all_achievements[0])
        self.assertEqual(condition_types, all_achievements[1])
        self.assertEqual(values, all_achievements[2])
        
       
    def test_Get_all_player_achievements(self):
        password =12345
        name = "Marsl"
        achievment_nr = 1
        
        self.player_repo.Player_login_check(name,password)
        player_achievements = self.player_repo.Get_all_player_achievements()
        print(player_achievements)
        self.assertEqual(achievment_nr, player_achievements)
    
    
    def test_receive_achievement(self):
        password = 12345
        name = "Marsl"
        achievements_achieved = [2]
        
        self.player_repo.Player_login_check(name,password)
        playerID_for_ach = self.player_repo.Get_player_id()
        player_achievements = self.player_repo.Get_all_player_achievements()
        player_data = self.player_repo.Get_value_from_table("Player","playerID, playerScore, correctHardQuestions,correctMediumQuestions,correctEasyQuestions","playerID",playerID_for_ach)
        all_achievements = self.achievement.Get_all_achievements()
        player = Player(
                        player_id=player_data[0],  # player_id = 3
                        score=player_data[1],  # score = 1580
                        correctHardQuestions=player_data[2],  # correctHardQuestions = 10
                        correctMediumQuestions=player_data[3],  # correctMediumQuestions = 10
                        correctEasyQuestions=player_data[4]  # correctEasyQuestions = 10
                    )
        
        
        achievments_given = player.Receive_achievement(all_achievements[0],all_achievements[1], all_achievements[2], player_achievements)
        self.assertEqual(achievements_achieved, achievments_given)

    def test_fill_player_to_achievments(self):
        password =12345
        name = "Marsl"
        self.player_repo.Player_login_check(name,password)
        
        #when
        achievements = ((1,),(2,))
        player_data = 1
        check_achievment = [2]
        
        self.achievement.Fill_player_to_achievments(player_data, check_achievment)
        player_achievements = self.player_repo.Get_all_player_achievements()
        
        self.assertEqual(achievements, player_achievements)

        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestAchievementRepository("test_get_player_data"))
    suite.addTest(TestAchievementRepository("test_get_all_achievements"))
    suite.addTest(TestAchievementRepository("test_Get_all_player_achievements"))
    suite.addTest(TestAchievementRepository("test_fill_player_to_achievments"))
                 
    runner = unittest.TextTestRunner()            
    runner.run(suite)