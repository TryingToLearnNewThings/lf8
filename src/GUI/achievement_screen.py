import tkinter as tk
from repositories.player_repository import PlayerRepository

def achievement_screen():
    # Initialisiere das Hauptfenster
    root = tk.Tk()
    root.title("Achievements")
    root.geometry("800x600")
    root.configure(bg="#2e2e2e")

    # Überschrift
    tk.Label(
        root,
        text="Achievements",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Tabelle für Achievements
    achievement_frame = tk.Frame(root, bg="#2e2e2e")
    achievement_frame.pack(pady=20)

    # Spaltenüberschriften
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

    # Spieler-Daten aus der Datenbank abrufen
    player_repo = PlayerRepository()
    player_id = 1  # Beispiel: Ersetze dies durch die tatsächliche Spieler-ID
    achievements = player_repo.get_all_player_achievements(player_id)

    # Achievements in der Tabelle anzeigen
    for index, achievement in enumerate(achievements):
        tk.Label(
            achievement_frame,
            text=achievement["name"],
            font=("Helvetica", 14),
            fg="white",
            bg="#2e2e2e",
            width=30,
        ).grid(row=index + 1, column=0)
        status = "Erreicht" if achievement["achieved"] else "Nicht erreicht"
        tk.Label(
            achievement_frame,
            text=status,
            font=("Helvetica", 14),
            fg="white" if achievement["achieved"] else "red",
            bg="#2e2e2e",
            width=15,
        ).grid(row=index + 1, column=1)

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