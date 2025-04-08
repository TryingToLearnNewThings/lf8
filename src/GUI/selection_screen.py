import tkinter as tk
import requests  # Für API-Anfragen
from tkinter import simpledialog, messagebox
from gameplay_screen import GameplayScreen  # Importiere den GameplayScreen


# Funktion zum Starten des Spiels mit der Auswahl
def start_game_mode(mode, root):
    """
    Startet den ausgewählten Spielmodus und schließt den aktuellen Bildschirm.
    """
    root.destroy()  # Schließt das Auswahlfenster
    if mode == "Singleplayer":
        GameplayScreen(category_id=1)  # Beispiel: Kategorie-ID = 1
    elif mode == "Multiplayer":
        multiplayer_screen()
    else:
        print(f"Unbekannter Modus: {mode}")


def create_multiplayer_game():
    try:
        # API-Aufruf, um ein neues Multiplayer-Spiel zu erstellen
        response = requests.post(
            "http://127.0.0.1:5000/create_game", json={"creatorID": 1}
        )  # Beispiel: creatorID = 1
        if response.status_code == 201:
            game_data = response.json()
            game_key = game_data.get("game_key")
            game_id = game_data.get("gameID")
            messagebox.showinfo(
                "Spiel erstellt", f"Spiel erstellt!\nGame Key: {game_key}"
            )
            print(
                f"Multiplayer-Spiel erstellt: Game Key: {game_key}, Game ID: {game_id}"
            )
        else:
            error_message = response.json().get("error", "Unbekannter Fehler")
            messagebox.showerror(
                "Fehler", f"Fehler beim Erstellen des Spiels: {error_message}"
            )
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Verbinden mit dem Server: {e}")


def join_multiplayer_game():
    # Dialog zur Eingabe des Game Keys
    game_key = simpledialog.askstring("Spiel beitreten", "Bitte gib den Game Key ein:")
    if not game_key:
        return  # Abbrechen, wenn kein Game Key eingegeben wurde

    try:
        # API-Aufruf, um einem bestehenden Spiel beizutreten
        response = requests.post(
            "http://127.0.0.1:5000/join_game",
            json={"game_key": game_key, "playerID": 1},
        )  # Beispiel: playerID = 1
        if response.status_code == 200:
            messagebox.showinfo(
                "Beigetreten", "Du bist dem Spiel erfolgreich beigetreten!"
            )
            print(f"Spiel beigetreten: Game Key: {game_key}")
        else:
            error_message = response.json().get("error", "Unbekannter Fehler")
            messagebox.showerror(
                "Fehler", f"Fehler beim Beitreten zum Spiel: {error_message}"
            )
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Verbinden mit dem Server: {e}")


def multiplayer_screen():
    multiplayer_window = tk.Toplevel()
    multiplayer_window.title("Multiplayer")
    multiplayer_window.geometry("400x300")
    multiplayer_window.configure(bg="#2e2e2e")

    label_font = ("Helvetica", 14, "bold")
    btn_font = ("Helvetica", 12, "bold")
    btn_bg = "#444444"
    btn_fg = "#DDDDDD"

    tk.Label(
        multiplayer_window,
        text="Multiplayer Optionen",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    btn_create = tk.Button(
        multiplayer_window,
        text="Spiel erstellen",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=create_multiplayer_game,
    )
    btn_create.pack(pady=10, ipadx=20, ipady=10)

    btn_join = tk.Button(
        multiplayer_window,
        text="Spiel beitreten",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=join_multiplayer_game,
    )
    btn_join.pack(pady=10, ipadx=20, ipady=10)


def mode_screen():
    root = tk.Tk()
    root.title("Wähle deinen Modus")
    root.geometry("800x600")
    root.configure(bg="#2e2e2e")  # Standard-Hintergrundfarbe

    # Schriftarten und Farben
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"  # Dunkleres Grau für Buttons
    btn_fg = "#DDDDDD"  # Hellgrauer Text

    # Frame zum vollständigen Zentrieren
    frame = tk.Frame(root, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Modus-Auswahl Label
    tk.Label(
        frame,
        text="Wählen Sie den Spielmodus",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Buttons für Spielmodi
    btn_singleplayer = tk.Button(
        frame,
        text="🎮 Singleplayer",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=lambda: start_game_mode(
            "Singleplayer", root
        ),  # Ruft den Singleplayer-Modus auf
    )
    btn_singleplayer.pack(pady=30, ipadx=40, ipady=20)

    btn_multiplayer = tk.Button(
        frame,
        text="🤝 Multiplayer",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=lambda: start_game_mode(
            "Multiplayer", root
        ),  # Ruft den Multiplayer-Modus auf
    )
    btn_multiplayer.pack(pady=30, ipadx=40, ipady=20)

    root.mainloop()
