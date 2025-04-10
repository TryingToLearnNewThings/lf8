import tkinter as tk

def leaderboardScreen(player_repo):
    # Initialises the main window
    root = tk.Tk()
    root.title("Leaderboard")
    root.geometry("800x600")
    root.configure(bg="#2e2e2e")

    # Headline
    tk.Label(
        root,
        text="Leaderboard",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Table for the leaderboard
    leaderboard_frame = tk.Frame(root, bg="#2e2e2e")
    leaderboard_frame.pack(pady=20)

    # Column headline
    tk.Label(
        leaderboard_frame,
        text="Placement",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=10,
    ).grid(row=0, column=0)
    tk.Label(
        leaderboard_frame,
        text="Name",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=20,
    ).grid(row=0, column=1)
    tk.Label(
        leaderboard_frame,
        text="Points",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=10,
    ).grid(row=0, column=2)

    # Retrieve player data from the database
    players = player_repo.Get_all_players_sorted_by_score()

    # Shows player in the table
    for index, player in enumerate(players):
        tk.Label(
            leaderboard_frame,
            text=f"{index + 1}",
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
            width=10,
        ).grid(row=index + 1, column=0)
        tk.Label(
            leaderboard_frame,
            text=player["playerName"],
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
            width=20,
        ).grid(row=index + 1, column=1)
        tk.Label(
            leaderboard_frame,
            text=player["playerScore"],
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
            width=10,
        ).grid(row=index + 1, column=2)

    # Button to the main menu
    tk.Button(
        root,
        text="Back to Mainscreen",
        font=("Helvetica", 14, "bold"),
        bg="#444444",
        fg="#DDDDDD",
        relief="flat",
        command=lambda: returnToEntryScreen(root,player_repo),  # Use a help function
    ).pack(pady=20, ipadx=20, ipady=10)

    root.mainloop()

def returnToEntryScreen(root,player_repo):
    from .entry_screen import entryScreen 
    root.destroy()  # Closes the leaderboard window
    entryScreen(player_repo)  # Starts the entry screen