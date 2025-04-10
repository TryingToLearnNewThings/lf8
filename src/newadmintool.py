import tkinter as tk
from tkinter import messagebox
from repositories.question_repository import QuestionRepository
import sqlite3


class AdminTool:
    def __init__(self):
        # Database connection
        self.db_path = "Database/database.db"
        self.connection = sqlite3.connect(self.db_path)
        self.question_repo = QuestionRepository(self.connection)

        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Admin Tool - Frage anzeigen")
        self.root.geometry("1280x720")  # HD-Auflösung
        self.root.configure(bg="#2e2e2e")

        # Create the GUI elements
        self.create_gui()

        # Start the main loop
        self.root.mainloop()

    def create_gui(self):
        """Creates the GUI for entering questionID and displaying the question."""
        tk.Label(
            self.root,
            text="Frage-ID eingeben:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)

        self.question_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.question_id_entry.pack(pady=10)

        tk.Button(
            self.root,
            text="Frage anzeigen",
            font=("Helvetica", 14, "bold"),
            bg="#444444",
            fg="#DDDDDD",
            relief="flat",
            command=self.show_question,
        ).pack(pady=10, ipadx=20, ipady=10)

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            fg="white",
            bg="#2e2e2e",
            wraplength=500,
            justify="left",
        )
        self.result_label.pack(pady=20)

        self.edit_button = tk.Button(
            self.root,
            text="Frage bearbeiten",
            font=("Helvetica", 14, "bold"),
            bg="#444444",
            fg="#DDDDDD",
            relief="flat",
            command=self.open_question_editor,
            state="disabled",  # Initially disabled
        )
        self.edit_button.pack(pady=10, ipadx=20, ipady=10)

        self.delete_button = tk.Button(
            self.root,
            text="Frage löschen",
            font=("Helvetica", 14, "bold"),
            bg="#FF4444",
            fg="#FFFFFF",
            relief="flat",
            command=self.delete_question,
            state="disabled",  # Initially disabled
        )
        self.delete_button.pack(pady=10, ipadx=20, ipady=10)

        tk.Button(
            self.root,
            text="Neue Frage erstellen",
            font=("Helvetica", 14, "bold"),
            bg="#444444",
            fg="#DDDDDD",
            relief="flat",
            command=self.open_create_question_window,
        ).pack(pady=10, ipadx=20, ipady=10)

    def show_question(self):
        """Fetches and displays the question based on the entered questionID."""
        try:
            question_id = int(self.question_id_entry.get().strip())
            self.current_question = self.question_repo.Get_question_by_id(question_id)

            if self.current_question:
                question_text = self.current_question["questionText"]
                answers = self.current_question["answers"]
                correct_answer = answers[0]["answerText"]  # Correct answer is always the first
                incorrect_answers = [a["answerText"] for a in answers[1:]]  # Remaining are incorrect

                result_text = (
                    f"Frage: {question_text}\n\n"
                    f"Korrekte Antwort: {correct_answer}\n"
                    f"Falsche Antworten:\n"
                    f" - {incorrect_answers[0]}\n"
                    f" - {incorrect_answers[1]}\n"
                    f" - {incorrect_answers[2]}"
                )
                self.result_label.config(text=result_text)
                self.edit_button.config(state="normal")  # Enable the edit button
                self.delete_button.config(state="normal")  # Enable the delete button
            else:
                self.result_label.config(text="Keine Frage mit dieser ID gefunden.")
                self.edit_button.config(state="disabled")
                self.delete_button.config(state="disabled")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Frage-ID ein.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def delete_question(self):
        """Deletes the question from the database."""
        try:
            question_id = int(self.question_id_entry.get().strip())
            confirm = messagebox.askyesno(
                "Bestätigung",
                f"Sind Sie sicher, dass Sie die Frage mit ID {question_id} löschen möchten?",
            )
            if confirm:
                self.question_repo.Delete_question(question_id)
                messagebox.showinfo("Erfolg", "Die Frage wurde erfolgreich gelöscht.")
                self.result_label.config(text="")
                self.edit_button.config(state="disabled")
                self.delete_button.config(state="disabled")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Frage-ID ein.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen der Frage: {e}")

    def open_question_editor(self):
        """Opens the Question Editor view."""
        if not self.current_question:
            messagebox.showerror("Fehler", "Keine Frage zum Bearbeiten gefunden.")
            return

        editor = tk.Toplevel(self.root)
        editor.title("Fragen Editor")
        editor.geometry("800x600")  # Einheitliche Standardgröße
        editor.configure(bg="#2e2e2e")

        # Question Text
        tk.Label(
            editor,
            text="Fragetext:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)
        question_text_entry = tk.Entry(editor, font=("Helvetica", 14), width=50)
        question_text_entry.insert(0, self.current_question["questionText"])
        question_text_entry.pack(pady=10)

        # Answers
        tk.Label(
            editor,
            text="Antworten:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)

        answer_entries = []
        correct_answer_var = tk.IntVar(value=1)  # Default correct answer is the first one

        for i, answer in enumerate(self.current_question["answers"], start=1):
            frame = tk.Frame(editor, bg="#2e2e2e")
            frame.pack(pady=5)

            tk.Radiobutton(
                frame,
                text="Korrekt",
                variable=correct_answer_var,
                value=i,
                bg="#2e2e2e",
                fg="white",
                selectcolor="#444444",
            ).pack(side="left", padx=5)

            entry = tk.Entry(frame, font=("Helvetica", 14), width=40)
            entry.insert(0, answer["answerText"])
            entry.pack(side="left", padx=5)
            answer_entries.append(entry)

        # Save Button
        tk.Button(
            editor,
            text="Speichern",
            font=("Helvetica", 14, "bold"),
            bg="#444444",
            fg="#DDDDDD",
            relief="flat",
            command=lambda: self.save_question_changes(
                question_text_entry.get(),
                [entry.get() for entry in answer_entries],
                correct_answer_var.get(),
            ),
        ).pack(pady=20, ipadx=20, ipady=10)

    def save_question_changes(self, question_text, answers, correct_answer_index):
        """Saves the changes made to the question."""
        try:
            question_id = int(self.question_id_entry.get().strip())
            self.question_repo.Update_question(
                questionID=question_id,
                question_text=question_text,
                answers=answers,
                correct_answer_index=correct_answer_index,
            )
            messagebox.showinfo("Erfolg", "Die Frage wurde erfolgreich aktualisiert.")
            self.result_label.config(text="Frage wurde aktualisiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Änderungen: {e}")

    def open_create_question_window(self):
        """Opens a window to create a new question."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Neue Frage erstellen")
        create_window.geometry("720x720")  # Einheitliche Standardgröße
        create_window.configure(bg="#2e2e2e")

        # Question Text
        tk.Label(
            create_window,
            text="Fragetext:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)
        question_text_entry = tk.Entry(create_window, font=("Helvetica", 14), width=50)
        question_text_entry.pack(pady=10)

        # Answers
        tk.Label(
            create_window,
            text="Antworten:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)

        answer_entries = []
        correct_answer_var = tk.IntVar(value=1)  # Default correct answer is the first one

        for i in range(4):  # Four answers
            frame = tk.Frame(create_window, bg="#2e2e2e")
            frame.pack(pady=5)

            tk.Radiobutton(
                frame,
                text="Korrekt",
                variable=correct_answer_var,
                value=i + 1,
                bg="#2e2e2e",
                fg="white",
                selectcolor="#444444",
            ).pack(side="left", padx=5)

            entry = tk.Entry(frame, font=("Helvetica", 14), width=40)
            entry.pack(side="left", padx=5)
            answer_entries.append(entry)

        # Category Selection
        tk.Label(
            create_window,
            text="Kategorie:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)

        category_var = tk.IntVar(value=1)  # Default category
        categories = {
            1: "Entertainment: Video Games",
            2: "Geography",
            3: "General Knowledge",
            4: "Entertainment: Japanese Anime and Manga",
            5: "Politics",
        }
        for category_id, category_name in categories.items():
            tk.Radiobutton(
                create_window,
                text=f"{category_name} (ID: {category_id})",
                variable=category_var,
                value=category_id,
                bg="#2e2e2e",
                fg="white",
                selectcolor="#444444",
            ).pack(anchor="w", padx=20)

        # Difficulty Selection
        tk.Label(
            create_window,
            text="Schwierigkeit:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=10)

        difficulty_var = tk.IntVar(value=1)  # Default difficulty
        difficulties = {
            1: "Medium",
            2: "Hard",
            3: "Easy",
        }
        for difficulty_id, difficulty_name in difficulties.items():
            tk.Radiobutton(
                create_window,
                text=f"{difficulty_name} (ID: {difficulty_id})",
                variable=difficulty_var,
                value=difficulty_id,
                bg="#2e2e2e",
                fg="white",
                selectcolor="#444444",
            ).pack(anchor="w", padx=20)

        # Save Button
        tk.Button(
            create_window,
            text="Frage speichern",
            font=("Helvetica", 14, "bold"),
            bg="#444444",
            fg="#DDDDDD",
            relief="flat",
            command=lambda: self.save_new_question(
                question_text_entry.get(),
                [entry.get() for entry in answer_entries],
                correct_answer_var.get(),
                category_var.get(),
                difficulty_var.get(),
            ),
        ).pack(pady=20, ipadx=20, ipady=10)

    def save_new_question(self, question_text, answers, correct_answer_index, category_id, difficulty_id):
        """Saves the new question to the database."""
        try:
            if not question_text or not all(answers) or correct_answer_index == 0:
                messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
                return

            self.question_repo.Create_question(
                question=question_text,
                category_id=category_id,
                difficulty_id=difficulty_id,
                correct_answer=answers[correct_answer_index - 1],
                incorrect_answer1=answers[0] if correct_answer_index != 1 else answers[1],
                incorrect_answer2=answers[1] if correct_answer_index != 2 else answers[2],
                incorrect_answer3=answers[2] if correct_answer_index != 3 else answers[3],
            )
            messagebox.showinfo("Erfolg", "Die Frage wurde erfolgreich erstellt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Frage: {e}")


if __name__ == "__main__":
    AdminTool()