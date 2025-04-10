import sys
import os
import random

# Adds the main folder 'src' to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox
from repositories.question_repository import QuestionRepository
from repositories.difficulty_repository import DifficultyRepository
from player import Player
from repositories.achievment_repository import AchievmentRepository
from GUI.leaderboard_screen import leaderboardScreen



class GameplayScreen:
    def __init__(self, category_id, player_repo):
        self.category_id = category_id
        self.question_repo = QuestionRepository()
        self.player_repo = player_repo
        self.player_id = None
        self.current_question = None
        self.score = 0
        self.question_id = None
        self.not_answert = self.question_repo.Get_questionids_with_categorys(self.category_id)
        self.time_left = 30  # Timer in seconds

        # Initialises the main window
        self.root = tk.Tk()
        self.root.title("Quiz Game")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2e2e2e")

        # Fonts and colours
        self.label_font = ("Helvetica", 16, "bold")
        self.btn_font = ("Helvetica", 14, "bold")
        self.btn_bg = "#444444"
        self.btn_fg = "#DDDDDD"

        # Creates GUI elements
        self.Create_widgets()

        # Loads first question
        self.Load_next_question()

        self.root.mainloop()

    def Create_widgets(self):
        # Frame for the question
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

        # Frame for the answer buttons
        self.answer_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.answer_frame.pack(pady=20)

        self.answer_buttons = []
        # Maximum of four possible answers
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

        # Frame for the score
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        )
        self.score_label.pack(pady=20)

        # Timer-Label
        self.timer_label = tk.Label(
            self.root,
            text=f"Time: {self.time_left} seconds",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        )
        self.timer_label.pack(pady=20)

        # Label for feedback (True/False)
        self.feedback_label = tk.Label(
            self.root, text="", font=self.label_font, fg="white", bg="#2e2e2e"
        )
        self.feedback_label.pack(pady=20)

        # Button to end the game (top right)
        self.end_game_button = tk.Button(
            self.root,
            text="End Game",
            font=self.btn_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=self.end_game,  # Calls up the method for exiting the game
        )
        self.end_game_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
    
    
    def Load_next_question(self):
        # Checks whether the game has ended
        if self.time_left <= 0:
            return

        # Pauses timer while next question is loaded
        if hasattr(self, "timer_after_id") and self.timer_after_id is not None:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        # Loads the next question
        self.question_id = self.question_repo.Get_random_questionID(self.not_answert)
        self.not_answert.remove(self.question_id)
        question_data = self.question_repo.Get_question()

        try:
            question_text = question_data.get("questionText", "Keine Frage vorhanden")
            correct_answer = question_data.get("correctAnswer", "Keine richtige Antwort")
            incorrect_answers = [
                question_data.get("incorrectAnswer1", "Keine falsche Antwort 1"),
                question_data.get("incorrectAnswer2", "Keine falsche Antwort 2"),
                question_data.get("incorrectAnswer3", "Keine falsche Antwort 3"),
            ]
            difficulty_id = question_data.get("difficultyID", -1)  # Default value, if not available

            #debugging
            # print(f"Frage: {question_text}")
            # print(f"Richtige Antwort: {correct_answer}")
            # print(f"Falsche Antworten: {incorrect_answers}")
            # print(f"Schwierigkeitsgrad: {difficulty_id}")

        except KeyError as e:
            print(f"Fehlender Schlüssel in den Daten: {e}")
            self.end_game()
            return

        # Mixes the answers
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)
        
        # Saves the current question and its data directly in the instance
        self.current_question = {
            "question_text": question_text,
            "options": all_answers,
            "correct_answer": correct_answer,
            "difficulty": difficulty_id,
        }

        # Displays questions and answers in the GUI
        self.question_label.config(
            text=f"{self.current_question['question_text']}\n\n"
        )
        for i, option in enumerate(self.current_question["options"]):
            self.answer_buttons[i].config(text=option, state="normal")
        difficulty_repo = DifficultyRepository()
        difficulty_mapping = difficulty_repo.Get_all_difficulties()  
        # difficulty_mapping = {
        #     1: ("leicht", "green"),
        #     2: ("mittel", "yellow"),
        #     3: ("schwer", "red"),
        # }
        difficulty_text, difficulty_color = difficulty_mapping.get(
            self.current_question["difficulty"], ("unbekannt", "white")
        )

        if hasattr(self, "difficulty_label"):
            # Removes the old label, if present
            self.difficulty_label.destroy()

        # Creates difficulty display
        self.difficulty_label = tk.Label(
            self.question_frame,
            text=f"Difficulty: {difficulty_text.capitalize()}",
            font=self.label_font,
            fg=difficulty_color,
            bg="#2e2e2e",
        )
        # Places the difficulty indicator in the centre above the question
        self.difficulty_label.pack(pady=(0, 10))

        # Gets points for the current question
        question_points = self.question_repo.Get_question_points(self.question_id)
        self.current_question_points = question_points if question_points else 0

        # Continues timer
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Zeit: {self.time_left} Sekunden")
            self.time_left -= 1
            # Saves the after handle
            self.timer_after_id = self.root.after(1000, self.update_timer)
        else:
            # Time expired
            if hasattr(self, "timer_after_id") and self.timer_after_id is not None:
                self.root.after_cancel(self.timer_after_id)
                self.timer_after_id = None 
            self.end_game()

    # Retrieves the selected answer, checks it for correctness and difficulty, and calculates the points
    def check_answer(self, selected_index):
        selected_answer = self.current_question["options"][selected_index]
        is_correct = selected_answer == self.current_question["correct_answer"]
        difficulty = self.current_question["difficulty"]
        difficulty_repo = DifficultyRepository()
        difficulty_name = difficulty_repo.Get_value_from_table("Difficulty", "difficultyName", "difficultyID",difficulty)
        question_points = difficulty_repo.get_difficulty_infos("difficultyPoints","difficultyID",difficulty)
        # print("difficulty 2", difficulty)
        # question_points = self.calculate_question_points(is_correct, difficulty, self.time_left)
       
        
        if is_correct:
            time_bonus = self.time_left * 10 
            self.score += (question_points + time_bonus)
            self.feedback_label.config(
                text=f"Correct! (+{question_points} Punkte)", fg="green"
            )
            
            # Checks a player's answer and updates the statistics based on the difficulty of the question.
            

            # Determines the field based on the difficulty
            if difficulty_name == 'easy':
                field = 'correctEasyQuestions'
            elif difficulty_name == 'medium':
                field = 'correctMediumQuestions'
            elif difficulty_name == 'hard':
                field = 'correctHardQuestions'
            else:
                raise ValueError("Invalid difficulty: " + str(difficulty_name))
            old_value = self.player_repo.Get_playerfield_info(field)
            new_value = old_value + 1
            self.player_repo.Update_player_field(field, new_value) 
        else:
            self.feedback_label.config(
                    text=f"Wrong! The right answer was: {self.current_question['correct_answer']}",
                    fg="red",
                )

        # Updates the score
        self.score_label.config(text=f"Points: {self.score}")

        # Loads the next question after a short delay
        self.next_question_after_id = self.root.after(2000, self.Load_next_question)

    #
    def Check_for_achievement(self, player_data):
         
        achievment_repo =AchievmentRepository()
        achievmentsInfos=achievment_repo.Get_all_achievements()
        
        self.player = Player(
                            player_id=self.player_id,
                            score=player_data[1],  
                            correctHardQuestions=player_data[2],
                            correctMediumQuestions=player_data[3],
                            correctEasyQuestions=player_data[4] 
                            )

        player_achievements = self.player_repo.Get_all_player_achievements()
        check_achievment = self.player.Receive_achievement(achievmentsInfos[0],achievmentsInfos[1], achievmentsInfos[2], player_achievements)

        if check_achievment:
            achievment_repo.Fill_player_to_achievments(
                player_data[0], check_achievment
            )

        # new_value_correctanswer = pr.get_correct_Questions_by_difficulty("medium")
       
    
    def end_game(self):
        self.time_left = 0
        
        
        # Cancelling the scheduled after-callback for the timer
        if hasattr(self, "timer_after_id") and self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except ValueError:
                pass  # Timer has already expired
            self.timer_after_id = None

        if hasattr(self, "next_question_after_id") and self.next_question_after_id is not None:
            try:
                self.root.after_cancel(self.next_question_after_id)
            except ValueError:
                pass  # Callback is already executed
            self.next_question_after_id = None

        # Removes all widgets and shows the final score
        for widget in self.root.winfo_children():
            widget.destroy()

        # Shows the score
        tk.Label(
            self.root,
            text=f"Good Job! Your score is: {self.score}",
            font=self.label_font,
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=20)

        # Updates the player's highest score
        playerData = self.player_repo.Get_value_from_table("Player","playerID, playerScore, correctHardQuestions,correctMediumQuestions,correctEasyQuestions","playerID",self.player_repo.Get_player_id())
        self.player_id = playerData[0]
        
        self.Update_high_score()
        self.Check_for_achievement(playerData)
       
        # Button to go back to the main screen
        tk.Button(
            self.root,
            text="Back to Mainmenu",
            font=self.btn_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=self.return_to_entryScreen,
        ).pack(pady=20, ipadx=20, ipady=10)

        # Button to the leaderboard
        tk.Button(
            self.root,
            text="Leaderboard",
            font=self.btn_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=self.Show_leaderboard,
        ).pack(pady=20, ipadx=20, ipady=10)
        
        
    def return_to_entryScreen(self):
        from GUI.entry_screen import entryScreen  # Dynamischer Import, um zirkuläre Abhängigkeiten zu vermeiden
        self.root.destroy()  # Schließt das aktuelle Fenster
        entryScreen(self.player_repo)  # Öffnet den Entry Screen und übergibt das Player Repository# 

    def Show_leaderboard(self):
        self.root.destroy()
        leaderboardScreen(self.player_repo)  # Starts the leaderboard screen

    def Update_high_score(self):
        self.player_repo.Update_high_score(self.player_id,self.score)
        print(f"Game ended. Final score for player {self.player_id}: {self.score}")
    
   