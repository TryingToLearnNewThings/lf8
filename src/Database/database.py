import sqlite3
import json

# Verbindung zur SQLite-Datenbank
conn = sqlite3.connect("Database/database.db")
cursor = conn.cursor()

# JSON-Datei laden
with open("Database/test_fragen.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Category und Difficulty zwischenspeichern (damit IDs nicht doppelt gespeichert werden)
category_cache = {}
difficulty_cache = {}

# JSON-Daten durchgehen
for entry in data["results"]:
    category_name = entry["category"]
    difficulty_name = entry["difficulty"]

    # Kategorie einfügen (falls noch nicht vorhanden)
    if category_name not in category_cache:
        cursor.execute(
            "INSERT OR IGNORE INTO Category (categoryName) VALUES (?)", (category_name,)
        )
        category_cache[category_name] = cursor.lastrowid

    # Schwierigkeitsgrad einfügen (falls noch nicht vorhanden)
    if difficulty_name not in difficulty_cache:
        if difficulty_name == "easy":
            Points = 1
        elif difficulty_name == "medium":
            Points = 2
        else:
            Points = 3
        cursor.execute(
            "INSERT OR IGNORE INTO Difficulty (difficultyName, difficultyPoints) VALUES (?, ?)",
            (difficulty_name, Points),
        )  # Punkte anpassen
        difficulty_cache[difficulty_name] = cursor.lastrowid

    # Kategorie- und Schwierigkeits-ID abrufen
    cursor.execute(
        "SELECT CategoryID FROM Category WHERE categoryName = ?", (category_name,)
    )
    category_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT DifficultyID FROM Difficulty WHERE difficultyName = ?",
        (difficulty_name,),
    )
    difficulty_id = cursor.fetchone()[0]

    # Frage in die Datenbank einfügen
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

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ JSON-Daten erfolgreich in SQLite gespeichert!")
