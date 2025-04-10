import tkinter as tk
from repositories.player_repository import PlayerRepository

def achievementScreen(player_repo):
    # Initialises the main window
    root = tk.Tk()
    root.title("Achievements")
    root.geometry("800x600")
    root.configure(bg="#2e2e2e")

    # Headline
    tk.Label(
        root,
        text="Achievements",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Table of achievements
    achievement_frame = tk.Frame(root, bg="#2e2e2e")
    achievement_frame.pack(pady=20)

    # Column headings
    tk.Label(
        achievement_frame,
        text="Achievement",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=30,
    ).grid(row=0, column=0)
    tk.Label(
        achievement_frame,
        text="Status",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=15,
    ).grid(row=0, column=1)

    # Retrieves player data from the database
    achievements = player_repo.Achievment_player_info()

    # Shows achievements in the table
    for index, achievement in enumerate(achievements):
        tk.Label(
            achievement_frame,
            text=achievement["name"],
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
            width=30,
        ).grid(row=index + 1, column=0)
        status = "Achieved" if achievement["achieved"] else "Not Achieved"
        tk.Label(
            achievement_frame,
            text=status,
            font=("Helvetica", 14),
            fg="white" if achievement["achieved"] else "red",
            bg="#2e2e2e",
            width=15,
        ).grid(row=index + 1, column=1)

    # Button to main menu
    tk.Button(
        root,
        text="Back to Main Menu",
        font=("Helvetica", 14, "bold"),
        bg="#444444",
        fg="#DDDDDD",
        relief="flat",
        command=root.destroy,
    ).pack(pady=20, ipadx=20, ipady=10)

    root.mainloop()