from flask import Flask, request, jsonify
from flask_cors import CORS
from repositories.player_repository import PlayerRepository
from repositories.game_repository import GameRepository
from repositories.question_repository import QuestionRepository
from repositories.difficulty_repository import DifficultyRepository

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize repositories
player_repo = PlayerRepository()
game_repo = GameRepository()
question_repo = QuestionRepository()
difficulty_repo = DifficultyRepository()


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    player_name = data.get("playerName")
    player_password = data.get("playerPassword")

    if player_repo.get_playerID_by_name(player_name):
        return jsonify({"message": "Player already exists"}), 400

    player_repo.create_player(player_name, player_password)
    return jsonify({"message": "Player registered successfully"}), 201


@app.route("/create_game", methods=["POST"])
def create_game():
    data = request.json
    creator_id = data.get("creatorID")
    if not creator_id:
        return jsonify({"error": "Creator ID is required"}), 400

    try:
        # Create a new game and generate a game key
        game_key = game_repo.create_game(creator_id)
        game_id = game_repo.get_gameID(
            game_key
        )  # Retrieve the game ID based on the game key
        return jsonify({"game_key": game_key, "gameID": game_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_questions/<int:game_id>", methods=["GET"])
def get_questions(game_id):
    try:
        questions = question_repo.get_random_questions(
            5
        )  # müsste das hier nicht die Variable Game_id sein?
        if not questions:
            return jsonify({"error": "Not enough questions available"}), 400

        question_repo.assign_questions_to_game(
            game_id, questions
        )  # woher kommt die Funktion? Meint ihr fill_game_question?
        return jsonify({"questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/submit_answer", methods=["POST"])
def submit_answer():  # wie funktioniert das hier genau mit data.get?
    data = request.json
    player_id = data.get("playerID")
    question_id = data.get("questionID")
    game_id = data.get("gameID")
    answer = data.get("answer")

    try:
        is_correct = question_repo.check_answer(
            question_id, answer
        )  # ist damit get_correct_answer gemeint? zudem muss neuerdings keine questionID mehr übergeben werden
        if is_correct:
            player_repo.increment_score(player_id)
            question_repo.mark_question_as_played(
                game_id, question_id
            )  # diese Funktion gibt es auch nicht, ist question_played (gab es bis eben nicht)?
            return jsonify({"correct": True}), 200

        return jsonify({"correct": False}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/join_game", methods=["POST"])
def join_game():
    data = request.json
    game_key = data.get("game_key")
    player_id = data.get("playerID")

    if not game_key or not player_id:
        return jsonify({"error": "Game Key and Player ID are required"}), 400

    try:
        if not game_repo.game_exists(game_key):
            return jsonify({"error": "Game not found"}), 404

        game_id = game_repo.get_gameID(
            game_key
        )  # Retrieve the game ID based on the game key
        game_repo.fill_player_of_game(player_id, game_id)  # Add the player to the game
        return jsonify({"message": "Player joined successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/end_game/<int:game_id>", methods=["GET"])
def end_game(game_id):
    try:
        winner = game_repo.get_winner(game_id)
        if not winner:
            return jsonify({"error": "No players in the game"}), 400

        return jsonify({"winner": winner}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
