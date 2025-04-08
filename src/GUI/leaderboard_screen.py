import tkinter as tk
from repositories.player_repository import PlayerRepository

def leaderboard_screen():
    # Initialisiere das Hauptfenster
    root = tk.Tk()
    root.title("Leaderboard")
    root.geometry("800x600")
    root.configure(bg="#2e2e2e")

    # Überschrift
    tk.Label(
        root,
        text="Leaderboard",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Tabelle für das Leaderboard
    leaderboard_frame = tk.Frame(root, bg="#2e2e2e")
    leaderboard_frame.pack(pady=20)

    # Spaltenüberschriften
    tk.Label(
        leaderboard_frame,
        text="Platz",
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
        text="Punkte",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        width=10,
    ).grid(row=0, column=2)

    # Spieler-Daten aus der Datenbank abrufen
    player_repo = PlayerRepository()
    players = player_repo.get_all_players_sorted_by_score()

    # Spieler in der Tabelle anzeigen
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

    # Button zum Hauptmenü
    tk.Button(
        root,
        text="Zurück zum Hauptmenü",
        font=("Helvetica", 14, "bold"),
        bg="#444444",
        fg="#DDDDDD",
        relief="flat",
        command=root.destroy,
    ).pack(pady=20, ipadx=20, ipady=10)

    root.mainloop()