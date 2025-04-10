import tkinter as tk
from tkinter import ttk
from .category_screen import categoryScreen
from .achievement_screen import achievementScreen
from .helper_screen import helperScreen


# Function to open the category selection
# Closes entry screen and starts category selection screen
def openCategoryScreen(player_repo):
    main_screen.destroy()
    categoryScreen(player_repo)


# Main screen (Entry Screen)
def entryScreen(player_repo):
    global main_screen
    main_screen = tk.Tk()
    main_screen.title("Mainmenu")
    main_screen.geometry("1200x800")
    main_screen.configure(bg="#2e2e2e")

    # Fonts and colours
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"
    btn_fg = "#DDDDDD"

    # Frame for complete centring
    frame = tk.Frame(main_screen, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title-Label
    tk.Label(
        frame,
        text="Welcome to our Quizgame!",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Button for category selection
    tk.Button(
        frame,
        text="Start Game",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=lambda: openCategoryScreen(player_repo),
    ).pack(pady=10, ipadx=20, ipady=10)

    # Button to the achievements
    tk.Button(
        frame,
        text="My Achievements",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=lambda: openAchievementScreen(player_repo),
    ).pack(pady=10, ipadx=20, ipady=10)

    # Button for the helper screen in the bottom-right corner
    help_button = tk.Button(
        main_screen,
        text="Help",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=helperScreen,  # Opens the helper screen
    )
    help_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    # Binds the "h" key to open the helper screen
    main_screen.bind("h", lambda event: helperScreen())

    main_screen.mainloop()

# Closes entry screen and opens achievement screen
def openAchievementScreen(player_repo):
    main_screen.destroy()
    achievementScreen(player_repo)
