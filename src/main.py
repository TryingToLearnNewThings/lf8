from repositories.question_repository import QuestionRepository
from question import Question

# from repositories.game_repository import GameRepository
from repositories.category_repository import CatecoryRepository
from repositories.difficulty_repository import DifficultyRepository
from repositories.achievment_repository import AchievmentRepository
from repositories.player_repository import PlayerRepository
from player import Player

category_repo = CatecoryRepository()
categoryID = category_repo.get_category_id_by_name("Politics")

q = Question("Sample question", ["Option1", "Option2"], "Option1", "Politics")
rq = QuestionRepository()
ids = rq.get_questionIDs_with_Categorys(categoryID)
rq.fill_game_question(ids, 1)
questionid = rq.get_random_questionID(1)
rq.get_question()
rq.get_correct_answer()
# rq.fill_right_or_wrong(1,1,1,True)
print(rq.get_question_points())

d = DifficultyRepository()
difficultyid = d.get_difficultyId_from_questionId(questionid)
print(difficultyid)
d.get_difficulty_points(difficultyid)
d.get_all_difficulties()

a = AchievmentRepository()
a.create_new_achievments(
    "correctEasyQuestions 20 or higher", "correctEasyQuestions", 20
)
requierments = a.get_requierments(1)
achievementName = a.get_achievment_name(1)
achievmentsInfos = a.get_all_achievements()
pr = PlayerRepository()
p = Player(
    player_id=1,
    name="Leon",
    player_password=123456,
    score=0,
    correctHardQuestions=10,
    correctMediumQuestions=5,
    correctEasyQuestions=20,
)
pr.get_playerID_by_name("Leon")
player_achievements = pr.get_all_player_achievements()
print(player_achievements)
check_achievment = p.receive_achievement(
    achievmentsInfos[0], achievmentsInfos[1], achievmentsInfos[2], player_achievements
)

if check_achievment:
    a.fill_player_to_achievments(p.player_id, check_achievment)
print(pr.get_player_achievments())

# new_value_correctanswer = pr.get_correct_Questions_by_difficulty("medium")
a.get_all_achievements()
