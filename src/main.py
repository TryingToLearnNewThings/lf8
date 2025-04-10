# from repositories.question_repository import QuestionRepository
# from repositories.category_repository import CategoryRepository
# from repositories.difficulty_repository import DifficultyRepository
# from repositories.achievment_repository import AchievmentRepository
# from repositories.player_repository import PlayerRepository
# from player import Player

# from GUI import achievement_screen
# from GUI import category_screen
# from GUI import createacc_screen
# from GUI import entryScreen
# from GUI import gameplay_screen
# from GUI import helper_screen
# from GUI import leaderboard_screen
from GUI.login_screen import Login_Class


if __name__ == "__main__":
   login_instance = Login_Class()
   login_instance.Login_screen()