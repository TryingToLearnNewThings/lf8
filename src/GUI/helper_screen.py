import tkinter as tk


def helperScreen():
    # Create main window
    root = tk.Tk()
    root.title("Help Instructions")
    root.geometry("1200x800")
    root.configure(bg="#2e2e2e")

    # Fonts and colors
    label_font = ("Helvetica", 16, "bold")
    text_font = ("Helvetica", 14)
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444" 
    btn_fg = "#DDDDDD" 

    # Title
    tk.Label(
        root,
        text="Help Instructions for the Quiz Game",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Help text
    help_text = """
    Welcome to the Quiz Game! Here are some tips and instructions to help you:

    1. Objective of the Game:
       - Answer as many questions as possible correctly to earn points.
       - Each question has a specific difficulty level (easy, medium, hard) that affects the points.

    2. Controls:
       - Choose the correct answer from the four options.
       - You can press the Enter key to submit your answer.
       - You can press the "h" key to open the help instructions.

    3. Time Limit:
       - Each question has a time limit of 60 seconds. Answer the question before the time runs out.

    4. Categories:
       - Choose a category to answer questions on a specific topic.
       - Examples of categories: Geography, Video Games, General Knowledge.

    5. Points:
       - For each correct answer, you earn points based on the difficulty of the question.
       - Incorrect answers do not give any points.

    6. End Game:
       - You can end the game at any time using the "End Game" button at the top right.

    Good luck and have fun playing!
    """

    tk.Label(
        root,
        text=help_text,
        font=text_font,
        fg="white",
        bg="#2e2e2e",
        justify="left",
        wraplength=1000,
    ).pack(pady=20)

    # Back button
    tk.Button(
        root,
        text="Back to Main Menu",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=root.destroy,  # Closes the help screen
    ).pack(pady=20, ipadx=20, ipady=10)

    root.mainloop()


# if __name__ == "__main__":
#     helperScreen()