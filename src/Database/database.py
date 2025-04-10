import sqlite3
import json

# Connection to the SQLite database
conn = sqlite3.connect("Database/database.db")
cursor = conn.cursor()

# Load JSON file
with open("Database/test_fragen.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Cache Category and Difficulty (so that IDs are not saved twice)
category_cache = {}
difficulty_cache = {}

# Go through JSON data
for entry in data["results"]:
    category_name = entry["category"]
    difficulty_name = entry["difficulty"]

    # Insert category
    if category_name not in category_cache:
        cursor.execute(
            "INSERT OR IGNORE INTO Category (categoryName) VALUES (?)", (category_name,)
        )
        category_cache[category_name] = cursor.lastrowid

    # Insert difficulty
    if difficulty_name not in difficulty_cache:
        if difficulty_name == "easy":
            Points = 1000
        elif difficulty_name == "medium":
            Points = 1500
        else:
            Points = 2000
        cursor.execute(
            "INSERT OR IGNORE INTO Difficulty (difficultyName, difficultyPoints) VALUES (?, ?)",
            (difficulty_name, Points),
        )  # Adjust points
        difficulty_cache[difficulty_name] = cursor.lastrowid

    # Retrieve category and difficulty ID
    cursor.execute(
        "SELECT CategoryID FROM Category WHERE categoryName = ?", (category_name,)
    )
    category_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT DifficultyID FROM Difficulty WHERE difficultyName = ?",
        (difficulty_name,),
    )
    difficulty_id = cursor.fetchone()[0]

    # Insert question into the database
    incorrects = entry["incorrect_answers"]
    cursor.execute(
        """
        INSERT INTO Question (categoryID, difficultyID, question, correctAnswer, incorrectAnswers1, incorrectAnswers2, incorrectAnswers3)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            category_id,
            difficulty_id,
            entry["question"],
            entry["correct_answer"],
            incorrects[0] if len(incorrects) > 0 else None,
            incorrects[1] if len(incorrects) > 1 else None,
            incorrects[2] if len(incorrects) > 2 else None,
        ),
    )

# Save changes and close connection
conn.commit()
conn.close()

print("✅ JSON data successfully saved in SQLite!")
