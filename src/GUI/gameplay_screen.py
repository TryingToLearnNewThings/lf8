import sys
import os
import random

# Füge den Hauptordner `src` zum Python-Suchpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox
from repositories.question_repository import QuestionRepository
from repositories.player_repository import PlayerRepository


class GameplayScreen:
    def __init__(self, category_id):
        self.category_id = category_id
        self.question_repo = QuestionRepository()
        self.current_question = None
        self.score = 0
        self.question_ids = self.question_repo.get_random_questionID(
            self.question_repo.get_questionIDs_with_Categorys(self.category_id))
    
        self.current_question_index = 0
        self.time_left = 10  # Timer in Sekunden

        # Initialisiere das Hauptfenster
        self.root = tk.Tk()
        self.root.title("Quiz-Spiel")
        self.root.geometry("1200x800")  # Breite x Höhe
        self.root.configure(bg="#2e2e2e")

        # Schriftarten und Farben
        self.label_font = ("Helvetica", 16, "bold")
        self.btn_font = ("Helvetica", 14, "bold")
        self.btn_bg = "#444444"
        self.btn_fg = "#DDDDDD"

        # GUI-Elemente erstellen
        self.create_widgets()

        # Erste Frage laden
        self.load_next_question()

        self.root.mainloop()

    def create_widgets(self):
        # Frame für die Frage
        self.question_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
            wraplength=700,
        )
        self.question_label.pack()

        # Frame für die Antwort-Buttons
        self.answer_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.answer_frame.pack(pady=20)

        self.answer_buttons = []
        # Maximal 4 Antwortmöglichkeiten
        for i in range(4):  
            btn = tk.Button(
                self.answer_frame,
                text="",
                font=self.btn_font,
                bg=self.btn_bg,
                fg=self.btn_fg,
                relief="flat",
                command=lambda i=i: self.check_answer(i),
            )
            btn.pack(pady=5, ipadx=20, ipady=10, fill="x")
            self.answer_buttons.append(btn)

        # Frame für den Score
        self.score_label = tk.Label(
            self.root,
            text=f"Punkte: {self.score}",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        )
        self.score_label.pack(pady=20)

        # Timer-Label
        self.timer_label = tk.Label(
            self.root,
            text=f"Zeit: {self.time_left} Sekunden",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        )
        self.timer_label.pack(pady=20)

        # Label für Feedback (Richtig/Falsch)
        self.feedback_label = tk.Label(
            self.root, text="", font=self.label_font, fg="white", bg="#2e2e2e"
        )
        self.feedback_label.pack(pady=20)

    
    
    def load_next_question(self):
        # Überprüfen, ob das Spiel beendet wurde und beendet die Methode
        if self.time_left <= 0:
            return

        # Lade die nächste Frage
        question_id = self.question_ids
        print("ID:", question_id)
        question_data = self.question_repo.get_question()
        print( question_data)
        # Debugging: Überprüfen, welche Schlüssel in question_data vorhanden sind
        # print(f"Erhaltene Daten für Frage ID {question_id}: {question_data}")

        try:
            question_text = question_data.get("questionText", "Keine Frage vorhanden")
            correct_answer = question_data.get("correctAnswer", "Keine richtige Antwort")
            incorrect_answers = [
                question_data.get("incorrectAnswer1", "Keine falsche Antwort 1"),
                question_data.get("incorrectAnswer2", "Keine falsche Antwort 2"),
                question_data.get("incorrectAnswer3", "Keine falsche Antwort 3"),
            ]
            difficulty_id = question_data.get("difficultyID", -1)  # Standardwert, wenn nicht vorhanden

            print(f"Frage: {question_text}")
            print(f"Richtige Antwort: {correct_answer}")
            print(f"Falsche Antworten: {incorrect_answers}")
            print(f"Schwierigkeitsgrad: {difficulty_id}")

        except KeyError as e:
            print(f"Fehlender Schlüssel in den Daten: {e}")
            self.end_game()
            return

        # Mische die Antworten
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)

        # Speichere die aktuelle Frage und ihre Daten direkt in der Instanz
        self.current_question = {
            "question_text": question_text,
            "options": all_answers,
            "correct_answer": correct_answer,
            "difficulty": difficulty_id,
        }

        # Frage und Antworten in der GUI anzeigen
        self.question_label.config(
            text=f"Frage ID: {question_id}\n\n{self.current_question['question_text']}\n\n"
        )
        for i, option in enumerate(self.current_question["options"]):
            self.answer_buttons[i].config(text=option, state="normal")

        # Schwierigkeit anzeigen
        difficulty_mapping = {
            1: ("leicht", "green"),
            2: ("mittel", "yellow"),
            3: ("schwer", "red"),
        }
        difficulty_text, difficulty_color = difficulty_mapping.get(
            self.current_question["difficulty"], ("unbekannt", "white")
        )

        if hasattr(self, "difficulty_label"):
            # Entferne das alte Label, falls vorhanden
            self.difficulty_label.destroy() 

        self.difficulty_label = tk.Label(
            self.root,
            text=f"Schwierigkeit: {difficulty_text.capitalize()}",
            font=self.label_font,
            fg=difficulty_color,
            bg="#2e2e2e",
        )
        self.difficulty_label.pack(pady=10)

        # Punkte für die aktuelle Frage holen
        question_points = self.question_repo.get_question_points(question_id)
        self.current_question_points = question_points[1] if question_points else 0

        self.current_question_index += 1

        # Timer zurücksetzen und starten
        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Zeit: {self.time_left} Sekunden")
            self.time_left -= 1
            # Speichere das after-Handle
            self.timer_after_id = self.root.after(1000, self.update_timer)
        else:
            # Zeit abgelaufen
            if self.time_left == 0:  # Verhindere mehrfaches Aufrufen von end_game
                self.end_game()
    # holt die ausgewählte Antwort, überprüft sie nach richtigkeit und schwierigkeit, und berechnet die Punkte
    def check_answer(self, selected_index):
        selected_answer = self.current_question["options"][selected_index]
        is_correct = selected_answer == self.current_question["correct_answer"]
        difficulty = self.current_question["difficulty"]

        question_points = self.calculate_question_points(is_correct, difficulty, self.time_left)
        if is_correct:
            self.score += question_points
            self.feedback_label.config(
                text=f"Richtig! (+{question_points} Punkte)", fg="green"
            )
        else:
            self.feedback_label.config(
                text=f"Falsch! Richtige Antwort: {self.current_question['correct_answer']}",
                fg="red",
            )

        # Aktualisiere den Punktestand
        self.score_label.config(text=f"Punkte: {self.score}")

        # Lade die nächste Frage nach kurzer Verzögerung
        self.next_question_after_id = self.root.after(2000, self.load_next_question)

    def end_game(self):
        # Stoppe den Timer
        self.time_left = 0

        # Abbrechen des geplanten after-Callbacks für den Timer
        if hasattr(self, "timer_after_id"):
            self.root.after_cancel(self.timer_after_id)

        if hasattr(self, "next_question_after_id"):
            self.root.after_cancel(self.next_question_after_id)

        # Entferne alle Widgets und zeige die Endpunktzahl
        for widget in self.root.winfo_children():
            widget.destroy()

        # Zeige die Punktzahl
        tk.Label(
            self.root,
            text=f"Spiel beendet! Deine Punktzahl: {self.score}",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=20)

        # Aktualisiere den höchsten Punktestand des Spielers
        player_id = 1# Beispiel: Ersetze dies durch die tatsächliche Spieler-ID
        
        self.update_high_score(player_id, self.score)

        # Button zum Entry-Screen
        tk.Button(
            self.root,
            text="Zurück zum Hauptmenü",
            font=self.btn_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=self.return_to_entry_screen,
        ).pack(pady=20, ipadx=20, ipady=10)

        # Button zum Leaderboard
        tk.Button(
            self.root,
            text="Leaderboard anzeigen",
            font=self.btn_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=self.show_leaderboard,
        ).pack(pady=20, ipadx=20, ipady=10)

    def show_leaderboard(self):
        self.root.destroy()
        from GUI.leaderboard_screen import leaderboard_screen  # Importiere die Funktion
        leaderboard_screen()  # Starte die Leaderboard-Screen-Funktion

    def update_high_score(self, player_id, final_score):
        player_repo = PlayerRepository()
        player_repo.update_high_score(player_id,final_score)
        print(f"Game ended. Final score for player {player_id}: {final_score}")

    def return_to_entry_screen(self):
        self.root.destroy()
        from GUI.entry_screen import entry_screen  # Importieren Sie die Funktion

        entry_screen()  # Starten Sie den Entry-Screen

    def calculate_question_points(self, is_correct, difficulty, time_left):
       
        """ 
        difficulty: Die Schwierigkeit der Frage (z. B. "leicht", "mittel", "schwer")
        param time_left: Verbleibende Zeit in Sekunden
        return: Punkte für die Frage
        """
        if not is_correct:
            return 0  # Keine Punkte für falsche Antworten

        # Basispunkte basierend auf der Schwierigkeit
        base_points = {
            "leicht": 1000,
            "mittel": 1500,
            "schwer": 2000,
        }.get(difficulty, 1000)  # Standard: 1000 Punkte für unbekannte Schwierigkeit

        # Bonuspunkte basierend auf der verbleibenden Zeit
        time_bonus = time_left * 10  # 10 Punkte pro verbleibender Sekunde

        return base_points + time_bonus


# Beispielaufruf
if __name__ == "__main__":
    # Ersetze `1` durch die tatsächliche Kategorie-ID, die zuvor ausgewählt wurde
    GameplayScreen(category_id=1)
